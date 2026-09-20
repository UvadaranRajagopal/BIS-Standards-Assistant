import { useEffect, useState } from "react";

import {
  ShieldCheck,
  AlertTriangle,
  Clock,
  FileCheck,
  FileText,
  UserCheck,
  CheckCircle,
} from "lucide-react";

import { auditApi } from "../services/api";

export default function AuditTrail() {
  const [logs, setLogs] = useState<any[]>([]);
  const [integrity, setIntegrity] = useState("checking");
  const [integrityDetails, setIntegrityDetails] = useState<any>(null);

  useEffect(() => {
    async function loadAudit() {
      try {
        const [logsData, integrityData] = await Promise.all([
          auditApi.getLogs(),
          auditApi.verifyIntegrity(),
        ]);

        setLogs(
          Array.isArray(logsData)
            ? logsData
            : logsData.logs || []
        );

        if (
          integrityData.valid === true ||
          integrityData.integrity === "valid"
        ) {
          setIntegrity("valid");
          setIntegrityDetails(null);
        } else {
          setIntegrity("invalid");
          setIntegrityDetails(integrityData.error || null);
        }
      } catch (error) {
        console.error("Audit loading failed:", error);
        setIntegrity("unavailable");
      }
    }

    loadAudit();
  }, []);

  // Backend stores timestamps in UTC without "Z".
  // Convert them correctly to IST for display.
  const formatIST = (timestamp: string) => {
    if (!timestamp) {
      return "";
    }

    const utcTimestamp = timestamp.endsWith("Z")
      ? timestamp
      : timestamp + "Z";

    return (
      new Date(utcTimestamp).toLocaleString("en-IN", {
        timeZone: "Asia/Kolkata",
        day: "2-digit",
        month: "short",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
        hour12: true,
      }) + " IST"
    );
  };

  const getTenderId = (log: any) => {
    return (
      log.data?.tender_id ||
      log.tender_id ||
      "N/A"
    );
  };

  const getAcceptedStandards = (log: any) => {
    const standards = log.data?.accepted_standards;

    if (!standards) {
      return null;
    }

    if (Array.isArray(standards)) {
      return standards;
    }

    return [standards];
  };

  const getCertificationVerifications = (log: any) => {
    return (
      log.data?.certification_verifications ||
      null
    );
  };

  const getActionTitle = (action: string) => {
    switch (action) {
      case "standards_analyzed":
        return "Standards Analyzed";

      case "standards_accepted":
        return "Officer Accepted Standards";

      case "pdf_generated":
        return "PDF Bundle Generated";

      default:
        return action || "System Action";
    }
  };

  const getActionIcon = (action: string) => {
    switch (action) {
      case "standards_analyzed":
        return <FileCheck size={19} />;

      case "standards_accepted":
        return <UserCheck size={19} />;

      case "pdf_generated":
        return <FileText size={19} />;

      default:
        return <ShieldCheck size={19} />;
    }
  };

  return (
    <section className="audit-page-card">

      {/* PAGE HEADER */}
      <div className="audit-page-header">
        <div className="audit-header-copy">
          <span className="audit-eyebrow">
            PROCUREMENT AUDIT
          </span>

          <h3>Audit Trail</h3>

          <p>
            Review recorded procurement actions and verify
            the integrity of the audit chain.
          </p>
        </div>

        <div
          className={
            integrity === "valid"
              ? "integrity-valid"
              : "integrity-invalid"
          }
        >
          {integrity === "valid" ? (
            <>
              <ShieldCheck size={19} />
              <span>
                <strong>Integrity Valid</strong>
                <small>SHA-256 chain verified</small>
              </span>
            </>
          ) : (
            <>
              <AlertTriangle size={19} />
              <span>
                <strong>
                  {integrity === "checking"
                    ? "Checking Integrity"
                    : integrity}
                </strong>

                <small>
                  Audit chain status
                </small>
              </span>
            </>
          )}
        </div>
      </div>

      {/* TAMPER INVESTIGATION */}
      {integrity === "invalid" && integrityDetails && (
        <div className="audit-tamper-panel">
          <div className="audit-tamper-header">
            <div className="audit-tamper-icon">
              <AlertTriangle size={20} />
            </div>

            <div>
              <strong>Security Alert: Audit Integrity Compromised</strong>
              <span>
                The system detected an integrity problem in the audit chain.
              </span>
            </div>

            <span className="audit-tamper-severity">
              {integrityDetails.severity || "HIGH"}
            </span>
          </div>

          <div className="audit-tamper-grid">
            <div className="audit-tamper-item">
              <span>Issue Type</span>
              <strong>
                {String(
                  integrityDetails.issue_type || "INTEGRITY_FAILURE"
                ).replaceAll("_", " ")}
              </strong>
            </div>

            <div className="audit-tamper-item">
              <span>Affected Event</span>
              <strong>
                {integrityDetails.event_index !== null &&
                integrityDetails.event_index !== undefined
                  ? `Event #${integrityDetails.event_index}`
                  : "Unknown"}
              </strong>
            </div>

            <div className="audit-tamper-item">
              <span>Action</span>
              <strong>
                {integrityDetails.action
                  ? getActionTitle(integrityDetails.action)
                  : "Unknown"}
              </strong>
            </div>

            <div className="audit-tamper-item">
              <span>Timestamp</span>
              <strong>
                {integrityDetails.timestamp
                  ? formatIST(integrityDetails.timestamp)
                  : "Unavailable"}
              </strong>
            </div>
          </div>

          <div className="audit-tamper-message">
            <AlertTriangle size={16} />
            <span>
              {integrityDetails.message ||
                "The audit record failed integrity verification."}
            </span>
          </div>

          {integrityDetails.issue_type === "CHAIN_BROKEN" && (
            <div className="audit-hash-comparison">
              <div>
                <span>Expected Previous Hash</span>
                <code>
                  {integrityDetails.expected_previous_hash || "Unavailable"}
                </code>
              </div>

              <div>
                <span>Actual Previous Hash</span>
                <code>
                  {integrityDetails.actual_previous_hash || "Unavailable"}
                </code>
              </div>
            </div>
          )}
        </div>
      )}

      {/* AUDIT HISTORY HEADER */}
      <div className="audit-history-header">
        <div>
          <h4>Audit History</h4>

          <p>
            Chronological record of procurement activity
          </p>
        </div>

        <span className="audit-event-count">
          {logs.length}{" "}
          {logs.length === 1 ? "EVENT" : "EVENTS"}
        </span>
      </div>

      {/* AUDIT EVENTS */}
      <div className="audit-list">

        {logs.length === 0 ? (
          <div className="empty-audit">
            <Clock size={25} />

            <div>
              <strong>No audit events</strong>

              <p>
                No procurement actions have been
                recorded yet.
              </p>
            </div>
          </div>
        ) : (
          logs
            .slice()
            .reverse()
            .map((log, index) => {

              const standards =
                getAcceptedStandards(log);

              const certificationVerifications =
                getCertificationVerifications(log);

              return (
                <article
                  className="audit-event"
                  key={log.index ?? index}
                >

                  {/* EVENT ICON */}
                  <div className="audit-event-icon">
                    {getActionIcon(log.action)}
                  </div>

                  {/* EVENT CONTENT */}
                  <div className="audit-event-content">

                    <div className="audit-event-top">
                      <div>
                        <strong className="audit-event-title">
                          {getActionTitle(log.action)}
                        </strong>

                        <div className="audit-event-meta">
                          <span>
                            Officer:{" "}
                            <b>
                              {log.user_id || "System"}
                            </b>
                          </span>

                          <span>
                            Tender:{" "}
                            <b>
                              {getTenderId(log)}
                            </b>
                          </span>
                        </div>
                      </div>

                      <time className="audit-event-time">
                        <Clock size={13} />
                        {formatIST(log.timestamp)}
                      </time>
                    </div>

                    {/* ACCEPTED STANDARDS */}
                    {standards &&
                      standards.length > 0 && (
                        <div className="audit-detail-block standards-block">

                          <div className="audit-detail-heading">
                            <CheckCircle size={15} />

                            <span>
                              Accepted Standards
                            </span>
                          </div>

                          <div className="standard-badges">
                            {standards.map(
                              (
                                standard: string,
                                standardIndex: number
                              ) => (
                                <span
                                  className="standard-badge"
                                  key={standardIndex}
                                >
                                  {standard}
                                </span>
                              )
                            )}
                          </div>
                        </div>
                      )}

                    {/* CERTIFICATION VERIFICATION */}
                    {certificationVerifications &&
                      Object.keys(
                        certificationVerifications
                      ).length > 0 && (
                        <div className="audit-detail-block certification-block">

                          <div className="audit-detail-heading certification-heading">
                            <ShieldCheck size={15} />

                            <span>
                              Certification Verification
                            </span>
                          </div>

                          <div className="certification-list">
                            {Object.entries(
                              certificationVerifications
                            ).map(
                              (
                                [
                                  standard,
                                  verified,
                                ]
                              ) => (
                                <div
                                  className={
                                    verified
                                      ? "certification-item verified"
                                      : "certification-item not-verified"
                                  }
                                  key={standard}
                                >
                                  {verified ? (
                                    <CheckCircle
                                      size={15}
                                    />
                                  ) : (
                                    <AlertTriangle
                                      size={15}
                                    />
                                  )}

                                  <span className="certification-standard">
                                    {standard}
                                  </span>

                                  <span className="certification-status">
                                    {verified
                                      ? "Verified"
                                      : "Not Verified"}
                                  </span>
                                </div>
                              )
                            )}
                          </div>
                        </div>
                      )}

                    {/* PDF */}
                    {log.data?.pdf_generated && (
                      <div className="audit-pdf">
                        <FileText size={15} />

                        <span>PDF Bundle</span>

                        <b>
                          {String(
                            log.data.pdf_generated
                          )
                            .split("\\")
                            .pop()
                            ?.split("/")
                            .pop()}
                        </b>
                      </div>
                    )}

                  </div>
                </article>
              );
            })
        )}
      </div>

      {/* SECURITY FOOTER */}
      <div className="audit-security-footer">
        <ShieldCheck size={16} />

        <div>
          <strong>
            Tamper-evident audit logging
          </strong>

          <span>
            All procurement actions are recorded in a
            SHA-256 hash chain for integrity verification.
          </span>
        </div>
      </div>

    </section>
  );
}