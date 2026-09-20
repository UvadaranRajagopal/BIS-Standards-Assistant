"""
LLM integration using Ollama (Llama 3.1).
Generates natural language explanations from retrieved standards.
"""

import ollama
from app.config import settings


def generate_explanation(
    query: str,
    retrieved_standards: list[dict],
    prompt_template: str = None
) -> str:
    """
    Generate an explanation using ONLY retrieved BIS standards.
    """

    # Build context from retrieved standards
    context_parts = []

    for i, std in enumerate(retrieved_standards, 1):
        context_parts.append(f"""
Standard {i}:
- Number: {std['metadata']['is_number']}
- Title: {std['metadata']['title']}
- Category: {std['metadata'].get('category', 'Not specified')}
- Scope: {std['document']}
- Certification: {std['metadata'].get('certification', 'Not specified')}
""")

    context = "\n".join(context_parts)

    # Default prompt
    if prompt_template is None:
        prompt = f"""You are a BIS standards assistant helping a government officer with procurement.

USER QUERY: "{query}"

RETRIEVED STANDARDS FROM BIS DATABASE:
{context}

INSTRUCTIONS:
1. Answer using ONLY the standards provided above.
2. Do NOT invent or mention standards that are not in the retrieved list.
3. If the retrieved standards do not match the query well, say so.
4. Be very concise and professional.
5. Give only 1 short sentence explaining why each standard is relevant.

YOUR RESPONSE:
"""
    else:
        prompt = prompt_template.format(
            query=query,
            context=context
        )

    # Generate response using Ollama
    try:
        model_name = getattr(
            settings,
            "LLM_PROVIDER",
            "llama3.1:8b"
        )

        response = ollama.generate(
    model=model_name,
    prompt=prompt,
    stream=False,
    options={
        "temperature": 0,
        "num_predict": 120,
        "num_ctx": 2048
    }
)

        return response["response"]

    except Exception as e:
        # Fallback if Ollama is unavailable
        return (
            f"[LLM unavailable] "
            f"Retrieved {len(retrieved_standards)} standards. "
            f"See evidence below:\n\n{context}"
        )


def test_llm():
    """Test LLM with sample BIS standard data."""

    print("=" * 60)
    print("LLM TEST")
    print("=" * 60)

    test_standards = [
        {
            "document": (
                "LED Luminaires for Street Lighting - Specification. "
                "This standard covers requirements for LED luminaires "
                "used in street lighting applications, including "
                "photometric performance, electrical safety, and "
                "environmental durability."
            ),
            "metadata": {
                "is_number": "IS 10322:2025",
                "title": "LED Luminaires for Street Lighting - Specification",
                "category": "LED Lighting & Electrical",
                "certification": "BIS Product Certification"
            }
        }
    ]

    query = "What standards apply to LED street lights for highways?"

    print(f"\nQuery: {query}\n")

    explanation = generate_explanation(
        query,
        test_standards
    )

    print(f"Explanation:\n{explanation}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    test_llm()