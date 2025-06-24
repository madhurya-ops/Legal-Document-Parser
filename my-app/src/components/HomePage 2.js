import React, { useEffect, useState } from "react";
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

  useEffect(() => {
    Promise.all(MAKERS.map(m => fetch(m.api).then(res => res.json()))).then(setProfiles).finally(() => setLoading(false));
  }, []);

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
                  onClick={() => { setActiveTab(tab); setMenuOpen(false); }}
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
            onClick={() => setActiveTab('About')}
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
      </main>

      {/* Tab Content */}
      <div className="max-w-5xl mx-auto px-2 sm:px-4 md:px-0 pb-10 sm:pb-16">
        <div className="rounded-3xl bg-white/90 dark:bg-slate-900/90 backdrop-blur-lg shadow-2xl border border-slate-200/60 dark:border-slate-700/60 p-4 sm:p-8 md:p-12 space-y-6 sm:space-y-8">
          {activeTab === "About" && (
            <section>
              <h2 className="text-2xl font-extrabold text-slate-900 dark:text-slate-100 mb-2 tracking-tight">
                About <span className="text-blue-700 dark:text-blue-400">LegalDoc</span>
              </h2>
              <p className="text-lg font-medium text-slate-900 dark:text-slate-100 mb-3">LegalDoc is a smart legal assistant platform that simplifies the interpretation of legal documents using AI. Designed for law firms, corporate legal teams, startups, and freelancers, it accelerates document review and clarifies complex clauses in plain English. Its AI extracts key obligations, penalties, deadlines, responsibilities, and actionable insights from PDF, DOCX, or TXT files within seconds.</p>
              <p className="text-lg font-medium text-slate-900 dark:text-slate-100">LegalDoc also detects inconsistencies and risky clauses, delivering proactive recommendations. With enterprise-grade security, JWT authentication, encrypted storage, and an intuitive dashboard, it's a future-ready tool for modern legal professionals.</p>
            </section>
          )}
          {activeTab === "Features" && (
            <section>
              <h2 className="text-2xl font-extrabold text-slate-900 dark:text-slate-100 mb-2 tracking-tight">
                <span className="text-blue-700 dark:text-blue-400">Key Features</span>
              </h2>
              <ul className="list-disc pl-6 space-y-2">
                <li className="text-base font-medium text-blue-700 dark:text-blue-400">Instant document parsing and AI-based clause extraction</li>
                <li className="text-base font-medium text-slate-700 dark:text-slate-300">Summary generation with <span className='text-blue-700 dark:text-blue-400'>clear, actionable insights</span></li>
                <li className="text-base font-medium text-slate-700 dark:text-slate-300">Risk assessment of <span className='text-blue-700 dark:text-blue-400'>contractual clauses</span></li>
                <li className="text-base font-medium text-blue-700 dark:text-blue-400">Real-time contract obligation reminders</li>
                <li className="text-base font-medium text-blue-700 dark:text-blue-400">Legal chatbot for immediate answers on uploaded documents</li>
                <li className="text-base font-medium text-slate-700 dark:text-slate-300">Support for <span className='text-blue-700 dark:text-blue-400'>PDF, DOCX, TXT</span> formats</li>
                <li className="text-base font-medium text-blue-700 dark:text-blue-400">Dark mode and responsive modern UI</li>
                <li className="text-base font-medium text-blue-700 dark:text-blue-400">Secure JWT-based authentication and user management</li>
                <li className="text-base font-medium text-slate-700 dark:text-slate-300">Document dashboard with <span className='text-blue-700 dark:text-blue-400'>version history</span></li>
                <li className="text-base font-medium text-blue-700 dark:text-blue-400">Custom tags, categories, and search features</li>
              </ul>
            </section>
          )}
          {activeTab === "Use Cases" && (
            <section>
              <h2 className="text-2xl font-extrabold text-slate-900 dark:text-slate-100 mb-2 tracking-tight">
                <span className="text-blue-700 dark:text-blue-400">Use Cases</span>
              </h2>
              <ul className="list-disc pl-6 space-y-2">
                <li className="text-base font-medium text-slate-700 dark:text-slate-300">Startups validating vendor agreements and NDAs</li>
                <li className="text-base font-medium text-slate-700 dark:text-slate-300">Law firms performing fast initial contract reviews</li>
                <li className="text-base font-medium text-slate-700 dark:text-slate-300">Business teams extracting obligations and penalties from service contracts</li>
                <li className="text-base font-medium text-slate-700 dark:text-slate-300">Freelancers reviewing client contracts</li>
                <li className="text-base font-medium text-slate-700 dark:text-slate-300">HR teams interpreting employment agreements</li>
                <li className="text-base font-medium text-slate-700 dark:text-slate-300">Real estate firms analyzing lease agreements</li>
                <li className="text-base font-medium text-slate-700 dark:text-slate-300">Corporate legal ops managing large-scale document libraries</li>
                <li className="text-base font-medium text-slate-700 dark:text-slate-300">Compliance teams scanning for non-standard clauses</li>
              </ul>
            </section>
          )}
          {activeTab === "Why LegalDoc" && (
            <section>
              <h2 className="text-2xl font-extrabold text-slate-900 dark:text-slate-100 mb-2 tracking-tight">
                Why Choose <span className="text-blue-700 dark:text-blue-400">LegalDoc?</span>
              </h2>
              <ul className="list-disc pl-6 space-y-2">
                <li className="text-base font-medium text-slate-700 dark:text-slate-300">5x faster document reviews with AI-powered summaries</li>
                <li className="text-base font-medium text-slate-700 dark:text-slate-300">Plain-English explanations of complex legal language</li>
                <li className="text-base font-medium text-slate-700 dark:text-slate-300">End-to-end document management from upload to chat-based queries</li>
                <li className="text-base font-medium text-slate-700 dark:text-slate-300">Real-time deadline notifications and contract risk reports</li>
                <li className="text-base font-medium text-slate-700 dark:text-slate-300">Enterprise-grade security with encrypted storage and JWT tokens</li>
                <li className="text-base font-medium text-slate-700 dark:text-slate-300">Customizable tags, categories, and filters</li>
                <li className="text-base font-medium text-slate-700 dark:text-slate-300">Modern, responsive, accessible interface with dark mode</li>
              </ul>
            </section>
          )}
          {activeTab === "Tech Stack" && (
            <section>
              <h2 className="text-2xl font-extrabold text-slate-900 dark:text-slate-100 mb-2 tracking-tight">
                <span className="text-blue-700 dark:text-blue-400">Technology Stack</span>
              </h2>
              <ul className="list-disc pl-6 space-y-2">
                <li className="text-base font-medium text-slate-700 dark:text-slate-300">React + Tailwind CSS frontend</li>
                <li className="text-base font-medium text-slate-700 dark:text-slate-300">FastAPI backend for rapid API services</li>
                <li className="text-base font-medium text-slate-700 dark:text-slate-300">PostgreSQL for document metadata storage</li>
                <li className="text-base font-medium text-slate-700 dark:text-slate-300">LangChain orchestration for LLM pipelines</li>
                <li className="text-base font-medium text-slate-700 dark:text-slate-300">Hugging Face models for AI document parsing</li>
                <li className="text-base font-medium text-slate-700 dark:text-slate-300">Docker-based containerization for scalable deployments</li>
                <li className="text-base font-medium text-slate-700 dark:text-slate-300">JWT and bcrypt for authentication and security</li>
              </ul>
            </section>
          )}
          {activeTab === "FAQs" && (
            <section>
              <h2 className="text-2xl font-extrabold text-slate-900 dark:text-slate-100 mb-2 tracking-tight">
                <span className="text-blue-700 dark:text-blue-400">Frequently Asked Questions</span>
              </h2>
              <ul className="list-disc pl-6 space-y-2">
                <li className="text-base font-medium text-slate-700 dark:text-slate-300"><strong>Which formats are supported?</strong> — PDF, DOCX, and TXT files.</li>
                <li className="text-base font-medium text-slate-700 dark:text-slate-300"><strong>Is my data secure?</strong> — Yes, documents are encrypted and secured with JWT-based authentication.</li>
                <li className="text-base font-medium text-slate-700 dark:text-slate-300"><strong>Does it provide legal advice?</strong> — No, it simplifies legal text and provides AI-based summaries and risk highlights.</li>
                <li className="text-base font-medium text-slate-700 dark:text-slate-300"><strong>Can I customize clause extraction rules?</strong> — Customization features are planned for enterprise plans.</li>
                <li className="text-base font-medium text-slate-700 dark:text-slate-300"><strong>Is there a chatbot?</strong> — Yes, for legal queries on your uploaded documents.</li>
              </ul>
            </section>
          )}
        </div>
      </div>

      {/* About the Makers Section */}
      <div className="max-w-5xl mx-auto px-2 sm:px-4 md:px-0 py-3 sm:py-5 animate-fade-in-up">
        <div className="rounded-3xl bg-white/90 dark:bg-slate-900/90 backdrop-blur-lg shadow-2xl border border-slate-200/60 dark:border-slate-700/60 p-4 sm:p-8 md:p-12">
          <h3 className="text-2xl font-extrabold text-slate-900 dark:text-slate-100 mb-8 text-center tracking-tight">
            About the <span className="text-blue-700 dark:text-blue-400">Makers</span>
          </h3>
          {loading ? (
            <div className="flex items-center gap-2 text-slate-700 dark:text-slate-300 justify-center"><Loader2 className="animate-spin w-5 h-5" /> Loading profiles...</div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 sm:gap-8">
              {MAKERS.map((maker, i) => (
                <div key={maker.github} className="flex flex-col items-center shadow-lg p-6 animate-fade-in-up bg-white/80 dark:bg-slate-800/80 rounded-2xl border border-slate-200/60 dark:border-slate-600/60">
                  <img
                    src={profiles[i]?.avatar_url || "https://avatars.githubusercontent.com/u/9919?v=4"}
                    alt="GitHub Avatar"
                    className="w-24 h-24 rounded-full shadow-md mb-4"
                  />
                  <span className="text-xl font-bold text-slate-900 dark:text-slate-100 mb-1">{profiles[i]?.name || maker.name}</span>
                  <span className="text-base font-medium text-slate-700 dark:text-slate-300 mb-2 text-center">{maker.bio}</span>
                  <div className="flex flex-col gap-1 text-sm text-slate-700 dark:text-slate-300 mb-2">
                    <a href={maker.github} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-2 hover:underline hover:text-blue-600 dark:hover:text-blue-400"><Github className="w-4 h-4" /> GitHub</a>
                    <a href={maker.projects} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-2 hover:underline hover:text-blue-600 dark:hover:text-blue-400"><ResumeIcon className="w-4 h-4" /> Projects</a>
                    <a href={maker.resume} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-2 hover:underline hover:text-blue-600 dark:hover:text-blue-400"><ResumeIcon className="w-4 h-4" /> Resume</a>
                    <a href={`mailto:${maker.contact}`} className="inline-flex items-center gap-2 hover:underline hover:text-blue-600 dark:hover:text-blue-400"><Mail className="w-4 h-4" /> {maker.contact}</a>
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