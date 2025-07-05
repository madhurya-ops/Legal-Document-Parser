import React from "react";

export function Card({ className = "", children, ...props }) {
  return (
    <div className={`rounded-2xl shadow border border-border bg-background/80 backdrop-blur-md ${className}`} {...props}>
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

export function CardHeader({ className = "", children, ...props }) {
  return (
    <div className={`p-4 sm:p-6 border-b border-border/60 flex flex-col items-center justify-center gap-2 ${className}`} {...props}>
      {children}
    </div>
  );
}

export function CardFooter({ className = "", children, ...props }) {
  return (
    <div className={`p-4 sm:p-6 border-t border-border/60 flex flex-col items-center justify-center gap-2 ${className}`} {...props}>
      {children}
    </div>
  );
} # update Sun Jul  6 02:56:34 IST 2025
