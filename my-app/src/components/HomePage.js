import React, { useEffect, useState, useRef } from "react";
import { Scale, Github, Loader2, Mail, FileText as ResumeIcon, ArrowRight, Menu } from "lucide-react";
import ThemeToggle from "./ThemeToggle";

const tabs = [
  "About",
  "Features",
  "Use Cases",
  "Why LegalDoc",
  "Tech Stack",
  "FAQs",
];

const MAKERS = [
  {
    github: "https://github.com/Chai-B/Chai-B",
    api: "https://api.github.com/users/Chai-B",
    name: "Chaitanya Bansal",
    bio: "Final year engineering student exploring AI/ML. Currently working on Legal Doc Interpretator. Learning LLM, LangChain, FastAPI, Streamlit.",
    contact: "bansalchaitanya1234@gmail.com",
    resume: "https://github.com/Chai-B/Chai-B/blob/main/resume.pdf",
    projects: "https://github.com/Chai-B?tab=repositories"
  },
  {
    github: "https://github.com/madhurya-ops/madhurya-ops",
    api: "https://api.github.com/users/madhurya-ops",
    name: "Madhurya Mishra",
    bio: "Final year engineering student exploring AI/ML. Currently working on Legal Doc Interpreter. Learning LangChain, LLM, FastAPI, React.",
    contact: "madhuryamishra@gmail.com",
    resume: "https://github.com/madhurya-ops/Madhurya_Mishra/blob/main/Madhurya_Mishra_Resume.pdf",
    projects: "https://github.com/madhurya-ops?tab=repositories"
  }
];

