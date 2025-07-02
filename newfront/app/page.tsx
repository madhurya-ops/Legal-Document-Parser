import Link from "next/link"
import {
  ArrowRight,
  FileText,
  Brain,
  Shield,
  Clock,
  Users,
  Sparkles,
  Zap,
  Target,
  Award,
  TrendingUp,
  BookOpen,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"

export default function HomePage() {
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
  ]

  const benefits = [
    { icon: TrendingUp, text: "Extract key dates and deadlines automatically" },
    { icon: BookOpen, text: "Identify relevant legal sections and clauses" },
    { icon: FileText, text: "Generate comprehensive document summaries" },
    { icon: Sparkles, text: "Get actionable next steps and recommendations" },
    { icon: Award, text: "Support for multiple document formats" },
    { icon: Shield, text: "Professional-grade accuracy and reliability" },
  ]

  const stats = [
    { number: "500+", label: "Legal Firms", icon: Users },
    { number: "50K+", label: "Documents Analyzed", icon: FileText },
    { number: "80%", label: "Time Saved", icon: Clock },
    { number: "99.9%", label: "Accuracy Rate", icon: Target },
  ]

  return (
    <div className="min-h-screen dotted-background">
      {/* Hero Section */}
      <section className="relative py-20 px-4 sm:px-6 lg:px-8 overflow-hidden">
        <div className="absolute inset-0 animated-dots opacity-30"></div>
        <div className="max-w-7xl mx-auto relative z-10">
          <div className="text-center">
            <div className="fade-in-up">
              <Badge variant="secondary" className="mb-4 hover-glow">
                <Sparkles className="w-4 h-4 mr-2" />
                Powered by Advanced AI
              </Badge>
            </div>
            <h1 className="text-4xl sm:text-6xl font-bold tracking-tight mb-6 fade-in-up-delay-1">
              Professional Legal
              <span className="text-primary block gradient-animate bg-clip-text text-transparent">
                Document Analysis
              </span>
            </h1>
            <p className="text-xl text-muted-foreground mb-8 max-w-3xl mx-auto fade-in-up-delay-2">
              Transform your legal practice with AI-powered document analysis. Upload contracts, agreements, and legal
              documents to get instant insights, summaries, and actionable recommendations.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center fade-in-up-delay-3">
              <Link href="/signup">
                <Button size="lg" className="text-lg px-8 hover-lift pulse-glow">
                  Start Free Trial
                  <ArrowRight className="ml-2 h-5 w-5 transition-transform group-hover:translate-x-1" />
                </Button>
              </Link>
              <Link href="/chat">
                <Button variant="outline" size="lg" className="text-lg px-8 bg-transparent hover-glow">
                  <Zap className="mr-2 h-5 w-5" />
                  Try Demo
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-muted/30">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <div key={index} className={`text-center fade-in-up-delay-${index + 1}`}>
                <Card className="hover-lift hover-glow">
                  <CardContent className="p-6">
                    <div className="float-animation">
                      <stat.icon className="h-8 w-8 text-primary mx-auto mb-2" />
                    </div>
                    <div className="text-3xl font-bold text-primary mb-1">{stat.number}</div>
                    <div className="text-sm text-muted-foreground">{stat.label}</div>
                  </CardContent>
                </Card>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16 fade-in-up">
            <h2 className="text-3xl sm:text-4xl font-bold mb-4">Powerful Features for Legal Professionals</h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Everything you need to analyze, understand, and act on legal documents efficiently.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <Card key={index} className={`text-center hover-lift hover-glow fade-in-up-delay-${index + 1}`}>
                <CardHeader>
                  <div
                    className={`mx-auto mb-4 p-4 ${feature.bgColor} rounded-full w-fit float-animation float-delay-${index + 1}`}
                  >
                    <feature.icon className={`h-8 w-8 ${feature.color}`} />
                  </div>
                  <CardTitle className="text-xl">{feature.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-base">{feature.description}</CardDescription>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-muted/30 dotted-background">
        <div className="max-w-7xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div className="slide-in-left">
              <h2 className="text-3xl sm:text-4xl font-bold mb-6">Why Legal Professionals Choose LegalAI</h2>
              <p className="text-lg text-muted-foreground mb-8">
                Built specifically for lawyers, paralegals, and legal teams who need accurate, reliable document
                analysis with professional-grade security.
              </p>
              <div className="space-y-4">
                {benefits.map((benefit, index) => (
                  <div key={index} className={`flex items-start space-x-3 fade-in-up-delay-${index + 1}`}>
                    <div className="p-1 bg-primary/10 rounded-full">
                      <benefit.icon className="h-5 w-5 text-primary" />
                    </div>
                    <span className="text-base">{benefit.text}</span>
                  </div>
                ))}
              </div>
            </div>
            <div className="lg:order-first slide-in-right">
              <Card className="p-8 hover-glow">
                <div className="space-y-6">
                  <div className="flex items-center space-x-4 hover-scale">
                    <div className="p-2 bg-blue-500/10 rounded-full">
                      <Users className="h-8 w-8 text-blue-500" />
                    </div>
                    <div>
                      <h3 className="font-semibold">Trusted by 500+ Legal Firms</h3>
                      <p className="text-muted-foreground">From solo practitioners to large firms</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-4 hover-scale">
                    <div className="p-2 bg-green-500/10 rounded-full">
                      <Shield className="h-8 w-8 text-green-500" />
                    </div>
                    <div>
                      <h3 className="font-semibold">Bank-Level Security</h3>
                      <p className="text-muted-foreground">SOC 2 compliant with end-to-end encryption</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-4 hover-scale">
                    <div className="p-2 bg-purple-500/10 rounded-full">
                      <TrendingUp className="h-8 w-8 text-purple-500" />
                    </div>
                    <div>
                      <h3 className="font-semibold">Save 15+ Hours Weekly</h3>
                      <p className="text-muted-foreground">Average time saved per legal professional</p>
                    </div>
                  </div>
                </div>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 animated-dots">
        <div className="max-w-4xl mx-auto text-center">
          <div className="fade-in-up">
            <h2 className="text-3xl sm:text-4xl font-bold mb-6">Ready to Transform Your Legal Practice?</h2>
            <p className="text-xl text-muted-foreground mb-8">
              Join thousands of legal professionals who trust LegalAI for their document analysis needs.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/signup">
                <Button size="lg" className="text-lg px-8 hover-lift pulse-glow">
                  <Sparkles className="mr-2 h-5 w-5" />
                  Start Your Free Trial
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
              <Link href="/about">
                <Button variant="outline" size="lg" className="text-lg px-8 bg-transparent hover-glow">
                  <BookOpen className="mr-2 h-5 w-5" />
                  Learn More
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}
