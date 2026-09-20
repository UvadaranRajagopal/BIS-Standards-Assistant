import { useState } from "react";
import { CheckCircle, FileText } from "lucide-react";
import type { StandardResult } from "../services/api";

interface Props {
  results: StandardResult[];
  onAccept: (standards: string[]) => void;
  accepted: boolean;
}

export default function ResultsList({
  results,
  onAccept,
  accepted,
}: Props) {
  const [verified, setVerified] = useState(false);
  const [evidence, setEvidence] = useState<string | null>(null);

  if (results.length === 0) {
    return null;
  }

  return (
    <div className="results-box">
      <h2>Recommended BIS Standards</h2>

      {results.map((result) => (
        <div className="result-card" key={result.id}>
          <div className="result-header">
            <div>
              <h3>{result.metadata.is_number}</h3>
              <p>{result.metadata.title}</p>
            </div>

            <span className="score">
              {result.relevance_score}% Match
            </span>
          </div>

          <div className="metadata">
            <div>
              <small>Category</small>
              <strong>{result.metadata.category}</strong>
            </div>

            <div>
              <small>Year</small>
              <strong>{result.metadata.year || "N/A"}</strong>
            </div>

            <div>
              <small>Status</small>
              <strong>{result.metadata.status || "N/A"}</strong>
            </div>
          </div>

          <button
            className="evidence-button"
            onClick={() =>
              setEvidence(
                evidence === result.id ? null : result.id
              )
            }
          >
            <FileText size={16} />
            {evidence === result.id
              ? "Hide Evidence"
              : "View Evidence"}
          </button>

          {evidence === result.id && (
            <div className="evidence">
              <strong>Evidence:</strong>
              <p>{result.document}</p>
            </div>
          )}
        </div>
      ))}

      <div className="accept-section">
        {!accepted ? (
          <>
            <label>
              <input
                type="checkbox"
                checked={verified}
                onChange={(e) => setVerified(e.target.checked)}
              />

              I have verified these standards against official BIS
              records.
            </label>

            <button
              className="accept-button"
              disabled={!verified}
              onClick={() =>
                onAccept(
                  results.map(
                    (result) => result.metadata.is_number
                  )
                )
              }
            >
              <CheckCircle size={18} />
              Accept Standards & Generate PDF
            </button>
          </>
        ) : (
          <div className="success">
            <CheckCircle size={40} />
            <h3>Standards Accepted</h3>
            <p>PDF bundle has been generated.</p>
          </div>
        )}
      </div>
    </div>
  );
}