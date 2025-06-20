import React from "react";

export function Badge({ className = "", variant = "default", ...props }) {
  const variantClasses = {
    default: "border-transparent bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200",
    secondary: "border-transparent bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200",
    destructive: "border-transparent bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200",
    outline: "border border-slate-300 dark:border-slate-600 text-slate-700 dark:text-slate-300",
  };
  return (
    <span className={`inline-flex items-center rounded-full border px-3 py-1 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-2 ${variantClasses[variant] || variantClasses.default} ${className}`}
      {...props}
    />
  );
} 