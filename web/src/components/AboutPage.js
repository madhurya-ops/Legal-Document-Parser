import React, { useEffect, useState, useRef } from "react";
import { Scale, Github, Loader2, Mail, FileText as ResumeIcon, ArrowRight } from "lucide-react";
import ThemeToggle from "./ThemeToggle";
import { Button } from "./ui/button";
import { Card, CardContent } from "./ui/card";

const tabs = [
  "Home",
  "Features",
  "Use Cases",
  "Why LegalDoc",
  "Tech Stack",
  "FAQs",
  "About"
];

const MAKERS = [
  {
    github: "https://github.com/Chai-B/Chai-B",
    api: "https://api.github.com/users/Chai-B",
    name: "Chaitanya Bansal",
    role: "Co-Founder",
    description: "Final year engineering student exploring AI/ML. Currently working on Legal Doc Interpretator. Learning LLM, LangChain, FastAPI, Streamlit.",
    contact: "bansalchaitanya1234@gmail.com",
    resume: "https://github.com/Chai-B/Chai-B/blob/main/resume.pdf",
    projects: "https://github.com/Chai-B?tab=repositories"
  },
  {
    github: "https://github.com/madhurya-ops/madhurya-ops",
    api: "https://api.github.com/users/madhurya-ops",
    name: "Madhurya Mishra",
    role: "Co-Founder",
    description: "Final year engineering student exploring AI/ML. Currently working on Legal Doc Interpreter. Learning LangChain, LLM, FastAPI, React.",
    contact: "madhuryamishra@gmail.com",
    resume: "https://github.com/madhurya-ops/Madhurya_Mishra/blob/main/Madhurya_Mishra_Resume.pdf",
    projects: "https://github.com/madhurya-ops?tab=repositories"
  }
];

const values = [
  {
    icon: Scale,
    title: "Integrity",
    description: "We believe in honest, transparent, and ethical AI for legal work.",
    color: "text-blue-500",
    bgColor: "bg-blue-500/10",
  },
  {
    icon: Github,
    title: "Open Source",
    description: "We build in the open and share our work with the community.",
    color: "text-green-500",
    bgColor: "bg-green-500/10",
  },
  {
    icon: Mail,
    title: "Support",
    description: "We are always available for feedback and support.",
    color: "text-purple-500",
    bgColor: "bg-purple-500/10",
  },
];

