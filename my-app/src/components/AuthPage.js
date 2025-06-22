import React, { useState } from "react";
import { Card, CardContent } from "./ui/card";
import { Button } from "./ui/button";
import { Badge } from "./ui/badge";
import ThemeToggle from "./ThemeToggle";
import { loginUser, signupUser, storeToken, getCurrentUser } from "../api";
import { Scale, Loader2, Eye, EyeOff, FileText } from "lucide-react";

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

export default function AuthPage({ onAuthSuccess }) {
  const [mode, setMode] = useState("login"); // 'login' or 'signup'
  const [form, setForm] = useState({ username: "", email: "", password: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [showPassword, setShowPassword] = useState(false);

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
        const data = await loginUser(form.email, form.password);
        storeToken(data.access_token);
        const user = await getCurrentUser(data.access_token);
        setSuccess("Welcome back! Redirecting...");
        setTimeout(() => onAuthSuccess(user), 700);
      } else {
        await signupUser(form.username, form.email, form.password);
        setSuccess("Signup successful! Please log in.");
        setMode("login");
        setForm({ username: "", email: form.email, password: "" });
      }
    } catch (err) {
      setError(parseErrorMessage(err, mode));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen bg-slate-50 dark:bg-slate-900 fade-in-home transition-colors duration-300 bg-dots relative overflow-hidden">
      {/* Left illustration/branding panel (hidden on mobile) */}
      <div className="hidden md:flex flex-col justify-between items-center w-1/2 bg-gradient-to-br from-blue-50/90 via-blue-100/80 to-blue-200/60 dark:from-blue-900/60 dark:via-slate-900/80 dark:to-blue-950/80 p-10 relative z-10 animate-slide-in-left">
        <div className="flex flex-col items-center gap-4 mt-10">
          <Scale className="w-16 h-16 text-blue-600 dark:text-blue-400 drop-shadow-lg" />
          <span className="text-3xl font-extrabold text-slate-900 dark:text-slate-100 tracking-tight drop-shadow-lg">LegalDoc</span>
          <span className="text-lg text-slate-600 dark:text-slate-300 text-center max-w-xs">AI-powered legal document analysis, secure and effortless.</span>
        </div>
        <div className="flex flex-col items-center gap-2 mb-10">
          <FileText className="w-8 h-8 text-blue-400 dark:text-blue-300" />
          <span className="text-base text-slate-500 dark:text-slate-400 text-center">Upload, chat, and analyze your legal docs with confidence.</span>
        </div>
      </div>
      {/* Dot pattern background overlay for extra effect */}
      <div className="absolute inset-0 pointer-events-none bg-dots opacity-60 dark:opacity-40 animate-fade-in" />
      {/* Auth card */}
      <div className="flex flex-1 items-center justify-center relative z-20">
        <Card className="w-full max-w-md mx-auto shadow-2xl rounded-3xl bg-white/90 dark:bg-slate-900/90 border border-slate-200/60 dark:border-slate-700/60 backdrop-blur-lg animate-slide-in-up relative overflow-hidden">
          <CardContent className="p-8 sm:p-10 flex flex-col gap-7">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-3">
                <Scale className="w-7 h-7 text-blue-600 dark:text-blue-400" />
                <span className="text-xl font-bold text-slate-900 dark:text-slate-100 tracking-tight">LegalDoc</span>
              </div>
              <ThemeToggle />
            </div>
            <h2 className="text-2xl font-extrabold text-slate-900 dark:text-slate-100 mb-2 text-center tracking-tight">
              {mode === "login" ? "Sign In to your account" : "Create your account"}
            </h2>
            <form className="space-y-6" onSubmit={handleSubmit} autoComplete="off">
              {mode === "signup" && (
                <div>
                  <label className="block text-base font-medium text-slate-700 dark:text-slate-300 mb-1" htmlFor="username">Username</label>
                  <input
                    id="username"
                    name="username"
                    type="text"
                    autoComplete="username"
                    required
                    value={form.username}
                    onChange={handleChange}
                    className="w-full rounded-xl border border-slate-300 dark:border-slate-600 bg-white/80 dark:bg-slate-800/80 px-4 py-3 text-lg text-slate-900 dark:text-slate-100 placeholder:text-slate-500 dark:placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-400 dark:focus:ring-blue-500 transition-colors duration-300 shadow-sm"
                    placeholder="Your username"
                  />
                </div>
              )}
              <div>
                <label className="block text-base font-medium text-slate-700 dark:text-slate-300 mb-1" htmlFor="email">Email</label>
                <input
                  id="email"
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                  value={form.email}
                  onChange={handleChange}
                  className="w-full rounded-xl border border-slate-300 dark:border-slate-600 bg-white/80 dark:bg-slate-800/80 px-4 py-3 text-lg text-slate-900 dark:text-slate-100 placeholder:text-slate-500 dark:placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-400 dark:focus:ring-blue-500 transition-colors duration-300 shadow-sm"
                  placeholder="you@example.com"
                />
              </div>
              <div className="relative">
                <label className="block text-base font-medium text-slate-700 dark:text-slate-300 mb-1" htmlFor="password">Password</label>
                <input
                  id="password"
                  name="password"
                  type={showPassword ? "text" : "password"}
                  autoComplete={mode === "login" ? "current-password" : "new-password"}
                  required
                  value={form.password}
                  onChange={handleChange}
                  className="w-full rounded-xl border border-slate-300 dark:border-slate-600 bg-white/80 dark:bg-slate-800/80 px-4 py-3 text-lg text-slate-900 dark:text-slate-100 placeholder:text-slate-500 dark:placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-400 dark:focus:ring-blue-500 transition-colors duration-300 shadow-sm pr-12"
                  placeholder={mode === "login" ? "Your password" : "Create a password"}
                />
                <button
                  type="button"
                  tabIndex={-1}
                  className="absolute right-3 top-[65%] -translate-y-[65%] flex items-center text-slate-400 hover:text-blue-500 dark:hover:text-blue-400 transition-colors"
                  onClick={() => setShowPassword((v) => !v)}
                  aria-label={showPassword ? "Hide password" : "Show password"}
                >
                  {showPassword ? (
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-eye w-5 h-5" aria-hidden="true"><path d="M2.062 12.348a1 1 0 0 1 0-.696 10.75 10.75 0 0 1 19.876 0 1 1 0 0 1 0 .696 10.75 10.75 0 0 1-19.876 0"></path><circle cx="12" cy="12" r="3"></circle></svg>
                  ) : (
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-eye-off w-5 h-5" aria-hidden="true"><path d="M17.94 17.94A10.94 10.94 0 0 1 12 19c-5 0-9.27-3.11-10.94-7a10.96 10.96 0 0 1 5.17-5.46"/><path d="M1 1l22 22"/><path d="M9.53 9.53A3 3 0 0 0 12 15a3 3 0 0 0 2.47-5.47"/><path d="M14.47 14.47A3 3 0 0 1 12 9a3 3 0 0 1-2.47 5.47"/></svg>
                  )}
                </button>
              </div>
              {error && <Badge variant="destructive" className="w-full text-center animate-fade-in-up text-base py-2">{error}</Badge>}
              {success && <Badge variant="default" className="w-full text-center animate-fade-in-up text-base py-2">{success}</Badge>}
              <Button
                type="submit"
                className="w-full bg-blue-600 hover:bg-blue-700 text-white rounded-xl py-3 text-lg font-semibold transition-all duration-300 hover:scale-105 disabled:opacity-60 shadow-md"
                disabled={loading}
              >
                {loading ? <Loader2 className="w-5 h-5 animate-spin mx-auto" /> : (mode === "login" ? "Sign In" : "Sign Up")}
              </Button>
            </form>
            <div className="flex items-center justify-center mt-2">
              <span className="text-base text-slate-600 dark:text-slate-400">
                {mode === "login" ? "Don't have an account?" : "Already have an account?"}
              </span>
              <button
                className="ml-2 text-blue-600 dark:text-blue-400 hover:underline text-base font-semibold transition-colors duration-200"
                onClick={() => { setMode(mode === "login" ? "signup" : "login"); setError(""); setSuccess(""); }}
                disabled={loading}
              >
                {mode === "login" ? "Sign Up" : "Sign In"}
              </button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}