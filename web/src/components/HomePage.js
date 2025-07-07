import React, { useEffect, useRef } from "react";
import {
  Scale, Github, ArrowRight, Sparkles, Brain, Zap, Shield, Target, TrendingUp, BookOpen, FileText, Award, Users, Clock
} from "lucide-react";
import { Button } from "./ui/button";
import { Card, CardContent } from "./ui/card";
import { Badge } from "./ui/badge";

const sections = [
  { key: "Home", label: "Home" },
  { key: "Features", label: "Features" },
  { key: "WhyUseLegalDoc", label: "Why LegalDoc" },
  { key: "TechStack", label: "Tech Stack" },
  { key: "FAQs", label: "FAQs" },
];

const features = [
  {
    icon: Brain,
    title: "AI-Powered Analysis",
    description: "Advanced machine learning algorithms analyze your legal documents with precision and speed.",
    color: "text-blue-500",
    bgColor: "bg-blue-500/10",
  },
  {
    icon: Zap,
    title: "Lightning Fast",
    description: "Get comprehensive document analysis in seconds, not hours. Boost your productivity instantly.",
    color: "text-yellow-500",
    bgColor: "bg-yellow-500/10",
  },
  {
    icon: Shield,
    title: "Bank-Grade Security",
    description: "Your documents are protected with enterprise-level encryption and privacy controls.",
    color: "text-green-500",
    bgColor: "bg-green-500/10",
  },
  {
    icon: Target,
    title: "Precision Insights",
    description: "Extract key information, dates, and actionable insights with unmatched accuracy.",
    color: "text-purple-500",
    bgColor: "bg-purple-500/10",
  },
];

const stats = [
  { number: "500+", label: "Legal Firms", icon: Users },
  { number: "50K+", label: "Documents Analyzed", icon: FileText },
  { number: "80%", label: "Time Saved", icon: Clock },
  { number: "99.9%", label: "Accuracy Rate", icon: Target },
];

const whyUseLegalDoc = [
  {
    icon: TrendingUp,
    title: "Extract Key Dates",
    description: "Automatically find important deadlines and milestones in contracts and agreements.",
    color: "text-blue-500",
    bgColor: "bg-blue-500/10",
  },
  {
    icon: BookOpen,
    title: "Clause Identification",
    description: "Identify and highlight relevant legal sections and clauses for quick review.",
    color: "text-purple-500",
    bgColor: "bg-purple-500/10",
  },
  {
    icon: FileText,
    title: "Comprehensive Summaries",
    description: "Generate clear, actionable summaries for lengthy legal documents.",
    color: "text-green-500",
    bgColor: "bg-green-500/10",
  },
  {
    icon: Sparkles,
    title: "Actionable Next Steps",
    description: "Get AI-powered recommendations for follow-up and compliance.",
    color: "text-yellow-500",
    bgColor: "bg-yellow-500/10",
  },
  {
    icon: Award,
    title: "Multi-format Support",
    description: "Works with PDF, DOCX, TXT, and scanned documents with OCR.",
    color: "text-indigo-500",
    bgColor: "bg-indigo-500/10",
  },
  {
    icon: Shield,
    title: "Enterprise Security",
    description: "Bank-grade encryption, access controls, and audit trails for peace of mind.",
    color: "text-red-500",
    bgColor: "bg-red-500/10",
  },
];

