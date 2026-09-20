import {
  LayoutDashboard,
  FileSearch,
  BookOpen,
  ShieldCheck,
} from "lucide-react";

import { NavLink } from "react-router-dom";

export default function Sidebar() {
  return (
    <aside className="sidebar">

      <div className="brand">

        <div className="brand-icon">
          <ShieldCheck size={28} />
        </div>

        <div>
          <h2>BIS Assistant</h2>
          <span>Procurement Intelligence</span>
        </div>

      </div>

      <nav>

        <NavLink to="/" end>
          <LayoutDashboard size={19} />
          Dashboard
        </NavLink>

        <NavLink to="/analyze">
          <FileSearch size={19} />
          Analyze Tender
        </NavLink>

        <NavLink to="/standards">
          <BookOpen size={19} />
          Standards Analysis
        </NavLink>

        <NavLink to="/audit">
          <ShieldCheck size={19} />
          Audit Trail
        </NavLink>

      </nav>

      <div className="sidebar-bottom">

        <div className="system-status">
          <span className="status-dot"></span>

          <div>
            <strong>System Online</strong>
            <small>RAG Engine Active</small>
          </div>
        </div>

        <small className="model-info">
          Model: Llama 3.2
        </small>

      </div>

    </aside>
  );
}