import React from "react";

export function Badge({ className = "", variant = "default", ...props }) {
  const variantClasses = {
    default: "border-transparent bg-muted text-muted-foreground",
    secondary: "border-transparent bg-secondary text-secondary-foreground",
    destructive: "border-transparent bg-destructive text-destructive-foreground",
    outline: "border border-border text-foreground",
  };
  return (
    <span className={`inline-flex items-center rounded-full border px-3 py-1 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 ${variantClasses[variant] || variantClasses.default} ${className}`}
      {...props}
    />
  );
} 
