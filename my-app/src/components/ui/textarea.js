import React from "react";

export const Textarea = React.forwardRef(({ className = "", ...props }, ref) => {
  return (
    <textarea
      className={`flex w-full rounded-xl border border-border bg-background px-3 py-2 text-base text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary transition-colors duration-300 resize-none ${className}`}
      ref={ref}
      {...props}
    />
  );
});
Textarea.displayName = "Textarea"; 