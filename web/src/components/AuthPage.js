import React, { useState } from "react";
import { useAuth0 } from "@auth0/auth0-react";
import { Card, CardContent, CardHeader, CardFooter } from "./ui/card";
import { Button } from "./ui/button";
import { Badge } from "./ui/badge";
import ThemeToggle from "./ThemeToggle";
import { loginUser, signupUser, storeToken, getCurrentUser } from "../api";
import { Scale, Loader2, Eye, EyeOff, FileText, Sparkles, ArrowRight } from "lucide-react";

function parseErrorMessage(err, mode) {
  if (!err || !err.message) return "An error occurred. Please try again.";
  const msg = err.message;
  if (msg.includes("Incorrect email or password")) return "Incorrect email or password. Please check your credentials.";
  if (msg.includes("Email already registered")) return "This email is already registered. Please log in or use another email.";
  if (msg.includes("Username already taken")) return "This username is already taken. Please choose another.";
  if (msg.includes("Password must")) return msg;
  if (msg.includes("value is not a valid email address")) return "Please enter a valid email address.";
  if (msg.includes("422")) return mode === "signup" ? "Please fill all fields correctly. Password must be at least 8 characters, with uppercase, lowercase, and a digit." : "Please enter your email and password.";
  return msg;
}

export default function AuthPage({ onAuthSuccess, onBack, cardSize = "xl" }) {
  const { loginWithRedirect, isAuthenticated, user, isLoading, error: auth0Error } = useAuth0();
  const [mode, setMode] = useState("login");
  const [form, setForm] = useState({ username: "", email: "", password: "", confirmPassword: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);

  const handleChange = (e) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
    setError("");
    setSuccess("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setSuccess("");
    try {
      if (mode === "login") {
        // Use Auth0 login
        await loginWithRedirect();
        // Optionally, handle post-login logic here if needed
      } else {
        // Keep your existing signup logic if you want to support local signup
        await signupUser(form.username, form.email, form.password);
        setSuccess("Signup successful! Please log in.");
        setMode("login");
        setForm({ username: "", email: form.email, password: "", confirmPassword: "" });
      }
    } catch (err) {
      setError(parseErrorMessage(err, mode));
    } finally {
      setLoading(false);
    }
  };

  if (isAuthenticated) {
    return <div>You're already logged in!</div>;
  }

  return (
    <Card className="w-full max-w-md mx-auto shadow-2xl rounded-3xl bg-background/90 border border-border animate-fade-in-up relative overflow-hidden my-12">
      {/* Back button (top left) */}
      {onBack && (
        <button
          onClick={onBack}
          className="absolute top-4 left-4 p-2 rounded-full bg-background/80 border border-border shadow hover:bg-primary/10 transition-colors z-10"
          title="Back to Home"
          aria-label="Back to Home"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2" className="text-primary"><path strokeLinecap="round" strokeLinejoin="round" d="M15 19l-7-7 7-7" /></svg>
        </button>
      )}
      <CardHeader className="text-center">
        <div className="mx-auto mb-4 p-3 bg-primary/10 rounded-full w-fit">
          <Scale className="h-8 w-8 text-primary" />
        </div>
        <h2 className="text-2xl font-bold mb-1">{mode === "login" ? "Welcome Back" : "Create Your Account"}</h2>
        <p className="text-muted-foreground mb-2">
          {mode === "login"
            ? "Sign in to your LegalDoc account to continue analyzing legal documents"
            : "Join LegalDoc and start analyzing legal documents with AI assistance"}
        </p>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          {mode === "signup" && (
            <div>
              <label htmlFor="username" className="block text-base font-medium text-foreground mb-1">Username</label>
              <input
                id="username"
                name="username"
                type="text"
                autoComplete="username"
                required
                value={form.username}
                onChange={handleChange}
                className="w-full rounded-xl border border-border bg-background/80 px-4 py-3 text-lg text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary transition-colors duration-300 shadow-sm"
                placeholder="Your username"
              />
            </div>
          )}
          <div>
            <label htmlFor="email" className="block text-base font-medium text-foreground mb-1">Email</label>
            <input
              id="email"
              name="email"
              type="email"
              autoComplete="email"
              required
              value={form.email}
              onChange={handleChange}
              className="w-full rounded-xl border border-border bg-background/80 px-4 py-3 text-lg text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary transition-colors duration-300 shadow-sm"
              placeholder="you@example.com"
            />
          </div>
          <div className="relative">
            <label htmlFor="password" className="block text-base font-medium text-foreground mb-1">Password</label>
            <input
              id="password"
              name="password"
              type={showPassword ? "text" : "password"}
              autoComplete={mode === "login" ? "current-password" : "new-password"}
              required
              value={form.password}
              onChange={handleChange}
              className="w-full rounded-xl border border-border bg-background/80 px-4 py-3 text-lg text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary transition-colors duration-300 shadow-sm pr-12"
              placeholder={mode === "login" ? "Your password" : "Create a password"}
            />
            <button
              type="button"
              tabIndex={-1}
              className="absolute right-3 top-[65%] -translate-y-[65%] flex items-center text-muted-foreground hover:text-primary transition-colors"
              onClick={() => setShowPassword((v) => !v)}
              aria-label={showPassword ? "Hide password" : "Show password"}
            >
              {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
            </button>
          </div>
          {mode === "signup" && (
            <div className="relative">
              <label htmlFor="confirmPassword" className="block text-base font-medium text-foreground mb-1">Confirm Password</label>
              <input
                id="confirmPassword"
                name="confirmPassword"
                type={showConfirmPassword ? "text" : "password"}
                required
                value={form.confirmPassword}
                onChange={handleChange}
                className="w-full rounded-xl border border-border bg-background/80 px-4 py-3 text-lg text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary transition-colors duration-300 shadow-sm pr-12"
                placeholder="Confirm your password"
              />
              <button
                type="button"
                tabIndex={-1}
                className="absolute right-3 top-[65%] -translate-y-[65%] flex items-center text-muted-foreground hover:text-primary transition-colors"
                onClick={() => setShowConfirmPassword((v) => !v)}
                aria-label={showConfirmPassword ? "Hide password" : "Show password"}
              >
                {showConfirmPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
              </button>
            </div>
          )}
          {mode === "login" && (
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <input id="remember" type="checkbox" className="rounded border-gray-300" checked={rememberMe} onChange={e => setRememberMe(e.target.checked)} />
                <label htmlFor="remember" className="text-sm">Remember me</label>
              </div>
              <button type="button" className="text-sm text-primary hover:underline" tabIndex={0} disabled>Forgot password?</button>
            </div>
          )}
          {error && <div className="w-full text-center text-red-600 text-base py-2 animate-fade-in-up">{error}</div>}
          {success && <div className="w-full text-center text-green-600 text-base py-2 animate-fade-in-up">{success}</div>}
          {auth0Error && <div className="w-full text-center text-red-600 text-base py-2 animate-fade-in-up">{auth0Error.message}</div>}
          <Button
            type="submit"
            className="w-full rounded-xl py-3 text-lg font-semibold transition-all duration-300 hover:scale-105 disabled:opacity-60 shadow-md"
            disabled={loading}
          >
            {loading ? <Loader2 className="w-5 h-5 animate-spin mx-auto" /> : (mode === "login" ? "Sign In" : "Sign Up")}
          </Button>
        </form>
        <div className="mt-6">
          <div className="text-center text-sm text-muted-foreground">Or continue with</div>
          <div className="mt-4 grid grid-cols-2 gap-3">
            <Button variant="outline" className="w-full bg-transparent" disabled>
              <Sparkles className="mr-2 h-4 w-4" />
              Google
            </Button>
            <Button variant="outline" className="w-full bg-transparent" disabled>
              <Sparkles className="mr-2 h-4 w-4" />
              Microsoft
            </Button>
          </div>
        </div>
      </CardContent>
      <CardFooter className="text-center">
        <p className="text-sm text-muted-foreground">
          {mode === "login"
            ? <>Don't have an account? <button className="text-primary hover:underline font-medium" onClick={() => setMode("signup")}>Sign up for free</button></>
            : <>Already have an account? <button className="text-primary hover:underline font-medium" onClick={() => setMode("login")}>Sign in</button></>}
        </p>
      </CardFooter>
    </Card>
  );
}