export default function HomePage({ onGetStarted, activeTab, setActiveTab }) {
  const sectionRefs = {
    Home: useRef(null),
    Features: useRef(null),
    WhyUseLegalDoc: useRef(null),
    TechStack: useRef(null),
    FAQs: useRef(null),
  };

  // Scroll to section when tab is clicked, accounting for header height (80px)
  const handleTabClick = (key) => {
    const ref = sectionRefs[key];
    if (ref && ref.current) {
      const y = ref.current.getBoundingClientRect().top + window.scrollY - 80;
      window.scrollTo({ top: y, behavior: "smooth" });
      setActiveTab(key); // Ensure tab is highlighted immediately on click
    }
  };

  // IntersectionObserver to update activeTab on scroll
  useEffect(() => {
    const observerOptions = { root: null, rootMargin: "-40% 0px -40% 0px", threshold: 0 };
    const observers = [];
    sections.forEach(({ key }) => {
      const ref = sectionRefs[key];
      if (ref && ref.current) {
        const obs = new window.IntersectionObserver((entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              setActiveTab(key);
            }
          });
        }, observerOptions);
        obs.observe(ref.current);
        observers.push(obs);
      }
    });
    return () => observers.forEach((obs) => obs.disconnect());
  }, [setActiveTab]);

  return (
    <div className="min-h-screen bg-background bg-dots font-sans transition-colors duration-300">
      {/* Hero Section - ensure only this is visible on load */}
      <section
        ref={sectionRefs.Home}
        id="home"
        className="relative py-20 px-4 sm:px-6 lg:px-8 overflow-hidden flex items-center justify-center"
        style={{ minHeight: 'calc(100vh - 80px)' }}
      >
        <div className="absolute inset-0 bg-dots opacity-30 pointer-events-none" />
        <div className="max-w-7xl mx-auto relative z-10">
          <div className="text-center">
            <h1 className="text-5xl sm:text-7xl font-extrabold tracking-tight mb-8 fade-in-up-delay-1">
              Professional Legal<br />
              <span className="block text-primary">Document Analysis</span>
            </h1>
            <p className="text-base sm:text-lg text-muted-foreground mb-10 max-w-3xl mx-auto fade-in-up-delay-2">
              Transform your legal practice with AI-powered document analysis. Upload contracts, agreements, and legal documents to get instant insights, summaries, and actionable recommendations.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center fade-in-up-delay-3">
              <Button size="lg" className="text-lg px-8 hover-lift pulse-glow" onClick={onGetStarted}>
                Get Started <ArrowRight className="ml-2 h-5 w-5 transition-transform group-hover:translate-x-1" />
              </Button>
              <Button variant="outline" size="lg" className="text-lg px-8 bg-transparent hover-glow" onClick={() => handleTabClick("Features")}> <Zap className="mr-2 h-5 w-5" /> Explore Features </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section ref={sectionRefs.Features} id="features" className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16 fade-in-up">
            <h2 className="text-3xl sm:text-4xl font-bold mb-4">Powerful Features for Legal Professionals</h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Everything you need to analyze, understand, and act on legal documents efficiently.
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <Card key={index} className={`text-center hover-glow fade-in-up-delay-${index + 1}`}>
                <CardContent>
                  <div className={`mx-auto mb-4 p-4 ${feature.bgColor} rounded-full w-fit`}>
                    <feature.icon className={`h-8 w-8 ${feature.color}`} />
                  </div>
                  <div className="text-xl font-bold mb-2">{feature.title}</div>
                  <div className="text-base text-muted-foreground">{feature.description}</div>
                </CardContent>
              </Card>
            ))}
        </div>
        </div>
      </section>

      {/* Why Use LegalDoc Section (merged Use Cases + Why LegalDoc) */}
      <section ref={sectionRefs.WhyUseLegalDoc} id="whyuselegaldoc" className="py-20 px-4 sm:px-6 lg:px-8 bg-muted/30">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16 fade-in-up">
            <h2 className="text-3xl sm:text-4xl font-bold mb-4">Why Use LegalDoc?</h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Built specifically for lawyers, paralegals, and legal teams who need accurate, reliable document analysis with professional-grade security.
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {whyUseLegalDoc.map((item, idx) => (
              <Card key={idx} className={`text-center hover-glow fade-in-up-delay-${idx + 1}`}>
                <CardContent>
                  <div className={`mx-auto mb-4 p-4 ${item.bgColor} rounded-full w-fit`}>
                    <item.icon className={`h-8 w-8 ${item.color}`} />
                  </div>
                  <div className="text-lg font-bold mb-2">{item.title}</div>
                  <div className="text-base text-muted-foreground">{item.description}</div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
            </section>

      {/* Tech Stack Section */}
      <section ref={sectionRefs.TechStack} id="techstack" className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-12 fade-in-up">
            <h2 className="text-3xl sm:text-4xl font-bold mb-4">Technology Stack</h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Built with modern, scalable, and secure technologies for legal professionals.
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            <Card className="hover-glow">
              <CardContent>
                <div className="text-lg font-bold mb-2">Backend</div>
                <ul className="list-disc pl-6 space-y-1 text-base text-foreground">
                  <li>FastAPI (Python): High-performance REST API</li>
                  <li>PyTorch + Hugging Face Transformers: Core NLP</li>
                  <li>spaCy + Prodigy: Annotation and rule-based entity matching</li>
                  <li>PDFPlumber / PyMuPDF + Tesseract OCR: Robust text extraction</li>
                  <li>Celery + Redis: Asynchronous job management</li>
                  <li>PostgreSQL: Secure storage for parsed data</li>
                  <li>Elasticsearch: Full-text search for extracted content</li>
              </ul>
              </CardContent>
            </Card>
            <Card className="hover-glow">
              <CardContent>
                <div className="text-lg font-bold mb-2">Frontend</div>
                <ul className="list-disc pl-6 space-y-1 text-base text-foreground">
                  <li>React.js: Interactive UI for document upload and review</li>
                  <li>Tailwind CSS: Clean, modern styling and responsive layouts</li>
              </ul>
              </CardContent>
            </Card>
            <Card className="hover-glow">
              <CardContent>
                <div className="text-lg font-bold mb-2">API & Integrations</div>
                <ul className="list-disc pl-6 space-y-1 text-base text-foreground">
                  <li>OpenAPI-compliant REST endpoints</li>
                  <li>Webhooks & client libraries for integration</li>
              </ul>
              </CardContent>
            </Card>
        </div>
      </div>
      </section>

      {/* FAQs Section */}
      <section ref={sectionRefs.FAQs} id="faqs" className="py-20 px-4 sm:px-6 lg:px-8 bg-muted/30">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-12 fade-in-up">
            <h2 className="text-3xl sm:text-4xl font-bold mb-4">Frequently Asked Questions</h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Answers to common questions about LegalDoc and its features.
            </p>
                  </div>
          <ul className="list-disc pl-6 space-y-4 text-base text-foreground max-w-3xl mx-auto text-left">
            <li><b>Which document formats do you support?</b> PDFs, Word (DOC/DOCX), plain text (TXT), and scanned documents via embedded OCR. All textual content—including tables, footnotes, and sidebar notes—is extracted and processed.</li>
            <li><b>How accurate is the parser?</b> AI models, trained on real legal documents and fine-tuned via rule-based logic, regularly achieve over 90% precision and recall for standard clauses. Confidence indicators accompany every output, and user reviews further improve accuracy via feedback loops.</li>
            <li><b>Can I customize clause extraction?</b> Yes. Use our UI to define clause patterns via keywords or regex, label training samples, and trigger custom model training. This ensures LegalDoc fits your company's unique legal vocabulary and requirements.</li>
            <li><b>What about data security?</b> Secure deployments (cloud or on-premises) with encryption at rest/in transit, role-based access, OAuth 2.0 authentication, and full audit trails. Designed for compliance with enterprise data standards.</li>
            <li><b>Is technical expertise needed?</b> No. The intuitive dashboard allows anyone to upload, parse, and export documents without coding.</li>
            <li><b>Can I scale document processing?</b> Absolutely. Container-based orchestration automatically scales to handle high document volumes. Administrators can monitor throughput, queue depth, and system performance in real time.</li>
            <li><b>What languages and jurisdictions are covered?</b> English contracts (U.S., UK, Commonwealth) are fully supported.</li>
          </ul>
                </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-dots">
        <div className="max-w-4xl mx-auto text-center">
          <div className="fade-in-up">
            <h2 className="text-3xl sm:text-4xl font-bold mb-6">Ready to Transform Your Legal Practice?</h2>
            <p className="text-xl text-muted-foreground mb-8">
              Join LegalDoc for your legal document analysis needs.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" className="text-lg px-8 hover-lift pulse-glow" onClick={onGetStarted}>
                <Sparkles className="mr-2 h-5 w-5" /> Get Started <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
              <Button variant="outline" size="lg" className="text-lg px-8 bg-transparent hover-glow" onClick={() => handleTabClick("Features")}> <BookOpen className="mr-2 h-5 w-5" /> Learn More </Button>
            </div>
        </div>
      </div>
      </section>

      {/* Footer */}
      <footer className="w-full py-8 text-center text-foreground/60 text-sm bg-background/90 border-t border-border/60 mt-auto backdrop-blur-sm">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4 px-4">
          <div className="flex items-center gap-2 justify-center">
            <Scale className="w-8 h-8 text-primary" />
            <span className="font-bold text-foreground">LegalDoc</span>
            <span className="text-xs text-muted-foreground ml-2">© {new Date().getFullYear()} All rights reserved.</span>
          </div>
          <div className="flex items-center gap-4 justify-center">
            <a href="https://github.com/madhurya-ops/Legal-Document-Parser" target="_blank" rel="noopener noreferrer" className="text-primary hover:underline hover-scale">GitHub</a>
            <span className="text-muted-foreground">·</span>
            <a href="mailto:bansalchaitanya1234@gmail.com" className="text-primary hover:underline hover-scale">Contact</a>
          </div>
        </div>
      </footer>
    </div>
  );
} 