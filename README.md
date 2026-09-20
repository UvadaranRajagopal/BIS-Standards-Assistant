@"
# BIS Standards Assistant

AI-Powered RAG Engine for Indian Standards and Government Procurement

## Overview

BIS Standards Assistant is an AI-assisted procurement standards analysis system designed to help users identify relevant Bureau of Indian Standards (BIS) standards from tender requirements.

The system uses Retrieval-Augmented Generation (RAG) to retrieve relevant BIS standards from a curated knowledge base and uses a local LLM to generate grounded explanations.

## Key Features

- Tender requirement analysis
- AI-assisted BIS standard retrieval
- Semantic search using vector embeddings
- RAG-based explanations
- Certification requirement information
- QCO and CRS metadata
- AI-detected related standards
- Structured procurement requirement extraction
- Officer review workflow
- SHA-256 hash-chain audit trail
- Audit integrity verification
- PDF report generation

## System Architecture

```text
Tender / Procurement Requirement
              |
              v
     Requirement Analysis
              |
              v
      Sentence Transformers
       (Embeddings)
              |
              v
          ChromaDB
     Semantic Retrieval
              |
              v
     Relevant BIS Standards
              |
              v
    Certification Metadata
              |
              v
       Local LLM (Ollama)
              |
              v
      Grounded Explanation
              |
              v
        Officer Review
              |
              v
        Audit Trail
       SHA-256 Hash Chain