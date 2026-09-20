import { Bell, UserCircle } from "lucide-react";

export default function Header() {
  return (
    <header className="top-header">

      <div>
        <span className="header-label">
          GOVERNMENT PROCUREMENT
        </span>

        <h1>BIS Standards Assistant</h1>
      </div>

      <div className="header-actions">

        <button className="icon-button">
          <Bell size={20} />
        </button>

        <div className="officer">

          <UserCircle size={34} />

          <div>
            <strong>Procurement Officer</strong>
            <small>OFFICER_001</small>
          </div>

        </div>

      </div>

    </header>
  );
}