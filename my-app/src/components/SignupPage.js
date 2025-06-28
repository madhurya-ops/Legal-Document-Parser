import React, { useState } from "react";
import { Card, CardContent } from "./ui/card";
import { Button } from "./ui/button";
import { Badge } from "./ui/badge";
import ThemeToggle from "./ThemeToggle";
import { signupUser } from "../api";
import { Scale, Loader2, Eye, EyeOff } from "lucide-react";
import { useNavigate } from "react-router-dom";

export default function SignupPage() {
  const [form, setForm] = useState({ username: "", email: "", password: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const navigate = useNavigate();

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
      await signupUser(form.username, form.email, form.password);
      setSuccess("Signup successful! Please log in.");
      setTimeout(() => navigate("/login"), 1200);
    } catch (err) {
      setError(err.message || "Signup failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen bg-slate-50 dark:bg-slate-900 bg-dots transition-colors duration-300 relative overflow-hidden items-center justify-center">
      <div className="absolute inset-0 pointer-events-none bg-dots opacity-80 dark:opacity-50 animate-fade-in" />
      <Card className="w-full max-w-md mx-auto shadow-2xl rounded-3xl bg-white/95 dark:bg-slate-900/95 border border-slate-200/60 dark:border-slate-700/60 backdrop-blur-lg animate-fade-in-up relative overflow-hidden">
        <CardContent className="p-8 sm:p-10 flex flex-col gap-7">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-3">
              <Scale className="w-7 h-7 text-blue-600 dark:text-blue-400" />
              <span className="text-xl font-bold text-slate-900 dark:text-slate-100 tracking-tight">LegalDoc</span>
            </div>
            <ThemeToggle />
          </div>
          <h2 className="text-2xl font-extrabold text-slate-900 dark:text-slate-100 mb-2 text-center tracking-tight animate-fade-in-up">
            Create your account
          </h2>
          <form className="space-y-6 animate-fade-in-up" onSubmit={handleSubmit} autoComplete="off">
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
                className="w-full rounded-xl border border-slate-300 dark:border-slate-600 bg-white/90 dark:bg-slate-800/90 px-4 py-3 text-lg text-slate-900 dark:text-slate-100 placeholder:text-slate-500 dark:placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-400 dark:focus:ring-blue-500 transition-all duration-300 shadow-sm hover:shadow-lg"
                placeholder="Your username"
              />
            </div>
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
                className="w-full rounded-xl border border-slate-300 dark:border-slate-600 bg-white/90 dark:bg-slate-800/90 px-4 py-3 text-lg text-slate-900 dark:text-slate-100 placeholder:text-slate-500 dark:placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-400 dark:focus:ring-blue-500 transition-all duration-300 shadow-sm hover:shadow-lg"
                placeholder="you@example.com"
              />
            </div>
            <div className="relative">
              <label className="block text-base font-medium text-slate-700 dark:text-slate-300 mb-1" htmlFor="password">Password</label>
              <input
                id="password"
                name="password"
                type={showPassword ? "text" : "password"}
                autoComplete="new-password"
                required
                value={form.password}
                onChange={handleChange}
                className="w-full rounded-xl border border-slate-300 dark:border-slate-600 bg-white/90 dark:bg-slate-800/90 px-4 py-3 text-lg text-slate-900 dark:text-slate-100 placeholder:text-slate-500 dark:placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-400 dark:focus:ring-blue-500 transition-all duration-300 shadow-sm hover:shadow-lg pr-12"
                placeholder="Create a password"
              />
              <button
                type="button"
                tabIndex={-1}
                className="absolute right-3 top-[65%] -translate-y-[65%] flex items-center text-slate-400 hover:text-blue-500 dark:hover:text-blue-400 transition-colors"
                onClick={() => setShowPassword((v) => !v)}
                aria-label={showPassword ? "Hide password" : "Show password"}
              >
                {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
              </button>
            </div>
            {error && <Badge variant="destructive" className="w-full text-center animate-fade-in-up text-base py-2">{error}</Badge>}
            {success && <Badge variant="default" className="w-full text-center animate-fade-in-up text-base py-2">{success}</Badge>}
            <Button
              type="submit"
              className="w-full bg-blue-600 hover:bg-blue-700 text-white rounded-xl py-3 text-lg font-semibold transition-all duration-300 hover:scale-105 disabled:opacity-60 shadow-md animate-fade-in-up"
              disabled={loading}
            >
              {loading ? <Loader2 className="w-5 h-5 animate-spin mx-auto" /> : "Sign Up"}
            </Button>
          </form>
          <div className="flex items-center justify-center mt-2 animate-fade-in-up">
            <span className="text-base text-slate-600 dark:text-slate-400">
              Already have an account?
            </span>
            <button
              className="ml-2 text-blue-600 dark:text-blue-400 hover:underline text-base font-semibold transition-colors duration-200"
              onClick={() => navigate("/login")}
              disabled={loading}
            >
              Sign In
            </button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
} 