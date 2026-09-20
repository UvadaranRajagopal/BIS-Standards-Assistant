import {
  FileSearch,
  Database,
  ShieldCheck,
  FileText,
  ArrowRight,
  Activity,
  BrainCircuit,
  CheckCircle2,
  Clock3,
  GitBranch,
  Sparkles,
  LockKeyhole,
  ExternalLink,
} from "lucide-react";

import { Link } from "react-router-dom";

export default function Dashboard() {
  return (
    <div className="dashboard-home">

      {/* HERO */}
      <section className="dashboard-hero">

        <div className="hero-copy">
          <span className="header-label">PROCUREMENT INTELLIGENCE</span>

          <h2>
            Smarter standards.
            <br />
            <span>Better procurement decisions.</span>
          </h2>

          <p>
            Analyze procurement requirements, retrieve relevant BIS standards,
            verify certification requirements and maintain a transparent
            audit trail — all from one intelligence workspace.
          </p>

          <div className="hero-actions">

            <Link to="/analyze" className="dashboard-primary-action">
              <FileSearch size={18} />
              Analyze New Tender
              <ArrowRight size={17} />
            </Link>

            <Link to="/standards" className="dashboard-secondary-action">
              View Standards Analysis
            </Link>

          </div>
        </div>

        {/* AI ENGINE VISUAL */}
        <div className="hero-engine">

          <div className="engine-glow"></div>

          <div className="engine-core">
            <BrainCircuit size={38} />
          </div>

          <div className="engine-ring ring-one"></div>
          <div className="engine-ring ring-two"></div>

          <div className="engine-label">
            <strong>AI ENGINE</strong>
            <span>RAG ACTIVE</span>
          </div>

        </div>

      </section>


      {/* KPI ROW */}
      <section className="dashboard-kpis">

        <div className="dashboard-kpi kpi-blue">

          <div className="kpi-icon">
            <Database size={21} />
          </div>

          <div className="kpi-content">
            <span>Knowledge Base</span>
            <strong>60</strong>
            <small>BIS standards indexed</small>
          </div>

          <span className="kpi-status">
            <CheckCircle2 size={13} />
            Ready
          </span>

        </div>


        <div className="dashboard-kpi kpi-purple">

          <div className="kpi-icon">
            <BrainCircuit size={21} />
          </div>

          <div className="kpi-content">
            <span>RAG Engine</span>
            <strong>ACTIVE</strong>
            <small>Semantic retrieval enabled</small>
          </div>

          <span className="kpi-status">
            <Activity size={13} />
            Online
          </span>

        </div>


        <div className="dashboard-kpi kpi-green">

          <div className="kpi-icon">
            <ShieldCheck size={21} />
          </div>

          <div className="kpi-content">
            <span>Audit Integrity</span>
            <strong>VALID</strong>
            <small>SHA-256 hash chain</small>
          </div>

          <span className="kpi-status">
            <CheckCircle2 size={13} />
            Secure
          </span>

        </div>


        <div className="dashboard-kpi kpi-orange">

          <div className="kpi-icon">
            <Sparkles size={21} />
          </div>

          <div className="kpi-content">
            <span>AI Model</span>
            <strong>Llama 3.2</strong>
            <small>Local inference via Ollama</small>
          </div>

          <span className="kpi-status">
            <LockKeyhole size={13} />
            Local
          </span>

        </div>

      </section>


      {/* MAIN DASHBOARD GRID */}
      <section className="dashboard-main-grid">

        {/* PROCUREMENT PIPELINE */}
        <div className="pipeline-panel">

          <div className="dashboard-section-header">

            <div>
              <span className="dashboard-section-label">
                INTELLIGENCE PIPELINE
              </span>

              <h3>How BIS Assistant works</h3>

              <p>
                From procurement requirement to verified standards.
              </p>
            </div>

            <div className="pipeline-live">
              <span></span>
              Engine Ready
            </div>

          </div>


          <div className="intelligence-pipeline">

            <div className="pipeline-step active-step">

              <div className="pipeline-number">01</div>

              <div className="pipeline-icon">
                <FileText size={20} />
              </div>

              <div className="pipeline-content">
                <strong>Requirement</strong>
                <span>Upload tender PDF</span>
              </div>

              <CheckCircle2 size={17} className="pipeline-check" />

            </div>


            <div className="pipeline-connector"></div>


            <div className="pipeline-step active-step">

              <div className="pipeline-number">02</div>

              <div className="pipeline-icon">
                <BrainCircuit size={20} />
              </div>

              <div className="pipeline-content">
                <strong>Understand</strong>
                <span>Semantic requirement matching</span>
              </div>

              <CheckCircle2 size={17} className="pipeline-check" />

            </div>


            <div className="pipeline-connector"></div>


            <div className="pipeline-step active-step">

              <div className="pipeline-number">03</div>

              <div className="pipeline-icon">
                <Database size={20} />
              </div>

              <div className="pipeline-content">
                <strong>Retrieve</strong>
                <span>BIS standards from knowledge base</span>
              </div>

              <CheckCircle2 size={17} className="pipeline-check" />

            </div>


            <div className="pipeline-connector"></div>


            <div className="pipeline-step">

              <div className="pipeline-number">04</div>

              <div className="pipeline-icon">
                <ShieldCheck size={20} />
              </div>

              <div className="pipeline-content">
                <strong>Verify</strong>
                <span>Officer review & audit recording</span>
              </div>

              <ArrowRight size={17} className="pipeline-arrow" />

            </div>

          </div>

        </div>


        {/* SYSTEM HEALTH */}
        <div className="system-health-panel">

          <div className="dashboard-section-header">

            <div>
              <span className="dashboard-section-label">
                SYSTEM HEALTH
              </span>

              <h3>Platform status</h3>

            </div>

            <Activity size={19} />

          </div>


          <div className="health-score">

            <div className="health-circle">
              <div>
                <strong>100%</strong>
                <span>Operational</span>
              </div>
            </div>

            <div className="health-summary">
              <strong>All core services ready</strong>
              <p>
                The intelligence pipeline is available for procurement analysis.
              </p>
            </div>

          </div>


          <div className="health-items">

            <div>
              <span className="health-dot green"></span>
              <span>Document extraction</span>
              <strong>Ready</strong>
            </div>

            <div>
              <span className="health-dot blue"></span>
              <span>Semantic retrieval</span>
              <strong>Active</strong>
            </div>

            <div>
              <span className="health-dot purple"></span>
              <span>Local AI inference</span>
              <strong>Active</strong>
            </div>

            <div>
              <span className="health-dot orange"></span>
              <span>Audit verification</span>
              <strong>Valid</strong>
            </div>

          </div>

        </div>

      </section>


      {/* LOWER SECTION */}
      <section className="dashboard-lower-grid">

        {/* QUICK ACTIONS */}
        <div className="quick-actions-panel">

          <div className="dashboard-section-header">

            <div>
              <span className="dashboard-section-label">
                QUICK ACTIONS
              </span>

              <h3>Procurement workspace</h3>

            </div>

          </div>


          <div className="quick-action-grid">

            <Link to="/analyze" className="quick-action blue-action">

              <div className="quick-action-icon">
                <FileSearch size={20} />
              </div>

              <div>
                <strong>Analyze Tender</strong>
                <span>Start a new procurement analysis</span>
              </div>

              <ArrowRight size={16} />

            </Link>


            <Link to="/standards" className="quick-action purple-action">

              <div className="quick-action-icon">
                <Database size={20} />
              </div>

              <div>
                <strong>Review Standards</strong>
                <span>Inspect AI recommendations</span>
              </div>

              <ArrowRight size={16} />

            </Link>


            <Link to="/audit" className="quick-action green-action">

              <div className="quick-action-icon">
                <ShieldCheck size={20} />
              </div>

              <div>
                <strong>Audit Trail</strong>
                <span>Verify procurement activity</span>
              </div>

              <ArrowRight size={16} />

            </Link>


            <a
              href="https://standards.bis.gov.in/website/know-your-standards"
              target="_blank"
              rel="noopener noreferrer"
              className="quick-action orange-action"
            >

              <div className="quick-action-icon">
                <ExternalLink size={20} />
              </div>

              <div>
                <strong>BIS Portal</strong>
                <span>Verify standards officially</span>
              </div>

              <ArrowRight size={16} />

            </a>

          </div>

        </div>


        {/* PLATFORM CAPABILITIES */}
        <div className="capabilities-panel">

          <div className="dashboard-section-header">

            <div>
              <span className="dashboard-section-label">
                CORE CAPABILITIES
              </span>

              <h3>Built for accountable AI</h3>

            </div>

            <GitBranch size={19} />

          </div>


          <div className="capability-list">

            <div className="capability-item">
              <div className="capability-badge blue-badge">
                <BrainCircuit size={16} />
              </div>

              <div>
                <strong>Evidence-grounded AI</strong>
                <span>Recommendations are based on retrieved BIS evidence.</span>
              </div>
            </div>


            <div className="capability-item">
              <div className="capability-badge green-badge">
                <ShieldCheck size={16} />
              </div>

              <div>
                <strong>Human verification</strong>
                <span>Officer retains the final verification authority.</span>
              </div>
            </div>


            <div className="capability-item">
              <div className="capability-badge purple-badge">
                <LockKeyhole size={16} />
              </div>

              <div>
                <strong>Local AI processing</strong>
                <span>Inference runs locally through Ollama.</span>
              </div>
            </div>

          </div>

        </div>

      </section>


      {/* FOOTER STATUS STRIP */}
      <section className="dashboard-status-strip">

        <div>
          <span className="status-pulse"></span>
          <strong>System Online</strong>
          <span>All intelligence services operational</span>
        </div>

        <div className="status-divider"></div>

        <div>
          <Clock3 size={15} />
          <span>Ready for new procurement analysis</span>
        </div>

        <div className="status-model">
          <BrainCircuit size={15} />
          Llama 3.2 · Local inference
        </div>

      </section>

    </div>
  );
}