import React, { useState } from "react";
import { Button } from "./ui/button";
import { Card } from "./ui/card";
import { Badge } from "./ui/badge";
import { Globe, ChevronDown, Check } from "lucide-react";

const LanguageSelector = () => {
  const [selectedLanguage, setSelectedLanguage] = useState("en");
  const [isOpen, setIsOpen] = useState(false);

  const languages = [
    { code: "en", name: "English", flag: "🇺🇸", status: "active" },
    { code: "hi", name: "Hindi", flag: "🇮🇳", status: "coming-soon" },
    { code: "mr", name: "Marathi", flag: "🇮🇳", status: "coming-soon" },
    { code: "ta", name: "Tamil", flag: "🇮🇳", status: "coming-soon" },
    { code: "te", name: "Telugu", flag: "🇮🇳", status: "coming-soon" },
    { code: "bn", name: "Bengali", flag: "🇮🇳", status: "coming-soon" }
  ];

  const selectedLang = languages.find(lang => lang.code === selectedLanguage);

  const handleLanguageSelect = (languageCode) => {
    if (languageCode === "en") {
      setSelectedLanguage(languageCode);
      setIsOpen(false);
    }
    // For other languages, just close the dropdown (they're not implemented yet)
    // setIsOpen(false);
  };

  return (
    <div className="relative">
      <h4 className="text-sm font-medium text-foreground mb-2">Language</h4>
      
      {/* Current Selection */}
      <Button
        variant="outline"
        size="sm"
        className="w-full justify-between text-xs h-8"
        onClick={() => setIsOpen(!isOpen)}
      >
        <div className="flex items-center gap-2">
          <Globe className="w-3 h-3" />
          <span>{selectedLang?.flag}</span>
          <span>{selectedLang?.name}</span>
        </div>
        <ChevronDown className={`w-3 h-3 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
      </Button>

      {/* Dropdown */}
      {isOpen && (
        <>
          {/* Overlay */}
          <div 
            className="fixed inset-0 z-10"
            onClick={() => setIsOpen(false)}
          />
          
          {/* Dropdown Menu */}
          <Card className="absolute top-full mt-1 w-full z-20 p-2 bg-background/95 backdrop-blur-lg border border-border shadow-lg">
            <div className="space-y-1">
              {languages.map((language) => (
                <button
                  key={language.code}
                  className={`w-full flex items-center justify-between p-2 rounded text-xs hover:bg-muted transition-colors ${
                    selectedLanguage === language.code ? 'bg-primary/10' : ''
                  } ${
                    language.status === 'coming-soon' ? 'opacity-60 cursor-not-allowed' : 'cursor-pointer'
                  }`}
                  onClick={() => handleLanguageSelect(language.code)}
                  disabled={language.status === 'coming-soon'}
                >
                  <div className="flex items-center gap-2">
                    <span>{language.flag}</span>
                    <span>{language.name}</span>
                    {language.status === 'coming-soon' && (
                      <Badge variant="secondary" className="text-xs py-0 px-1">
                        Soon
                      </Badge>
                    )}
                  </div>
                  {selectedLanguage === language.code && (
                    <Check className="w-3 h-3 text-primary" />
                  )}
                </button>
              ))}
            </div>
            
            <div className="mt-2 pt-2 border-t border-border">
              <p className="text-xs text-muted-foreground text-center">
                More languages coming soon
              </p>
            </div>
          </Card>
        </>
      )}
    </div>
  );
};

export default LanguageSelector;