export default function HomePage({ onGetStarted }) {
  const [activeTab, setActiveTab] = useState("About");
  const [profiles, setProfiles] = useState([null, null]);
  const [loading, setLoading] = useState(true);
  const [menuOpen, setMenuOpen] = useState(false);
  const tabBoxRef = useRef(null);

  useEffect(() => {
    Promise.all(MAKERS.map(m => fetch(m.api).then(res => res.json()))).then(setProfiles).finally(() => setLoading(false));
  }, []);

  // Helper to scroll tab content into view
  const scrollTabBoxIntoView = () => {
    if (tabBoxRef.current) {
      tabBoxRef.current.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  };

  // Scroll to tab content when Learn More is clicked
  const handleLearnMore = () => {
    if (tabBoxRef.current) {
      tabBoxRef.current.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 dark:bg-slate-900 bg-dots relative overflow-hidden transition-colors duration-300 font-sans">
      {/* Header with centered logo and hamburger menu */}
      <header className="fixed left-0 top-0 w-full z-50 flex items-center justify-between px-2 sm:px-4 md:px-16 py-3 sm:py-4 bg-white/90 dark:bg-slate-900/90 backdrop-blur-lg shadow-2xl border border-slate-200/60 dark:border-slate-700/60 rounded-b-2xl">
        {/* Hamburger menu */}
        <div className="relative flex items-center">
          <button
            className="flex items-center justify-center p-2 rounded-lg hover:bg-blue-50 dark:hover:bg-blue-900/40 focus:outline-none focus:ring-2 focus:ring-blue-400"
            onClick={() => setMenuOpen((open) => !open)}
            aria-label="Open menu"
            type="button"
          >
            <Menu className="w-7 h-7 text-blue-600 dark:text-blue-400" />
          </button>
          {/* Dropdown menu */}
          {menuOpen && (
            <div className="absolute left-0 top-12 w-48 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl shadow-lg py-2 flex flex-col animate-fade-in-up">
              {tabs.map((tab) => (
                <button
                  key={tab}
                  onClick={() => { setActiveTab(tab); setMenuOpen(false); setTimeout(scrollTabBoxIntoView, 50); }}
                  className={`text-left px-5 py-2 text-base font-medium transition-colors duration-200 hover:bg-blue-50 dark:hover:bg-blue-800/40 text-slate-800 dark:text-slate-200 ${activeTab === tab ? "bg-blue-100 dark:bg-blue-900/40 font-semibold" : ""}`}
                >
                  {tab}
                </button>
              ))}
            </div>
          )}
        </div>
        {/* Centered logo */}
        <div className="flex-1 flex justify-center">
          <button
            className="flex items-center gap-3 focus:outline-none"
            onClick={() => { setActiveTab('About'); setTimeout(scrollTabBoxIntoView, 50); }}
            title="About LegalDoc"
            aria-label="About LegalDoc"
            tabIndex={-1}
          >
            <Scale className="w-8 h-8 text-blue-600 dark:text-blue-400" />
            <span className="text-2xl font-bold text-slate-900 dark:text-slate-100">LegalDoc</span>
          </button>
        </div>
        {/* Right side controls */}
        <div className="flex items-center gap-2">
          <ThemeToggle />
          <a
            href="https://github.com/madhurya-ops/Legal-Document-Parser"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-4 py-2 rounded-xl border border-blue-600 dark:border-blue-400 text-blue-700 dark:text-blue-300 font-semibold bg-white/90 dark:bg-slate-900/90 hover:bg-blue-50 dark:hover:bg-blue-800/40 transition-all duration-300 shadow-md text-base"
          >
            <Github className="w-5 h-5" /> GitHub
          </a>
        </div>
      </header>

      {/* Minimal Landing Section */}
      <main className="flex flex-1 flex-col items-center justify-center text-center px-4 mt-40 mb-12">
        <h1 className="text-4xl sm:text-5xl font-extrabold text-blue-700 dark:text-blue-300 mb-6 tracking-tight">AI-Powered Legal Document Interpreter</h1>
        <div className="space-y-4 max-w-2xl mx-auto">
          <p className="text-lg sm:text-xl text-slate-700 dark:text-slate-300">Upload, parse, and understand your legal documents instantly with AI.</p>
          <p className="text-lg sm:text-xl text-slate-700 dark:text-slate-300">Extract obligations, penalties, dates, and clear summaries in plain English.</p>
          <p className="text-lg sm:text-xl text-slate-700 dark:text-slate-300">Built for legal professionals, startups, and anyone dealing with contracts.</p>
        </div>
        <button
          className="mt-8 px-8 py-3 rounded-xl bg-blue-600 text-white font-semibold text-lg shadow-lg transition-all duration-300 hover:bg-blue-700 hover:scale-105 focus:outline-none focus:ring-2 focus:ring-blue-400"
          onClick={handleLearnMore}
        >
          Learn More
        </button>
      </main>

      {/* Tab Content */}
      <div ref={tabBoxRef} className="max-w-5xl mx-auto px-2 sm:px-4 md:px-0 pb-10 sm:pb-16">
        <div className="rounded-3xl bg-white/90 dark:bg-slate-900/90 backdrop-blur-lg shadow-2xl border border-slate-200/60 dark:border-slate-700/60 p-4 sm:p-8 md:p-12 space-y-6 sm:space-y-8">
          {activeTab === "About" && (
            <section>
              <h2 className="text-2xl font-extrabold text-slate-900 dark:text-slate-100 mb-2 tracking-tight">About <span className="text-blue-700 dark:text-blue-400">LegalDoc Parser</span></h2>
              <p className="text-lg font-medium text-slate-900 dark:text-slate-100 mb-3">LegalDoc Parser is a powerful AI-driven platform designed to automate and streamline the extraction of critical information from complex legal documents—contracts, agreements, policies, and more. Built for legal teams, enterprises, and compliance professionals, the parser eliminates manual review, alleviating bottlenecks, reducing errors, and accelerating informed decision-making.</p>
              <ul className="list-disc pl-6 space-y-2 mb-3">
                <li><b>Seamless document ingestion:</b> Upload PDFs, DOCX files, plain text, or scanned documents (with OCR) via a user-friendly interface or API. Bulk upload capabilities support high-volume processing.</li>
                <li><b>AI-powered extraction engine:</b> Leveraging advanced NLP techniques and transformer-based models, our parser identifies core legal elements—parties, effective dates, obligations, clauses, liabilities, renewal terms, and more—converting them into clean, standardized formats.</li>
                <li><b>User-centric design:</b> After upload, documents are processed quickly and returned with structured outputs (JSON, CSV) accompanied by confidence scores and traceable metadata. Users can review or override entries before exporting.</li>
                <li><b>Security and compliance:</b> With encryption in transit and at rest, role-based access roles, and audit logging, the platform can be deployed in cloud or on-premises environments to meet enterprise-grade compliance requirements.</li>
                <li><b>Scalable and future-proof:</b> Built on a modular and extensible architecture, the platform supports continuous model updates, jurisdiction-specific clause recognition, and custom model fine-tuning for specialized needs.</li>
              </ul>
              <p className="text-lg font-medium text-slate-900 dark:text-slate-100">LegalDoc Parser empowers users to shift focus from manual data extraction to strategic thinking. By transforming legal text into structured intelligence and delivering it via an intuitive dashboard or API, the platform supports faster negotiations, better compliance oversight, and more efficient contract workflows—all within a secure, scalable framework.</p>
            </section>
          )}
          {activeTab === "Features" && (
            <section>
              <h2 className="text-2xl font-extrabold text-slate-900 dark:text-slate-100 mb-2 tracking-tight"><span className="text-blue-700 dark:text-blue-400">Features</span></h2>
              <ol className="list-decimal pl-6 space-y-2 text-base text-slate-700 dark:text-slate-300">
                <li><b>AI-Powered Extraction:</b> Combines transformer-based NLP with rule-based logic to accurately detect and extract standard and specialized legal elements—such as parties, dates, definitions, clauses, obligations, and monetary terms.</li>
                <li><b>Format-Agnostic Input:</b> Supports PDFs, Word documents, plaintext, and scanned files (OCR included), preserving original formatting like headers, footnotes, tables, and multi-page content.</li>
                <li><b>Custom Clause Detection:</b> Define your own clause patterns or keywords via the UI. Upload example documents to train custom models. Flag high-priority clauses like indemnity, non-compete, ESG, or audit clauses.</li>
                <li><b>Structured, Traceable Outputs:</b> Export results in JSON or CSV formats, each element tagged with metadata: source location, confidence level, and extraction type. This ensures full traceability and auditability.</li>
                <li><b>Confidence Scoring & Metadata:</b> All extractions include confidence indicators and references to source text, location, and confidence score, enabling quick verification and manual review when needed.</li>
                <li><b>Bulk Processing & Automation:</b> Handle large document volumes efficiently. Upload files in batches, process asynchronously, and integrate with downstream systems via webhooks and API.</li>
                <li><b>API-First Architecture:</b> All operations—uploading, parsing, status checking, and data retrieval—are available via REST endpoints, enabling integration with CLM systems, BI platforms, or internal apps.</li>
                <li><b>Comparative Analysis:</b> Built-in comparison tool identifies changes between document versions at clause or sentence level. Visual diffs make version review clear and efficient.</li>
                <li><b>Security & Compliance:</b> Deploy securely in cloud or on-premises. Role-based access control, end-to-end encryption, and audit trails meet enterprise compliance standards.</li>
                <li><b>Scalable Infrastructure:</b> Powered by Kubernetes and containerized services, with auto-scaling capacity. Designed to support high-volume processing without manual intervention.</li>
                <li><b>Monitoring & Auditing:</b> Dashboard includes logging of user activity and extraction history. Tools help identify failed jobs, bottlenecks, or exceptions flagged during parsing.</li>
                <li><b>Continuous Improvement:</b> Monthly model updates and regular release cycles. Users receive transparency with model versioning and changelogs.</li>
              </ol>
            </section>
          )}
          {activeTab === "Use Cases" && (
            <section>
              <h2 className="text-2xl font-extrabold text-slate-900 dark:text-slate-100 mb-2 tracking-tight"><span className="text-blue-700 dark:text-blue-400">Use Cases</span></h2>
              <ol className="list-decimal pl-6 space-y-2 text-base text-slate-700 dark:text-slate-300 mb-4">
                <li><b>Law Firms & Legal Consultancies:</b> Fast, accurate review of contracts (NDAs, SLAs, licensing agreements). Bulk upload contracts → AI extracts parties, obligations, dates → attorneys review confidence-scored outputs → structured summaries feed case management systems. <i>Benefit:</i> Rapid delivery of insights, improved consistency, and time savings.</li>
                <li><b>In-House Legal & Compliance Teams:</b> Tracking vendor obligations, compliance deadlines, and regulatory clauses. Ingest existing agreements → auto-extract key terms and deadlines → populate compliance trackers and generate alerts. <i>Benefit:</i> Proactive oversight, fewer breaches, and better regulatory alignment.</li>
                <li><b>SMEs & Startups:</b> Lacking full-time legal staff to monitor contracts and renewal terms. Upload contracts and agreements → parser pulls renewal dates, obligations, liabilities → dashboard highlights upcoming actions. <i>Benefit:</i> Reduced legal risk and increased operational efficiency without hiring overhead.</li>
                <li><b>Enterprises & Contract Operations:</b> Managing thousands of contracts across departments manually. Automated bulk parsing pipelines feed structured data into CLM or ERP systems, while diff tools highlight changes in contract versions. <i>Benefit:</i> Centralized data visibility, audit-ready workflows, and scalable document processing.</li>
                <li><b>Specialized Domains:</b> Regulatory & Finance: Capture loan covenant specifics, compliance milestones. IP & Licensing: Extract royalty structures, territory provisions, royalty models. Real Estate & M&A: Track rent escalations, maintenance responsibilities, and potential liability across documents. <i>Benefit:</i> Deep domain insights with minimal manual effort.</li>
              </ol>
              <p className="text-base text-slate-900 dark:text-slate-100">In every scenario, LegalDoc Parser translates unstructured legal text into actionable data—streamlining workflows, improving oversight, enabling better decision-making, and ensuring auditability.</p>
            </section>
          )}
          {activeTab === "Why LegalDoc" && (
            <section>
              <h2 className="text-2xl font-extrabold text-slate-900 dark:text-slate-100 mb-2 tracking-tight">Why Choose <span className="text-blue-700 dark:text-blue-400">LegalDoc Parser?</span></h2>
              <ol className="list-decimal pl-6 space-y-2 text-base text-slate-700 dark:text-slate-300">
                <li><b>Legal-Centric Accuracy:</b> Models trained on real-world legal documents ensure high precision and relevance—rarely misclassifying clauses or entities.</li>
                <li><b>Full Traceability:</b> Every data point extracted is linked back to its source text, location, and confidence score, ensuring transparency and accountability.</li>
                <li><b>Customizable Clause Logic:</b> The clause-definition framework empowers users to train models on proprietary or niche legal vocabularies—supporting internal policies and domain-specific language.</li>
                <li><b>Security Tailored for Enterprise:</b> Role-based access control, encryption in transit and at rest, and secure deployment options meet rigorous security standards.</li>
                <li><b>Seamless Integration:</b> An API-first design enables plug-and-play connectivity with contract management systems, BI dashboards, and legal workflow tools.</li>
                <li><b>Scalable Architecture:</b> Containerized microservices enable elastic scaling, supporting both small business and enterprise volumes without loss of performance.</li>
                <li><b>User-Friendly Interface:</b> Clean, intuitive dashboard enables non-technical users to parse and review documents effectively, with minimal onboarding.</li>
                <li><b>Designed for Global Context:</b> Supports jurisdiction-specific expressions and provisions, multilingual capabilities, and compliance with international legal norms.</li>
                <li><b>Continuous Advancement:</b> Regular model updates, feature releases, and transparent version notes mean the system evolves alongside legal standards.</li>
                <li><b>Built for Governance:</b> With audit logging, version comparison, and user activity tracking, LegalDoc aligns with corporate governance and audit requirements.</li>
                <li><b>Recognized by Lean and Legal Teams:</b> The platform empowers both paralegals and legal departments to drive better outcomes—shortening review cycles, reducing risk, and enabling data-driven contract insights.</li>
              </ol>
            </section>
          )}
          {activeTab === "Tech Stack" && (
            <section>
              <h2 className="text-2xl font-extrabold text-slate-900 dark:text-slate-100 mb-2 tracking-tight"><span className="text-blue-700 dark:text-blue-400">Technology Stack</span></h2>
              <div className="mb-4">
                <h3 className="text-lg font-bold text-slate-900 dark:text-slate-100 mb-1">Backend</h3>
                <ul className="list-disc pl-6 space-y-1 text-base text-slate-700 dark:text-slate-300">
                  <li>FastAPI (Python): High-performance REST API with async endpoints</li>
                  <li>PyTorch + Hugging Face Transformers: Core NLP for entity and clause extraction</li>
                  <li>spaCy + Prodigy: Annotation and rule-based entity matching</li>
                  <li>PDFPlumber / PyMuPDF + Tesseract OCR: Robust text extraction from varied document types</li>
                  <li>Celery + Redis: Asynchronous task job management</li>
                  <li>PostgreSQL: Secure storage for parsed data, metadata, and logs</li>
                  <li>Elasticsearch: Full-text search capabilities for extracted content</li>
                </ul>
              </div>
              <div className="mb-4">
                <h3 className="text-lg font-bold text-slate-900 dark:text-slate-100 mb-1">Frontend</h3>
                <ul className="list-disc pl-6 space-y-1 text-base text-slate-700 dark:text-slate-300">
                  <li>React.js + TypeScript: Interactive UI for document upload, parsing review, and comparisons</li>
                  <li>Tailwind CSS: Clean, modern styling and responsive layouts</li>
                </ul>
              </div>
              <div className="mb-4">
                <h3 className="text-lg font-bold text-slate-900 dark:text-slate-100 mb-1">API & Integrations</h3>
                <ul className="list-disc pl-6 space-y-1 text-base text-slate-700 dark:text-slate-300">
                  <li>OpenAPI-compliant REST endpoints</li>
                  <li>Webhooks & client libraries for integration with external systems (Node.js, Python, Java)</li>
                </ul>
              </div>
              <div className="mb-4">
                <h3 className="text-lg font-bold text-slate-900 dark:text-slate-100 mb-1">Infrastructure & DevOps</h3>
                <ul className="list-disc pl-6 space-y-1 text-base text-slate-700 dark:text-slate-300">
                  <li>Docker + Kubernetes: Container orchestration with auto-scaling</li>
                  <li>AWS / GCP / Azure: Cloud infrastructure support</li>
                  <li>CI/CD pipelines: Automated testing and deployment via GitHub Actions or Jenkins</li>
                  <li>Monitoring tools: Prometheus, Grafana, Sentry, ELK stack for logs and error tracking</li>
                </ul>
              </div>
              <div className="mb-4">
                <h3 className="text-lg font-bold text-slate-900 dark:text-slate-100 mb-1">Security</h3>
                <ul className="list-disc pl-6 space-y-1 text-base text-slate-700 dark:text-slate-300">
                  <li>OAuth 2.0 / OpenID Connect: Enterprise authentication (Okta, Azure AD)</li>
                  <li>RBAC & audit logs: Ensuring compliance and accountability</li>
                  <li>Encryption: TLS for transport and AES-256 for data at rest</li>
                </ul>
              </div>
              <div className="mb-4">
                <h3 className="text-lg font-bold text-slate-900 dark:text-slate-100 mb-1">Model Management (MLOps)</h3>
                <ul className="list-disc pl-6 space-y-1 text-base text-slate-700 dark:text-slate-300">
                  <li>MLflow: Versioned model lifecycle and performance monitoring</li>
                  <li>Annotation pipelines: Continuous model refinement with client feedback</li>
                </ul>
              </div>
              <div className="mb-4">
                <h3 className="text-lg font-bold text-slate-900 dark:text-slate-100 mb-1">Exports & Reporting</h3>
                <ul className="list-disc pl-6 space-y-1 text-base text-slate-700 dark:text-slate-300">
                  <li>JSON / CSV exports, SFTP integrations, and BI connectors (Tableau, Power BI, Snowflake)</li>
                </ul>
              </div>
              <p className="text-base text-slate-900 dark:text-slate-100">This full-stack ecosystem powers LegalDoc Parser to deliver reliability, agility, and compliance at every scale.</p>
            </section>
          )}
          {activeTab === "FAQs" && (
            <section>
              <h2 className="text-2xl font-extrabold text-slate-900 dark:text-slate-100 mb-2 tracking-tight"><span className="text-blue-700 dark:text-blue-400">Frequently Asked Questions</span></h2>
              <ul className="list-disc pl-6 space-y-2 text-base text-slate-700 dark:text-slate-300">
                <li><b>Which document formats do you support?</b> We support PDFs, Word (DOC/DOCX), plain text (TXT), and scanned documents via embedded OCR. All textual content—including tables, footnotes, and sidebar notes—is extracted and processed.</li>
                <li><b>How accurate is the parser?</b> Our AI models, trained on real legal documents and fine-tuned via rule-based logic, regularly achieve over 90% precision and recall for standard clauses. Confidence indicators accompany every output, and user reviews further improve accuracy via feedback loops.</li>
                <li><b>Can I customize clause extraction?</b> Yes. Use our UI to define clause patterns via keywords or regex, label training samples, and trigger custom model training. This ensures LegalDoc fits your company's unique legal vocabulary and requirements.</li>
                <li><b>What about data security?</b> We support secure deployments (cloud or on-premises) with encryption at rest/in transit, role-based access, OAuth 2.0 authentication, and full audit trails. Designed for compliance with enterprise data standards.</li>
                <li><b>How does integration work?</b> All functionality is accessible via OpenAPI-compliant REST endpoints. Use webhooks for job completion triggers. Client SDKs (Python, Node.js, Java) make it easy to embed parser logic into contract management, ERP, or analytics tools.</li>
                <li><b>Is technical expertise needed?</b> No. The intuitive dashboard allows anyone to upload, parse, and export documents without coding.</li>
                <li><b>Can I scale document processing?</b> Absolutely. Container-based orchestration automatically scales to handle high document volumes. Administrators can monitor throughput, queue depth, and system performance in real time.</li>
                <li><b>What languages and jurisdictions are covered?</b> English contracts (U.S., UK, Commonwealth) are fully supported.</li>
              </ul>
            </section>
          )}
        </div>
      </div>

      {/* About the Makers Section */}
      <div className="max-w-5xl mx-auto px-2 sm:px-4 md:px-0 py-3 sm:py-5 animate-fade-in-up">
        <div className="rounded-3xl bg-white/90 dark:bg-slate-900/90 backdrop-blur-lg shadow-2xl p-4 sm:p-8 md:p-12">
          <h3 className="text-2xl font-extrabold text-slate-900 dark:text-slate-100 mb-8 text-center tracking-tight">
            About the <span className="text-blue-700 dark:text-blue-400">Makers</span>
          </h3>
          {loading ? (
            <div className="flex items-center gap-2 text-slate-700 dark:text-slate-300 justify-center"><Loader2 className="animate-spin w-5 h-5" /> Loading profiles...</div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 sm:gap-8 animate-fade-in-up">
              {MAKERS.map((maker, i) => (
                <div
                  key={maker.github}
                  className="flex flex-col items-center bg-white/80 dark:bg-slate-800/80 rounded-2xl shadow-xl p-7 sm:p-8 transition-all duration-300 border border-transparent hover:shadow-2xl hover:scale-[1.03] hover:border-slate-200 dark:hover:border-slate-600 group animate-fade-in-up"
                  style={{ animationDelay: `${i * 0.08 + 0.1}s` }}
                >
                  <img
                    src={profiles[i]?.avatar_url || "https://avatars.githubusercontent.com/u/9919?v=4"}
                    alt="GitHub Avatar"
                    className="w-24 h-24 rounded-full shadow-lg mb-4 border-4 border-white dark:border-slate-900 group-hover:border-slate-200 dark:group-hover:border-slate-600 transition-all duration-300"
                  />
                  <span className="text-xl font-bold text-slate-900 dark:text-slate-100 mb-1 text-center">{profiles[i]?.name || maker.name}</span>
                  <span className="text-base font-medium text-slate-700 dark:text-slate-300 mb-3 text-center">{maker.bio}</span>
                  <div className="flex flex-wrap justify-center gap-2 text-sm text-slate-700 dark:text-slate-300 mb-2 mt-2">
                    <a href={maker.github} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 font-semibold hover:bg-blue-100 dark:hover:bg-blue-800/50 transition-colors duration-200 shadow-sm">
                      <Github className="w-4 h-4" /> GitHub
                    </a>
                    <a href={maker.projects} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-100 dark:bg-slate-800/40 text-slate-700 dark:text-slate-200 font-semibold hover:bg-slate-200 dark:hover:bg-slate-700/60 transition-colors duration-200 shadow-sm">
                      <ResumeIcon className="w-4 h-4" /> Projects
                    </a>
                    <a href={maker.resume} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-100 dark:bg-slate-800/40 text-slate-700 dark:text-slate-200 font-semibold hover:bg-slate-200 dark:hover:bg-slate-700/60 transition-colors duration-200 shadow-sm">
                      <ResumeIcon className="w-4 h-4" /> Resume
                    </a>
                    <a href={`mailto:${maker.contact}`} className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-100 dark:bg-slate-800/40 text-slate-700 dark:text-slate-200 font-semibold hover:bg-slate-200 dark:hover:bg-slate-700/60 transition-colors duration-200 shadow-sm">
                      <Mail className="w-4 h-4" /> {maker.contact}
                    </a>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Floating Chat Input/Button */}
      <div className="fixed inset-x-0 mx-auto bottom-4 sm:bottom-8 z-50 w-full max-w-lg sm:max-w-2xl px-2 sm:px-4 animate-fade-in-up">
        <div className="backdrop-blur-lg bg-white/90 dark:bg-slate-900/90 border border-slate-200/60 dark:border-slate-700/60 shadow-2xl rounded-2xl px-3 sm:px-6 py-3 sm:py-4 flex flex-col items-center gap-2">
          <div className="w-full flex flex-col sm:flex-row items-center gap-2">
            <input
              type="text"
              className="flex-1 rounded-xl border border-slate-300 dark:border-slate-600 bg-white/80 dark:bg-slate-800/80 px-3 sm:px-4 py-2 sm:py-3 text-base sm:text-lg text-slate-900 dark:text-slate-100 placeholder:text-slate-500 dark:placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-400 dark:focus:ring-blue-500 transition-colors duration-300 shadow-sm cursor-pointer backdrop-blur-md"
              placeholder="Ask about legal matters, case law, or your document..."
              onFocus={onGetStarted}
              readOnly
            />
            <a
              className="inline-flex items-center gap-2 px-4 sm:px-6 py-2 sm:py-3 rounded-xl border border-blue-600 dark:border-blue-400 text-blue-700 dark:text-blue-300 font-semibold bg-white/90 dark:bg-slate-900/90 hover:bg-blue-50 dark:hover:bg-blue-800/40 transition-all duration-300 shadow-lg text-base sm:text-lg cursor-pointer"
              onClick={onGetStarted}
            >
              Get Started <ArrowRight className="ml-2 w-5 h-5" />
            </a>
          </div>
          <span className="text-xs text-slate-500 dark:text-slate-400 text-center">Sign in to start chatting</span>
        </div>
      </div>

      {/* Footer */}
      <footer className="w-full py-6 text-center text-slate-500 dark:text-slate-400 text-sm bg-white/90 dark:bg-slate-900/90 border-t border-slate-200/60 dark:border-slate-700/60 mt-auto backdrop-blur-sm">
        © {new Date().getFullYear()} LegalDoc · Built with ♥ by Chaitanya Bansal & Madhurya Mishra
      </footer>
    </div>
  );
} 