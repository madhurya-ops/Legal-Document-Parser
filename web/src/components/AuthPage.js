import React, { useState } from "react";
import { useAuth0 } from "@auth0/auth0-react";
import { Card, CardContent, CardHeader, CardFooter } from "./ui/card";
import { Button } from "./ui/button";
import { Badge } from "./ui/badge";
import ThemeToggle from "./ThemeToggle";
import { Scale, Loader2, Eye, EyeOff, FileText, Sparkles, ArrowRight } from "lucide-react";

// Google Icon Component
const GoogleIcon = ({ className = "w-5 h-5" }) => (
  <svg className={className} viewBox="0 0 24 24" fill="currentColor">
    <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
    <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
    <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
    <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
  </svg>
);

// Apple Icon Component
const AppleIcon = ({ className = "w-5 h-5" }) => (
  <svg className={className} viewBox="0 0 24 24" fill="currentColor">
    <path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M13 3.5c.73-.83 1.94-1.46 2.94-1.5.13 1.17-.34 2.35-1.04 3.19-.69.85-1.83 1.51-2.95 1.42-.15-1.15.41-2.35 1.05-3.11z"/>
  </svg>
);

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
  const { 
    loginWithPopup, 
    isAuthenticated, 
    user, 
    isLoading, 
    error: auth0Error 
  } = useAuth0();
  const [mode, setMode] = useState("login");
  const [form, setForm] = useState({ username: "", email: "", password: "", confirmPassword: "" });
  const [loading, setLoading] = useState(false);
  const [socialLoading, setSocialLoading] = useState(null); // Track which social button is loading
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

  // Auth0 Authentication API helper
  const authenticateWithAuth0 = async (email, password) => {
    const response = await fetch(`https://dev-8oivjmih178u6qpg.us.auth0.com/oauth/token`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        grant_type: 'password',
        username: email,
        password: password,
        client_id: 'USWlBGBM57kpWY8L5g1BTwYZ2uUArTAF',
        scope: 'openid profile email',
        audience: 'https://legaldoc-api'
      })
    });
    
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.error_description || 'Authentication failed');
    }
    
    return data;
  };

  // Auth0 Signup API helper
  const signupWithAuth0 = async (email, password, username) => {
    const response = await fetch(`https://dev-8oivjmih178u6qpg.us.auth0.com/dbconnections/signup`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        client_id: 'USWlBGBM57kpWY8L5g1BTwYZ2uUArTAF',
        connection: 'Username-Password-Authentication',
        email: email,
        password: password,
        username: username
      })
    });
    
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.description || 'Signup failed');
    }
    
    return data;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setSuccess("");
    
    try {
      if (mode === "login") {
        // Use Auth0 API for email/password login
        const authResult = await authenticateWithAuth0(form.email, form.password);
        
        // Store tokens and redirect to dashboard
        localStorage.setItem('auth0_access_token', authResult.access_token);
        localStorage.setItem('auth0_id_token', authResult.id_token);
        
        // Trigger authentication success
        if (onAuthSuccess) {
          onAuthSuccess();
        }
        
      } else {
        // Use Auth0 API for signup
        await signupWithAuth0(form.email, form.password, form.username);
        setSuccess("Account created successfully! Please log in.");
        setMode("login");
        setForm({ username: "", email: form.email, password: "", confirmPassword: "" });
      }
    } catch (err) {
      console.error('Auth error:', err);
      setError(err.message || parseErrorMessage(err, mode));
    } finally {
      setLoading(false);
    }
  };

  const handleSocialLogin = async (provider) => {
    try {
      setSocialLoading(provider);
      setError("");
      setSuccess("");

      const auth0Domain = 'dev-8oivjmih178u6qpg.us.auth0.com'; // Update with your Auth0 Domain
      const clientId = 'USWlBGBM57kpWY8L5g1BTwYZ2uUArTAF'; // Update with your Auth0 Client ID
      const redirectUri = window.location.origin; // Your application's redirect URI
      
      // Map provider to Auth0 connection
      const connectionMap = {
        google: 'google-oauth2',
        apple: 'apple'
      };
      
      const connection = connectionMap[provider];
      const authUrl = `https://${auth0Domain}/authorize?response_type=code&client_id=${clientId}&redirect_uri=${redirectUri}&connection=${connection}&scope=openid%20profile%20email&screen_hint=login`;

      window.location.href = authUrl;
    } catch (err) {
      console.error(`${provider} login error:`, err);
      setError(`Failed to connect with ${provider}. Please try again.`);
    } finally {
      setSocialLoading(null);
    }
  };

  // If user is authenticated, the parent component will handle the redirect
  if (isAuthenticated) {
    return null;
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
            <Button 
              variant="outline" 
              className="w-full bg-transparent hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors duration-200 relative" 
              onClick={() => handleSocialLogin('google')}
              disabled={socialLoading !== null || loading}
            >
              {socialLoading === 'google' ? (
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              ) : (
                <GoogleIcon className="mr-2 h-4 w-4" />
              )}
              Google
            </Button>
            <Button 
              variant="outline" 
              className="w-full bg-transparent hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors duration-200 relative" 
              onClick={() => handleSocialLogin('apple')}
              disabled={socialLoading !== null || loading}
            >
              {socialLoading === 'apple' ? (
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              ) : (
                <AppleIcon className="mr-2 h-4 w-4" />
              )}
              Apple
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