import React, { useState } from "react";
import { Card } from "./ui/card";
import { Button } from "./ui/button";
import { Badge } from "./ui/badge";
import { 
  X, 
  User, 
  Mail, 
  Lock, 
  Bell, 
  Shield, 
  Settings,
  Edit3,
  Save,
  Camera
} from "lucide-react";

const ProfileSettings = ({ isOpen, onClose, user, onSave }) => {
  const [editMode, setEditMode] = useState(false);
  const [formData, setFormData] = useState({
    username: user?.username || '',
    email: user?.email || '',
    notifications: true,
    darkMode: false
  });

  const handleSave = () => {
    if (onSave) {
      onSave(formData);
    }
    setEditMode(false);
  };

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  if (!isOpen) return null;

  return (
    <>
      {/* Overlay */}
      <div 
        className="fixed inset-0 bg-black/20 backdrop-blur-sm z-40"
        onClick={onClose}
      />
      
      {/* Modal */}
      <div className="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-full max-w-md z-50">
        <Card className="bg-background/95 backdrop-blur-lg border border-border shadow-2xl rounded-3xl overflow-hidden">
          {/* Header */}
          <div className="p-6 border-b border-border/30 bg-gradient-to-r from-primary/5 to-secondary/5">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-primary/10 rounded-xl">
                  <User className="w-5 h-5 text-primary" />
                </div>
                <div>
                  <h2 className="text-lg font-semibold text-foreground">Profile Settings</h2>
                  <p className="text-xs text-muted-foreground">Manage your account</p>
                </div>
              </div>
              <Button
                variant="ghost"
                size="sm"
                onClick={onClose}
                className="p-2 h-8 w-8"
              >
                <X className="w-4 h-4" />
              </Button>
            </div>
          </div>

          {/* Content */}
          <div className="p-6 space-y-6">
            {/* Avatar Section */}
            <div className="flex items-center gap-4">
              <div className="relative">
                <div className="w-16 h-16 rounded-full bg-gradient-to-br from-primary to-primary/60 flex items-center justify-center shadow-lg">
                  <span className="text-xl font-bold text-primary-foreground">
                    {user?.username?.charAt(0)?.toUpperCase() || 'U'}
                  </span>
                </div>
                <button className="absolute -bottom-1 -right-1 p-1.5 bg-primary/10 rounded-full border-2 border-background hover:bg-primary/20 transition-colors">
                  <Camera className="w-3 h-3 text-primary" />
                </button>
              </div>
              <div className="flex-1">
                <h3 className="font-medium text-foreground">{user?.username || 'User'}</h3>
                <p className="text-sm text-muted-foreground">{user?.email || ''}</p>
                <div className="flex items-center gap-2 mt-1">
                  <Badge variant="secondary" className="text-xs">
                    {user?.role || 'User'}
                  </Badge>
                  <Badge variant="outline" className="text-xs">
                    Active
                  </Badge>
                </div>
              </div>
            </div>

            {/* Form Fields */}
            <div className="space-y-4">
              {/* Username */}
              <div>
                <label className="text-sm font-medium text-foreground mb-2 block">
                  Username
                </label>
                <div className="relative">
                  <User className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                  <input
                    type="text"
                    value={formData.username}
                    onChange={(e) => handleInputChange('username', e.target.value)}
                    disabled={!editMode}
                    className="pl-9 pr-3 py-2 w-full rounded-xl border border-border bg-background/50 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary disabled:opacity-60 transition-all"
                  />
                </div>
              </div>

              {/* Email */}
              <div>
                <label className="text-sm font-medium text-foreground mb-2 block">
                  Email
                </label>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                  <input
                    type="email"
                    value={formData.email}
                    onChange={(e) => handleInputChange('email', e.target.value)}
                    disabled={!editMode}
                    className="pl-9 pr-3 py-2 w-full rounded-xl border border-border bg-background/50 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary disabled:opacity-60 transition-all"
                  />
                </div>
              </div>

              {/* Settings Toggles */}
              <div className="space-y-3">
                <div className="flex items-center justify-between p-3 bg-background/50 rounded-xl border border-border/30">
                  <div className="flex items-center gap-3">
                    <Bell className="w-4 h-4 text-muted-foreground" />
                    <div>
                      <p className="text-sm font-medium text-foreground">Notifications</p>
                      <p className="text-xs text-muted-foreground">Receive email updates</p>
                    </div>
                  </div>
                  <button
                    onClick={() => handleInputChange('notifications', !formData.notifications)}
                    disabled={!editMode}
                    className={`w-10 h-6 rounded-full transition-colors relative ${
                      formData.notifications ? 'bg-primary' : 'bg-muted'
                    } ${!editMode ? 'opacity-60' : ''}`}
                  >
                    <div
                      className={`w-4 h-4 bg-white rounded-full absolute top-1 transition-transform ${
                        formData.notifications ? 'translate-x-5' : 'translate-x-1'
                      }`}
                    />
                  </button>
                </div>

                <div className="flex items-center justify-between p-3 bg-background/50 rounded-xl border border-border/30">
                  <div className="flex items-center gap-3">
                    <Shield className="w-4 h-4 text-muted-foreground" />
                    <div>
                      <p className="text-sm font-medium text-foreground">Privacy Mode</p>
                      <p className="text-xs text-muted-foreground">Enhanced security</p>
                    </div>
                  </div>
                  <Badge variant="secondary" className="text-xs">
                    Enabled
                  </Badge>
                </div>
              </div>
            </div>
          </div>

          {/* Footer */}
          <div className="p-6 border-t border-border/30 bg-background/50">
            <div className="flex items-center gap-2">
              {!editMode ? (
                <Button
                  onClick={() => setEditMode(true)}
                  className="flex-1 h-9 rounded-xl gap-2"
                >
                  <Edit3 className="w-4 h-4" />
                  Edit Profile
                </Button>
              ) : (
                <>
                  <Button
                    variant="outline"
                    onClick={() => setEditMode(false)}
                    className="flex-1 h-9 rounded-xl"
                  >
                    Cancel
                  </Button>
                  <Button
                    onClick={handleSave}
                    className="flex-1 h-9 rounded-xl gap-2"
                  >
                    <Save className="w-4 h-4" />
                    Save Changes
                  </Button>
                </>
              )}
            </div>
          </div>
        </Card>
      </div>
    </>
  );
};

export default ProfileSettings;
