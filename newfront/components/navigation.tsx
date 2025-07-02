"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { Scale, Menu, X, Home, Sparkles, Users, MessageSquare } from "lucide-react"
import { Button } from "@/components/ui/button"
import { ThemeToggle } from "./theme-toggle"
import { useState } from "react"

export function Navigation() {
  const pathname = usePathname()
  const [isMenuOpen, setIsMenuOpen] = useState(false)

  const navigation = [
    { name: "Home", href: "/", icon: Home },
    { name: "Features", href: "/#features", icon: Sparkles },
    { name: "About", href: "/about", icon: Users },
    { name: "Chat", href: "/chat", icon: MessageSquare },
  ]

  return (
    <nav className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/" className="flex items-center space-x-2 hover-scale">
              <div className="p-1 bg-primary/10 rounded-full">
                <Scale className="h-8 w-8 text-primary float-animation" />
              </div>
              <span className="text-xl font-bold gradient-animate bg-clip-text text-transparent">LegalAI</span>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            {navigation.map((item, index) => (
              <Link
                key={item.name}
                href={item.href}
                className={`flex items-center space-x-1 text-sm font-medium transition-all duration-200 hover:text-primary hover-scale ${
                  pathname === item.href ? "text-primary" : "text-muted-foreground"
                } fade-in-up-delay-${index + 1}`}
              >
                <item.icon className="h-4 w-4" />
                <span>{item.name}</span>
              </Link>
            ))}
          </div>

          <div className="hidden md:flex items-center space-x-4">
            <ThemeToggle />
            <Link href="/login">
              <Button variant="ghost" className="hover-glow">
                Login
              </Button>
            </Link>
            <Link href="/signup">
              <Button className="hover-lift">
                <Sparkles className="mr-2 h-4 w-4" />
                Get Started
              </Button>
            </Link>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden flex items-center space-x-2">
            <ThemeToggle />
            <Button variant="ghost" size="icon" onClick={() => setIsMenuOpen(!isMenuOpen)} className="hover-scale">
              {isMenuOpen ? <X className="h-6 w-6 icon-wiggle" /> : <Menu className="h-6 w-6" />}
            </Button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <div className="md:hidden py-4 space-y-2 slide-in-bottom">
            {navigation.map((item, index) => (
              <Link
                key={item.name}
                href={item.href}
                className={`flex items-center space-x-2 px-3 py-2 text-sm font-medium transition-colors hover:text-primary hover:bg-muted/50 rounded-md fade-in-up-delay-${index + 1}`}
                onClick={() => setIsMenuOpen(false)}
              >
                <item.icon className="h-4 w-4" />
                <span>{item.name}</span>
              </Link>
            ))}
            <div className="px-3 py-2 space-y-2">
              <Link href="/login" onClick={() => setIsMenuOpen(false)}>
                <Button variant="ghost" className="w-full justify-start hover-glow">
                  Login
                </Button>
              </Link>
              <Link href="/signup" onClick={() => setIsMenuOpen(false)}>
                <Button className="w-full hover-lift">
                  <Sparkles className="mr-2 h-4 w-4" />
                  Get Started
                </Button>
              </Link>
            </div>
          </div>
        )}
      </div>
    </nav>
  )
}
