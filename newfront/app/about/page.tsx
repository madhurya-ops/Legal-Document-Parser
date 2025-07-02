import { Github, Linkedin, Mail, Scale, Heart, Code, Lightbulb, Shield, Users, Zap, Target } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"

export default function AboutPage() {
  const team = [
    {
      name: "Alex Johnson",
      role: "Lead Developer & AI Engineer",
      description: "Specialized in AI/ML and natural language processing with 8+ years of experience in legal tech.",
      github: "alexjohnson",
      linkedin: "alex-johnson-dev",
      email: "alex@legalai.com",
      color: "from-blue-500 to-purple-500",
    },
    {
      name: "Sarah Chen",
      role: "Legal Tech Consultant",
      description: "Former attorney with expertise in legal document analysis and regulatory compliance.",
      github: "sarahchen",
      linkedin: "sarah-chen-legal",
      email: "sarah@legalai.com",
      color: "from-green-500 to-teal-500",
    },
    {
      name: "Michael Rodriguez",
      role: "Backend Engineer",
      description: "Expert in secure, scalable systems and data privacy with focus on enterprise solutions.",
      github: "mrodriguez",
      linkedin: "michael-rodriguez-eng",
      email: "michael@legalai.com",
      color: "from-orange-500 to-red-500",
    },
  ]

  const technologies = [
    { name: "Next.js", color: "bg-black text-white" },
    { name: "TypeScript", color: "bg-blue-600 text-white" },
    { name: "OpenAI GPT-4", color: "bg-green-600 text-white" },
    { name: "Vector Databases", color: "bg-purple-600 text-white" },
    { name: "RAG Architecture", color: "bg-indigo-600 text-white" },
    { name: "Tailwind CSS", color: "bg-cyan-600 text-white" },
    { name: "Node.js", color: "bg-green-700 text-white" },
    { name: "Python", color: "bg-yellow-600 text-white" },
    { name: "PostgreSQL", color: "bg-blue-700 text-white" },
    { name: "Redis", color: "bg-red-600 text-white" },
  ]

  const values = [
    {
      icon: Shield,
      title: "Privacy First",
      description: "Your documents are processed with the highest standards of privacy and security.",
      color: "text-green-500",
      bgColor: "bg-green-500/10",
    },
    {
      icon: Target,
      title: "Accuracy",
      description: "We continuously improve our AI models to ensure the most accurate analysis.",
      color: "text-blue-500",
      bgColor: "bg-blue-500/10",
    },
    {
      icon: Lightbulb,
      title: "Innovation",
      description: "Constantly pushing the boundaries of what's possible with legal AI.",
      color: "text-yellow-500",
      bgColor: "bg-yellow-500/10",
    },
    {
      icon: Heart,
      title: "Support",
      description: "Dedicated to providing exceptional support to our legal professional users.",
      color: "text-red-500",
      bgColor: "bg-red-500/10",
    },
  ]

  return (
    <div className="min-h-screen py-12 px-4 sm:px-6 lg:px-8 dotted-background">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-16 fade-in-up">
          <div className="mx-auto mb-6 p-4 bg-primary/10 rounded-full w-fit">
            <Scale className="h-12 w-12 text-primary float-animation" />
          </div>
          <h1 className="text-4xl font-bold mb-4">About LegalAI</h1>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            We're a passionate team of developers, legal experts, and AI engineers dedicated to revolutionizing how
            legal professionals work with documents.
          </p>
        </div>

        {/* Mission */}
        <section className="mb-16 fade-in-up-delay-1">
          <Card className="p-8 hover-glow">
            <div className="text-center">
              <div className="mx-auto mb-6 p-3 bg-primary/10 rounded-full w-fit">
                <Zap className="h-8 w-8 text-primary float-animation" />
              </div>
              <h2 className="text-3xl font-bold mb-6">Our Mission</h2>
              <p className="text-lg text-muted-foreground leading-relaxed max-w-4xl mx-auto">
                To empower legal professionals with cutting-edge AI technology that makes document analysis faster, more
                accurate, and more accessible. We believe that by combining the precision of artificial intelligence
                with the expertise of legal professionals, we can create tools that enhance rather than replace human
                judgment.
              </p>
            </div>
          </Card>
        </section>

        {/* Team */}
        <section className="mb-16">
          <h2 className="text-3xl font-bold text-center mb-12 fade-in-up">Meet Our Team</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {team.map((member, index) => (
              <Card key={index} className={`hover-lift hover-glow fade-in-up-delay-${index + 1}`}>
                <CardHeader>
                  <div
                    className={`w-20 h-20 bg-gradient-to-br ${member.color} rounded-full mx-auto mb-4 flex items-center justify-center float-animation float-delay-${index + 1}`}
                  >
                    <span className="text-2xl font-bold text-white">
                      {member.name
                        .split(" ")
                        .map((n) => n[0])
                        .join("")}
                    </span>
                  </div>
                  <CardTitle className="text-center">{member.name}</CardTitle>
                  <CardDescription className="text-center font-medium text-primary">{member.role}</CardDescription>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground text-center mb-6">{member.description}</p>
                  <div className="flex justify-center space-x-2">
                    <Button variant="outline" size="icon" asChild className="hover-scale hover-glow bg-transparent">
                      <a href={`https://github.com/${member.github}`} target="_blank" rel="noopener noreferrer">
                        <Github className="h-4 w-4" />
                      </a>
                    </Button>
                    <Button variant="outline" size="icon" asChild className="hover-scale hover-glow bg-transparent">
                      <a href={`https://linkedin.com/in/${member.linkedin}`} target="_blank" rel="noopener noreferrer">
                        <Linkedin className="h-4 w-4" />
                      </a>
                    </Button>
                    <Button variant="outline" size="icon" asChild className="hover-scale hover-glow bg-transparent">
                      <a href={`mailto:${member.email}`}>
                        <Mail className="h-4 w-4" />
                      </a>
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </section>

        {/* Technology Stack */}
        <section className="mb-16 fade-in-up">
          <Card className="p-8 hover-glow">
            <CardHeader className="text-center">
              <div className="mx-auto mb-4 p-3 bg-primary/10 rounded-full w-fit">
                <Code className="h-8 w-8 text-primary float-animation" />
              </div>
              <CardTitle className="text-2xl">Built with Modern Technology</CardTitle>
              <CardDescription>Our platform leverages the latest in web development and AI technology</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap justify-center gap-3">
                {technologies.map((tech, index) => (
                  <Badge
                    key={index}
                    className={`text-sm py-2 px-4 hover-scale hover-glow ${tech.color} fade-in-up-delay-${index + 1}`}
                  >
                    {tech.name}
                  </Badge>
                ))}
              </div>
            </CardContent>
          </Card>
        </section>

        {/* Values */}
        <section className="mb-16">
          <h2 className="text-3xl font-bold text-center mb-12 fade-in-up">Our Values</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {values.map((value, index) => (
              <Card key={index} className={`text-center p-6 hover-lift hover-glow fade-in-up-delay-${index + 1}`}>
                <CardHeader>
                  <div
                    className={`mx-auto mb-4 p-3 ${value.bgColor} rounded-full w-fit float-animation float-delay-${index + 1}`}
                  >
                    <value.icon className={`h-6 w-6 ${value.color}`} />
                  </div>
                  <CardTitle className="text-lg">{value.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground">{value.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </section>

        {/* Contact */}
        <section className="fade-in-up">
          <Card className="p-8 text-center hover-glow">
            <CardHeader>
              <div className="mx-auto mb-4 p-3 bg-primary/10 rounded-full w-fit">
                <Users className="h-8 w-8 text-primary float-animation" />
              </div>
              <CardTitle className="text-2xl">Get in Touch</CardTitle>
              <CardDescription>Have questions or feedback? We'd love to hear from you.</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Button variant="outline" asChild className="hover-lift hover-glow bg-transparent">
                  <a href="mailto:team@legalai.com">
                    <Mail className="h-4 w-4 mr-2" />
                    team@legalai.com
                  </a>
                </Button>
                <Button variant="outline" asChild className="hover-lift hover-glow bg-transparent">
                  <a href="https://github.com/legalai" target="_blank" rel="noopener noreferrer">
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
  )
}