export default function AboutPage({ onGetStarted, onTabChange, activeTab }) {
  const [profiles, setProfiles] = useState([null, null]);
  const [loading, setLoading] = useState(true);
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

  return (
    <div className="min-h-screen flex flex-col bg-background bg-dots relative overflow-hidden transition-colors duration-300 font-sans">
      {/* About Content (Mission, Team, Values, Contact, About the Makers) */}
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-16 fade-in-up">
          <div className="mx-auto mb-6 p-4 bg-primary/10 rounded-full w-fit">
            <Scale className="h-12 w-12 text-primary float-animation" />
          </div>
          <h1 className="text-4xl font-bold mb-4 text-foreground">About LegalDoc</h1>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            We're a passionate team of developers and AI engineers dedicated to revolutionizing how legal professionals work with documents.
          </p>
        </div>
        {/* Mission */}
        <section className="mb-16 fade-in-up-delay-1">
          <Card className="p-8 hover-glow">
            <div className="text-center">
              <div className="mx-auto mb-6 p-3 bg-primary/10 rounded-full w-fit">
                <Scale className="h-8 w-8 text-primary float-animation" />
              </div>
              <h2 className="text-3xl font-bold mb-6 text-foreground">Our Mission</h2>
              <p className="text-lg text-muted-foreground leading-relaxed max-w-4xl mx-auto">
                To empower legal professionals with cutting-edge AI technology that makes document analysis faster, more accurate, and more accessible. We believe that by combining the precision of artificial intelligence with the expertise of legal professionals, we can create tools that enhance rather than replace human judgment.
              </p>
            </div>
          </Card>
        </section>
        {/* Team */}
        <section className="mb-16">
          <h2 className="text-3xl font-bold text-center mb-12 fade-in-up text-foreground">Meet Our Team</h2>
          <div className="grid md:grid-cols-2 gap-8">
            {MAKERS.map((member, index) => (
              <Card key={index} className={`hover-lift hover-glow fade-in-up-delay-${index + 1}`}>
                <CardContent>
                  <div className="flex flex-col items-center">
                    <img
                      src={profiles[index]?.avatar_url || "https://avatars.githubusercontent.com/u/9919?v=4"}
                      alt="GitHub Avatar"
                      className="w-24 h-24 rounded-full shadow-lg mb-4 border-4 border-background group-hover:border-border transition-all duration-300 float-animation"
                    />
                    <div className="text-xl font-bold text-foreground mb-1 text-center">{profiles[index]?.name || member.name}</div>
                    <div className="text-base font-medium text-primary mb-2 text-center">{member.role}</div>
                    <p className="text-sm text-muted-foreground text-center mb-6">{member.description}</p>
                    <div className="flex justify-center space-x-2">
                      <Button variant="outline" size="icon" asChild className="hover-scale hover-glow bg-transparent">
                        <a href={member.github} target="_blank" rel="noopener noreferrer">
                          <Github className="h-4 w-4" />
                        </a>
                      </Button>
                      <Button variant="outline" size="icon" asChild className="hover-scale hover-glow bg-transparent">
                        <a href={`mailto:${member.contact}`}>
                          <Mail className="h-4 w-4" />
                        </a>
                      </Button>
                      <Button variant="outline" size="icon" asChild className="hover-scale hover-glow bg-transparent">
                        <a href={member.resume} target="_blank" rel="noopener noreferrer">
                          <ResumeIcon className="h-4 w-4" />
                        </a>
                      </Button>
                      <Button variant="outline" size="icon" asChild className="hover-scale hover-glow bg-transparent">
                        <a href={member.projects} target="_blank" rel="noopener noreferrer">
                          <ResumeIcon className="h-4 w-4" />
                        </a>
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </section>
        {/* Values */}
        <section className="mb-16">
          <h2 className="text-3xl font-bold text-center mb-12 fade-in-up text-foreground">Our Values</h2>
          <div className="grid md:grid-cols-3 gap-6">
            {values.map((value, index) => (
              <Card key={index} className={`text-center p-6 hover-lift hover-glow fade-in-up-delay-${index + 1}`}>
                <CardContent>
                  <div className={`mx-auto mb-4 p-3 ${value.bgColor} rounded-full w-fit float-animation float-delay-${index + 1}`}>
                    <value.icon className={`h-6 w-6 ${value.color}`} />
                  </div>
                  <div className="text-lg font-bold text-foreground mb-2">{value.title}</div>
                  <p className="text-sm text-muted-foreground">{value.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </section>
        {/* Contact */}
        <section className="fade-in-up">
          <Card className="p-8 text-center hover-glow">
            <CardContent>
              <div className="mx-auto mb-4 p-3 bg-primary/10 rounded-full w-fit">
                <Mail className="h-8 w-8 text-primary float-animation" />
              </div>
              <div className="text-2xl font-bold text-foreground mb-2">Get in Touch</div>
              <div className="text-muted-foreground mb-4">Have questions or feedback? We'd love to hear from you.</div>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Button variant="outline" asChild className="hover-lift hover-glow bg-transparent">
                  <a href="mailto:bansalchaitanya1234@gmail.com">
                    <Mail className="h-4 w-4 mr-2" />
                    bansalchaitanya1234@gmail.com
                  </a>
                </Button>
                <Button variant="outline" asChild className="hover-lift hover-glow bg-transparent">
                  <a href="mailto:madhuryamishra@gmail.com">
                    <Mail className="h-4 w-4 mr-2" />
                    madhuryamishra@gmail.com
                  </a>
                </Button>
                <Button variant="outline" asChild className="hover-lift hover-glow bg-transparent">
                  <a href="https://github.com/madhurya-ops/Legal-Document-Parser" target="_blank" rel="noopener noreferrer">
                    <Github className="h-4 w-4 mr-2" />
                    GitHub
                  </a>
                </Button>
              </div>
            </CardContent>
          </Card>
        </section>
      </div>
    </div>
  );
} 