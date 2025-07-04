import React from "react";
import { Button } from "./ui/button";
import { Sun, Moon } from "lucide-react";
import { useTheme } from "../ThemeProvider";

export default function ThemeToggle() {
  const { theme, toggleTheme } = useTheme();

  return (
    <Button
      variant="ghost"
      size="icon"
      aria-label={`Switch to ${theme === "light" ? "dark" : "light"} mode`}
      onClick={toggleTheme}
      className="rounded-full border border-border bg-background/90 hover:bg-muted transition-all duration-300 shadow-sm hover:shadow-md hover:scale-105 active:scale-95"
    >
      {theme === "light" ? (
        <Moon className="w-5 h-5 text-foreground transition-all duration-300 hover:rotate-12" />
      ) : (
        <Sun className="w-5 h-5 text-foreground transition-all duration-300 hover:rotate-12" />
      )}
    </Button>
  );
} 