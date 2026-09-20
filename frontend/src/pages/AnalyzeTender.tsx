import { useState } from "react";

import FileUpload from "../components/FileUpload";
import RequirementCard from "../components/RequirementCard";

import { standardsApi, pdfApi } from "../services/api";

import {
  Search,
  Sparkles,
  AlertCircle,
  FileText,
  Database,
  BrainCircuit,
  ShieldCheck,
  ArrowRight,
} from "lucide-react";

import { useNavigate } from "react-router-dom";

export default function AnalyzeTender() {

  const navigate = useNavigate();

  const [file, setFile] = useState<File | null>(null);

  const [requirement, setRequirement] = useState("");

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");


  const analyze = async () => {

    const query = requirement.trim();

    if (!file && !query) {
      setError(
        "Please upload a PDF or enter a procurement requirement."
      );
      return;
    }

    setLoading(true);
    setError("");

    try {

      let analysisQuery = query;

      /*
       * If a PDF was uploaded, extract its text first.
       */
      if (file) {

        const extracted = await pdfApi.extract(file);

        analysisQuery = extracted.text.trim();

        if (!analysisQuery) {
          throw new Error(
            "No usable text was found in the uploaded PDF."
          );
        }
      }

      /*
       * Send the extracted PDF text or
       * manually entered requirement to the
       * existing BIS RAG analysis pipeline.
       */
      const result = await standardsApi.analyze(
        analysisQuery,
        3
      );

      sessionStorage.setItem(
        "analysisResult",
        JSON.stringify(result)
      );

      navigate("/standards");

    } catch (err: any) {

      console.error(err);

      const detail = err.response?.data?.detail;

      setError(
        typeof detail === "string"
          ? detail
          : err.message ||
            "Unable to analyze the procurement requirement."
      );

    } finally {

      setLoading(false);

    }
  };


  return (
    <div className="analyze-page">

      {/* PAGE HEADER */}

      <div className="page-title analyze-page-header">

        <div>

          <span className="header-label">
            NEW ANALYSIS
          </span>

          <h2>Analyze Procurement Requirement</h2>

          <p>
            Identify applicable BIS standards from a tender document
            or a procurement requirement using AI-powered semantic analysis.
          </p>

        </div>

        <div className="analysis-header-badge">
          <Sparkles size={16} />
          <span>AI-Powered</span>
        </div>

      </div>


      {/* MAIN ANALYSIS AREA */}

      <div className="analysis-layout">

        {/* LEFT SIDE */}

        <div className="analysis-main">

          <section className="panel analysis-input-panel">

            {/* SECTION HEADER */}

            <div className="section-heading">

              <div className="section-icon">
                <Search size={20} />
              </div>

              <div>

                <span className="analysis-step-label">
                  STEP 01
                </span>

                <h3>Provide Procurement Requirement</h3>

                <p>
                  Upload a tender PDF or describe the requirement manually.
                </p>

              </div>

            </div>


            {/* PDF AREA */}

            <div className="analysis-upload-section">

              <div className="analysis-field-label">

                <div className="analysis-field-title">

                  <FileText size={17} />

                  <span>Tender Document</span>

                </div>

                <span className="analysis-optional">
                  OPTIONAL
                </span>

              </div>


              <FileUpload
                onFileSelect={(selectedFile) =>
                  setFile(selectedFile)
                }
              />

            </div>


            {/* DIVIDER */}

            <div className="or-divider">
              <span>OR ENTER MANUALLY</span>
            </div>


            {/* MANUAL REQUIREMENT */}

            <div className="analysis-manual-section">

              <div className="analysis-field-label">

                <div className="analysis-field-title">

                  <Search size={17} />

                  <span>Procurement Requirement</span>

                </div>

                <span className="analysis-required">
                  REQUIRED
                </span>

              </div>


              <textarea
                className="requirement-input"
                value={requirement}
                onChange={(e) =>
                  setRequirement(e.target.value)
                }
                placeholder="Example: We need LED street lights for a highway project..."
                rows={7}
              />

              <div className="analysis-input-hint">
                Describe the product, material, equipment, service,
                or technical requirement as clearly as possible.
              </div>

            </div>


            {/* SELECTED FILE */}

            {file && (

              <div className="info-message analysis-file-message">

                <FileText size={18} />

                <div>

                  <strong>Document ready for analysis</strong>

                  <span>
                    {file.name}
                  </span>

                  <small>
                    Tender text will be extracted automatically.
                  </small>

                </div>

              </div>

            )}


            {/* ERROR */}

            {error && (

              <div className="error-message">

                <AlertCircle size={18} />

                <span>
                  {error}
                </span>

              </div>

            )}


            {/* ANALYZE BUTTON */}

            <button
              className="primary-button analyze-button"
              onClick={analyze}
              disabled={loading}
            >

              {loading ? (
                <>
                  <span className="analysis-loading-spinner" />
                  Extracting PDF & analyzing...
                </>
              ) : (
                <>
                  <Sparkles size={19} />
                  Analyze Requirement
                  <ArrowRight size={18} />
                </>
              )}

            </button>

          </section>


          {/* WHAT HAPPENS NEXT */}

          <section className="info-panel analysis-process-panel">

            <div className="analysis-process-header">

              <div>

                <span className="analysis-step-label">
                  ANALYSIS PIPELINE
                </span>

                <h3>What happens after analysis?</h3>

              </div>

              <ShieldCheck size={22} />

            </div>


            <div className="mini-steps">

              <div className="analysis-process-step">

                <span>01</span>

                <div>
                  <strong>Requirement matching</strong>
                  <small>
                    Understand the procurement requirement
                  </small>
                </div>

              </div>


              <div className="analysis-process-step">

                <span>02</span>

                <div>
                  <strong>BIS standards retrieval</strong>
                  <small>
                    Search the BIS knowledge base
                  </small>
                </div>

              </div>


              <div className="analysis-process-step">

                <span>03</span>

                <div>
                  <strong>AI explanation</strong>
                  <small>
                    Generate evidence-based reasoning
                  </small>
                </div>

              </div>


              <div className="analysis-process-step">

                <span>04</span>

                <div>
                  <strong>Version verification</strong>
                  <small>
                    Check versions and amendments
                  </small>
                </div>

              </div>

            </div>

          </section>

        </div>


        {/* RIGHT SIDE */}

        <aside className="analysis-side">

          {/* AI ENGINE */}

          <div className="side-card analysis-engine-card">

            <div className="analysis-side-icon">
              <Sparkles size={22} />
            </div>

            <span className="analysis-side-label">
              INTELLIGENCE ENGINE
            </span>

            <h3>AI-Powered Analysis</h3>

            <p>
              The system combines semantic embeddings,
              retrieval, and local AI reasoning to identify
              relevant BIS standards from procurement requirements.
            </p>


            <div className="analysis-engine-stack">

              <div className="analysis-engine-item">

                <div className="analysis-engine-item-icon">
                  <BrainCircuit size={16} />
                </div>

                <div>
                  <strong>Semantic Embeddings</strong>
                  <span>
                    Understand requirement meaning
                  </span>
                </div>

              </div>


              <div className="analysis-engine-item">

                <div className="analysis-engine-item-icon">
                  <Database size={16} />
                </div>

                <div>
                  <strong>BIS Knowledge Base</strong>
                  <span>
                    Retrieve relevant standards
                  </span>
                </div>

              </div>


              <div className="analysis-engine-item">

                <div className="analysis-engine-item-icon">
                  <Sparkles size={16} />
                </div>

                <div>
                  <strong>AI Reasoning</strong>
                  <span>
                    Explain recommendations
                  </span>
                </div>

              </div>

            </div>

          </div>


          {/* VERIFICATION NOTE */}

          <div className="side-card analysis-important-card">

            <div className="analysis-important-heading">

              <ShieldCheck size={19} />

              <h3>Officer Verification</h3>

            </div>

            <p>
              AI recommendations are intended to assist the
              procurement officer. Final decisions should be
              verified against official BIS records before approval.
            </p>

            <div className="analysis-verification-status">

              <span className="analysis-status-dot" />

              <span>
                Human-in-the-loop verification
              </span>

            </div>

          </div>


          {/* FLOW SUMMARY */}

          <div className="analysis-flow-card">

            <span className="analysis-side-label">
              WORKFLOW
            </span>

            <div className="analysis-flow">

              <span>Tender</span>

              <ArrowRight size={14} />

              <span>RAG</span>

              <ArrowRight size={14} />

              <span>BIS Standards</span>

            </div>

          </div>

        </aside>

      </div>


      {/* REQUIREMENT PREVIEW */}

      {requirement && (
        <RequirementCard requirement={requirement} />
      )}

    </div>
  );
}