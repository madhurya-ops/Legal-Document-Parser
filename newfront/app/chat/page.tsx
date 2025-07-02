"use client"

import type React from "react"

import { useState, useRef } from "react"
import {
  Send,
  Upload,
  FileText,
  Paperclip,
  Download,
  Calendar,
  CheckCircle2,
  Brain,
  Zap,
  Clock,
  AlertCircle,
  Sparkles,
  FileCheck,
  TrendingUp,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Textarea } from "@/components/ui/textarea"

interface Message {
  id: string
  type: "user" | "assistant"
  content: string
  timestamp: Date
  documents?: string[]
}

interface DocumentAnalysis {
  summary: string
  keyDates: { date: string; description: string }[]
  nextSteps: string[]
  legalSections: string[]
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      type: "assistant",
      content:
        "Hello! I'm your legal document analysis assistant. Upload a document to get started, or ask me any questions about legal documents.",
      timestamp: new Date(),
    },
  ])
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([])
  const [analysis, setAnalysis] = useState<DocumentAnalysis | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || [])
    setUploadedFiles((prev) => [...prev, ...files])

    // Simulate document analysis
    setTimeout(() => {
      const mockAnalysis: DocumentAnalysis = {
        summary:
          "This employment agreement outlines the terms of employment for a Senior Software Engineer position. The contract includes standard clauses for compensation, benefits, confidentiality, and termination procedures.",
        keyDates: [
          { date: "2024-01-15", description: "Employment start date" },
          { date: "2024-07-15", description: "First performance review due" },
          { date: "2024-12-31", description: "Contract renewal deadline" },
        ],
        nextSteps: [
          "Review compensation package details",
          "Ensure all parties sign and date the agreement",
          "File executed contract in employee records",
          "Schedule onboarding session",
        ],
        legalSections: [
          "Section 3: Compensation and Benefits",
          "Section 7: Confidentiality Agreement",
          "Section 12: Termination Clause",
        ],
      }
      setAnalysis(mockAnalysis)
    }, 1500)
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim()) return

    const userMessage: Message = {
      id: Date.now().toString(),
      type: "user",
      content: input,
      timestamp: new Date(),
      documents: uploadedFiles.map((f) => f.name),
    }

    setMessages((prev) => [...prev, userMessage])
    setInput("")
    setIsLoading(true)

    // Simulate AI response
    setTimeout(() => {
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: "assistant",
        content:
          "Based on your uploaded documents, I can see this is an employment agreement. The contract appears to be comprehensive and includes standard provisions for a senior-level position. Key areas to focus on include the compensation structure in Section 3, which offers competitive base salary plus equity participation. The confidentiality clause in Section 7 is standard but broadly written. Would you like me to elaborate on any specific aspect?",
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, assistantMessage])
      setIsLoading(false)
    }, 2000)
  }

  return (
    <div className="min-h-screen bg-background dotted-background">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid lg:grid-cols-4 gap-6">
          {/* Main Chat Area */}
          <div className="lg:col-span-3 space-y-6">
            {/* Header */}
            <Card className="hover-glow fade-in-up">
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <div className="p-2 bg-primary/10 rounded-full">
                    <Brain className="h-6 w-6 text-primary float-animation" />
                  </div>
                  <span>Legal Document Analysis Chat</span>
                  <Badge variant="secondary" className="ml-auto">
                    <Sparkles className="h-3 w-3 mr-1" />
                    AI Powered
                  </Badge>
                </CardTitle>
              </CardHeader>
            </Card>

            {/* Messages */}
            <Card className="min-h-[500px] hover-glow fade-in-up-delay-1">
              <CardContent className="p-6">
                <div className="space-y-4 mb-4 max-h-96 overflow-y-auto chat-scroll">
                  {messages.map((message, index) => (
                    <div
                      key={message.id}
                      className={`flex ${message.type === "user" ? "justify-end" : "justify-start"} fade-in-up`}
                    >
                      <div
                        className={`max-w-[80%] p-4 rounded-lg hover-scale ${
                          message.type === "user" ? "bg-primary text-primary-foreground" : "bg-muted hover-glow"
                        }`}
                      >
                        <p className="text-sm">{message.content}</p>
                        {message.documents && (
                          <div className="mt-2 flex flex-wrap gap-1">
                            {message.documents.map((doc, index) => (
                              <Badge key={index} variant="secondary" className="text-xs hover-scale">
                                <Paperclip className="h-3 w-3 mr-1" />
                                {doc}
                              </Badge>
                            ))}
                          </div>
                        )}
                        <p className="text-xs opacity-70 mt-2">{message.timestamp.toLocaleTimeString()}</p>
                      </div>
                    </div>
                  ))}
                  {isLoading && (
                    <div className="flex justify-start">
                      <div className="bg-muted p-4 rounded-lg hover-glow">
                        <div className="flex items-center space-x-2">
                          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-primary"></div>
                          <Zap className="h-4 w-4 text-primary icon-bounce" />
                          <span className="text-sm">Analyzing with AI...</span>
                        </div>
                      </div>
                    </div>
                  )}
                </div>

                {/* Upload Area */}
                {uploadedFiles.length > 0 && (
                  <div className="mb-4 p-4 bg-muted/50 rounded-lg hover-glow slide-in-bottom">
                    <h4 className="font-medium mb-2 flex items-center">
                      <FileCheck className="h-4 w-4 mr-2 text-green-500" />
                      Uploaded Documents:
                    </h4>
                    <div className="space-y-2">
                      {uploadedFiles.map((file, index) => (
                        <div key={index} className="flex items-center space-x-2 hover-scale">
                          <FileText className="h-4 w-4 text-muted-foreground" />
                          <span className="text-sm">{file.name}</span>
                          <Badge variant="outline" className="text-xs">
                            {(file.size / 1024).toFixed(1)} KB
                          </Badge>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Input Area */}
                <div className="space-y-3">
                  <div className="flex space-x-2">
                    <Button
                      variant="outline"
                      size="icon"
                      onClick={() => fileInputRef.current?.click()}
                      className="hover-lift hover-glow"
                    >
                      <Upload className="h-4 w-4" />
                    </Button>
                    <form onSubmit={handleSubmit} className="flex-1 flex space-x-2">
                      <Textarea
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Ask questions about your legal documents..."
                        className="min-h-[60px] resize-none hover-glow"
                        onKeyDown={(e) => {
                          if (e.key === "Enter" && !e.shiftKey) {
                            e.preventDefault()
                            handleSubmit(e)
                          }
                        }}
                      />
                      <Button type="submit" disabled={isLoading || !input.trim()} className="hover-lift pulse-glow">
                        <Send className="h-4 w-4" />
                      </Button>
                    </form>
                  </div>
                  <input
                    ref={fileInputRef}
                    type="file"
                    multiple
                    accept=".pdf,.doc,.docx,.txt"
                    onChange={handleFileUpload}
                    className="hidden"
                  />
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Analysis Sidebar */}
          <div className="space-y-6">
            {analysis && (
              <>
                {/* Document Summary */}
                <Card className="hover-glow fade-in-up-delay-2">
                  <CardHeader>
                    <CardTitle className="text-lg flex items-center space-x-2">
                      <FileText className="h-5 w-5 text-blue-500" />
                      <span>Document Summary</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-muted-foreground">{analysis.summary}</p>
                  </CardContent>
                </Card>

                {/* Key Dates */}
                <Card className="hover-glow fade-in-up-delay-3">
                  <CardHeader>
                    <CardTitle className="text-lg flex items-center space-x-2">
                      <Calendar className="h-5 w-5 text-green-500 float-animation" />
                      <span>Key Dates</span>
                      <Badge variant="secondary" className="ml-auto">
                        {analysis.keyDates.length}
                      </Badge>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      {analysis.keyDates.map((item, index) => (
                        <div key={index} className="flex flex-col space-y-1 hover-scale p-2 rounded hover:bg-muted/50">
                          <div className="font-medium text-sm flex items-center">
                            <Clock className="h-3 w-3 mr-2 text-orange-500" />
                            {item.date}
                          </div>
                          <div className="text-xs text-muted-foreground ml-5">{item.description}</div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>

                {/* Next Steps */}
                <Card className="hover-glow fade-in-up-delay-4">
                  <CardHeader>
                    <CardTitle className="text-lg flex items-center space-x-2">
                      <CheckCircle2 className="h-5 w-5 text-purple-500" />
                      <span>Next Steps</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2">
                      {analysis.nextSteps.map((step, index) => (
                        <div
                          key={index}
                          className="flex items-start space-x-2 hover-scale p-2 rounded hover:bg-muted/50"
                        >
                          <div className="w-2 h-2 bg-primary rounded-full mt-2 flex-shrink-0 pulse-glow"></div>
                          <span className="text-sm">{step}</span>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>

                {/* Legal Sections */}
                <Card className="hover-glow fade-in-up-delay-5">
                  <CardHeader>
                    <CardTitle className="text-lg flex items-center space-x-2">
                      <AlertCircle className="h-5 w-5 text-red-500" />
                      <span>Referenced Sections</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2">
                      {analysis.legalSections.map((section, index) => (
                        <Badge
                          key={index}
                          variant="outline"
                          className="block text-left text-xs p-2 hover-scale hover-glow"
                        >
                          {section}
                        </Badge>
                      ))}
                    </div>
                  </CardContent>
                </Card>

                {/* Export Options */}
                <Card className="hover-glow fade-in-up-delay-6">
                  <CardHeader>
                    <CardTitle className="text-lg flex items-center space-x-2">
                      <TrendingUp className="h-5 w-5 text-indigo-500" />
                      <span>Export Analysis</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2">
                      <Button
                        variant="outline"
                        size="sm"
                        className="w-full justify-start bg-transparent hover-lift hover-glow"
                      >
                        <Download className="h-4 w-4 mr-2" />
                        Export as PDF
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        className="w-full justify-start bg-transparent hover-lift hover-glow"
                      >
                        <Download className="h-4 w-4 mr-2" />
                        Export as Word
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
