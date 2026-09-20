import AuditTrail from "../components/AuditTrail";

export default function AuditPage() {

  return (

    <div>

      <div className="page-title">

        <div>

          <span className="header-label">
            SECURITY & COMPLIANCE
          </span>

          <h2>Audit Trail</h2>

          <p>
            Review procurement actions and verify the integrity
            of the tamper-evident audit chain.
          </p>

        </div>

      </div>

      <AuditTrail />

    </div>

  );
}