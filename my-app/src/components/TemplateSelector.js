import React, { useState } from "react";
import { Button } from "./ui/button";
import { Card } from "./ui/card";
import { Badge } from "./ui/badge";
import { FileText, ChevronDown, Plus, Clock } from "lucide-react";

const TemplateSelector = () => {
  const [isOpen, setIsOpen] = useState(false);

  const templates = [
    { 
      id: "nda", 
      name: "Non-Disclosure Agreement", 
      category: "Confidentiality",
      description: "Standard NDA template for business partnerships",
      status: "coming-soon"
    },
    { 
      id: "employment", 
      name: "Employment Contract", 
      category: "HR & Employment",
      description: "Comprehensive employment agreement template",
      status: "coming-soon"
    },
    { 
      id: "service", 
      name: "Service Agreement", 
      category: "Business",
      description: "Service provider agreement template",
      status: "coming-soon"
    },
    { 
      id: "lease", 
      name: "Lease Agreement", 
      category: "Real Estate",
      description: "Property lease agreement template",
      status: "coming-soon"
    },
    { 
      id: "partnership", 
      name: "Partnership Agreement", 
      category: "Business",
      description: "Business partnership agreement template",
      status: "coming-soon"
    }
  ];

  const handleTemplateSelect = (template) => {
    // This would trigger template creation flow
    console.log('Selected template:', template.name);
    setIsOpen(false);
  };

  return (
    <div className="w-full">
      {/* Coming Soon Badge */}
      <div className="mb-4">
        <Badge variant="secondary" className="text-sm px-3 py-1">
          <Clock className="w-4 h-4 mr-2" />
          Feature Coming Soon
        </Badge>
      </div>
      
      {/* Template Selector Button */}
      <Button
        variant="outline"
        size="default"
        className="w-full justify-between mb-4 h-10"
        onClick={() => setIsOpen(!isOpen)}
      >
        <div className="flex items-center gap-2">
          <FileText className="w-4 h-4" />
          <span>Draft New Document</span>
        </div>
        <ChevronDown className={`w-4 h-4 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
      </Button>

      {/* Templates Grid */}
      <div className="space-y-3">
        {templates.map((template) => (
          <Card
            key={template.id}
            className="p-4 opacity-60 cursor-not-allowed transition-all hover:bg-muted/30"
            onClick={() => handleTemplateSelect(template)}
          >
            <div className="flex items-start gap-3">
              <div className="p-2 bg-primary/10 rounded-lg">
                <FileText className="w-4 h-4 text-primary" />
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-2">
                  <h6 className="text-sm font-medium text-foreground truncate">
                    {template.name}
                  </h6>
                  <Badge variant="secondary" className="text-xs">
                    Soon
                  </Badge>
                </div>
                <p className="text-sm text-muted-foreground mb-2 leading-relaxed">
                  {template.description}
                </p>
                <Badge variant="outline" className="text-xs">
                  {template.category}
                </Badge>
              </div>
            </div>
          </Card>
        ))}
      </div>
      
      <div className="mt-4 pt-4 border-t border-border">
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <Plus className="w-4 h-4" />
          <span>Custom templates and AI-assisted drafting coming soon</span>
        </div>
      </div>
    </div>
  );
};

export default TemplateSelector;
