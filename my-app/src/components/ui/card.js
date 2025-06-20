import React from "react";

export function Card({ className = "", children, ...props }) {
  return (
    <div className={`rounded-2xl shadow bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 ${className}`} {...props}>
      {children}
    </div>
  );
}

export function CardContent({ className = "", children, ...props }) {
  return (
    <div className={`p-4 sm:p-6 ${className}`} {...props}>
      {children}
    </div>
  );
} 