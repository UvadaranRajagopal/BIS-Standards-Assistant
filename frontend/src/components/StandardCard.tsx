import {
  FileText,
  RefreshCw,
  Link as LinkIcon,
  CheckCircle,
  AlertTriangle,
} from "lucide-react";

import type { StandardResult } from "../services/api";

interface Props {
  standard: StandardResult;
}

export default function StandardCard({
  standard,
}: Props) {

  const version =
    standard.version_check;

  const related =
    standard.related_standards || [];

  return (
    <div className="standard-card">

      {/* HEADER */}

      <div className="standard-top">

        <div>

          <span className="standard-number">
            {standard.metadata.is_number}
          </span>

          <h3>
            {standard.metadata.title}
          </h3>

        </div>

        <div className="match-score">

          {standard.relevance_score}%

          <small>
            semantic match
          </small>

        </div>

      </div>


      {/* METADATA */}

      <div className="standard-meta">

        <span>
          Category:
          <strong>
            {standard.metadata.category}
          </strong>
        </span>

        <span>
          Year:
          <strong>
            {standard.metadata.year || "N/A"}
          </strong>
        </span>

        <span>
          Status:
          <strong>
            {standard.metadata.status || "Verify"}
          </strong>
        </span>

      </div>


      {/* EVIDENCE */}

      <div className="evidence-box">

        <div className="evidence-title">

          <FileText size={17} />

          <strong>
            Evidence / Scope
          </strong>

        </div>

        <p>
          {standard.document}
        </p>

      </div>


      {/* VERSION */}

      <div
        className={
          version?.status === "CURRENT"
            ? "version-box version-current"
            : "version-box version-warning"
        }
      >

        {version?.status === "CURRENT" ? (
          <CheckCircle size={17} />
        ) : (
          <AlertTriangle size={17} />
        )}

        <div>

          <strong>
            Version & Amendment Check
          </strong>

          <p>
            {version?.message ||
              "Revision information requires verification."}
          </p>

        </div>

      </div>


      {/* RELATED */}

      <div className="related-box">

        <div className="related-title">

          <LinkIcon size={17} />

          <strong>
            Related / Normative Standards
          </strong>

        </div>


        {related.length === 0 ? (

          <p>
            No related standards found.
          </p>

        ) : (

          <div className="related-list">

            {related.map((item) => (

              <div
                className="related-item"
                key={item.id}
              >

                <strong>
                  {item.metadata.is_number}
                </strong>

                <span>
                  {item.metadata.title}
                </span>

              </div>

            ))}

          </div>

        )}

      </div>

    </div>
  );
}