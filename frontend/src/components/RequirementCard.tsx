import { FileSearch } from "lucide-react";

interface Props {
  requirement: string;
}

export default function RequirementCard({
  requirement,
}: Props) {
  return (
    <div className="requirement-card">

      <div className="section-heading">

        <div className="section-icon">
          <FileSearch size={20} />
        </div>

        <div>
          <h3>Detected Requirement</h3>
          <p>
            Requirement extracted from procurement input
          </p>
        </div>

      </div>

      <div className="requirement-text">
        {requirement}
      </div>

    </div>
  );
}