import React, { useState, useEffect, useMemo } from 'react';
import { Card } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { getAdminDashboard, getAllUsers, getAllDocuments, updateUser, getSystemMetrics } from '../api';
import { 
  Users, 
  FileText, 
  MessageSquare, 
  BarChart3, 
  Activity, 
  Database,
  Search,
  Filter,
  Download,
  Settings,
  Trash2,
  Eye,
  Shield,
  AlertTriangle,
  Server,
  HardDrive,
  Cpu,
  Clock,
  Globe,
  Lock,
  Unlock,
  UserPlus,
  UserMinus,
  RefreshCw,
  Calendar,
  TrendingUp,
  TrendingDown,
  Zap,
  Archive,
  Mail,
  Bell,
  ChevronUp,
  ChevronDown,
  CheckCircle,
  XCircle,
  Pause,
  Play,
  MoreVertical
} from 'lucide-react';

const AdminDashboard = ({ user, onClose }) => {
  const [activeTab, setActiveTab] = useState('overview');
  const [users, setUsers] = useState([]);
  const [documents, setDocuments] = useState([]);
  const [metrics, setMetrics] = useState({});
  const [systemLogs, setSystemLogs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [filterType, setFilterType] = useState('all');
  const [selectedDateRange, setSelectedDateRange] = useState('7d');
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState(null);

  // Load dashboard data from API
  const loadDashboardData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // Load dashboard overview data
      const dashboardData = await getAdminDashboard();
      setMetrics({
        totalUsers: dashboardData.user_stats.total_users,
        activeUsers: dashboardData.user_stats.active_users,
        newUsersToday: dashboardData.user_stats.new_users_this_month,
        totalDocuments: dashboardData.document_stats.total_documents,
        documentsToday: dashboardData.document_stats.documents_this_month,
        totalQueries: 0, // Not available in current API
        queriesToday: 0, // Not available in current API
        avgResponseTime: dashboardData.system_stats.average_response_time,
        systemUptime: dashboardData.system_stats.system_uptime,
        apiCallsToday: dashboardData.system_stats.api_calls_today,
        activeSessions: dashboardData.system_stats.active_sessions
      });
      
      // Load users if needed
      if (activeTab === 'users') {
        const usersData = await getAllUsers();
        setUsers(usersData.map(user => ({
          ...user,
          isActive: user.is_active,
          createdAt: new Date(user.created_at),
          lastLogin: user.last_login ? new Date(user.last_login) : new Date(),
          documentsCount: 0, // Would need to be calculated
          queriesCount: 0    // Would need to be calculated
        })));
      }
      
      // Load documents if needed
      if (activeTab === 'documents') {
        const documentsData = await getAllDocuments();
        setDocuments(documentsData.map(doc => ({
          ...doc,
          size: parseFloat(doc.file_size) || 0,
          type: doc.file_type,
          status: 'processed', // Default status
          uploadedAt: new Date(doc.created_at),
          processedAt: new Date(doc.created_at),
          queriesCount: 0, // Would need to be calculated
          uploadedBy: 'unknown' // Would need user lookup
        })));
      }
      
    } catch (err) {
      console.error('Error loading dashboard data:', err);
      setError(err.message);
      // Fallback to some basic data
      setMetrics({
        totalUsers: 0,
        activeUsers: 0,
        newUsersToday: 0,
        totalDocuments: 0,
        documentsToday: 0,
        totalQueries: 0,
        queriesToday: 0,
        avgResponseTime: 0,
        systemUptime: '0%',
        apiCallsToday: 0,
        activeSessions: 0
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDashboardData();
  }, [activeTab]);

  const handleRefresh = async () => {
    setRefreshing(true);
    await loadDashboardData();
    setRefreshing(false);
  };

  const handleUserAction = async (userId, action) => {
    try {
      switch (action) {
        case 'activate':
          await updateUser(userId, { is_active: true });
          break;
        case 'deactivate':
          await updateUser(userId, { is_active: false });
          break;
        case 'delete':
          if (window.confirm('Are you sure you want to delete this user?')) {
            // Delete user API call would go here
            console.log(`Deleting user ${userId}`);
          }
          break;
        case 'view':
        case 'edit':
          console.log(`${action} user ${userId}`);
          break;
        default:
          console.log(`Unknown action: ${action}`);
      }
      // Reload data after action
      await loadDashboardData();
    } catch (err) {
      console.error(`Error performing ${action} on user ${userId}:`, err);
      setError(err.message);
    }
  };

  const handleDocumentAction = async (documentId, action) => {
    try {
      switch (action) {
        case 'delete':
          if (window.confirm('Are you sure you want to delete this document?')) {
            // await deleteDocument(documentId);
            console.log(`Deleting document ${documentId}`);
          }
          break;
        case 'view':
        case 'download':
        case 'reprocess':
          console.log(`${action} document ${documentId}`);
          break;
        default:
          console.log(`Unknown action: ${action}`);
      }
      // Reload data after action
      await loadDashboardData();
    } catch (err) {
      console.error(`Error performing ${action} on document ${documentId}:`, err);
      setError(err.message);
    }
  };

  const filteredUsers = useMemo(() => {
    return users.filter(user => {
      const matchesSearch = user.username.toLowerCase().includes(searchQuery.toLowerCase()) ||
                           user.email.toLowerCase().includes(searchQuery.toLowerCase());
      const matchesFilter = filterType === 'all' || 
                           (filterType === 'active' && user.isActive) ||
                           (filterType === 'inactive' && !user.isActive) ||
                           (filterType === 'admin' && user.role === 'admin');
      return matchesSearch && matchesFilter;
    });
  }, [users, searchQuery, filterType]);

  const MetricsCard = ({ title, value, icon: Icon, suffix = '', color = 'primary' }) => (
    <Card className="p-6 hover:shadow-lg transition-shadow">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-muted-foreground">{title}</p>
          <p className={`text-2xl font-bold text-${color}`}>
            {value}{suffix}
          </p>
        </div>
        <Icon className={`h-8 w-8 text-${color}`} />
      </div>
    </Card>
  );

  const UserRow = ({ user }) => (
    <tr className="border-b border-border hover:bg-muted/50 transition-colors">
      <td className="px-4 py-3">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
            <Users className="w-4 h-4 text-primary" />
          </div>
          <div>
            <p className="font-medium text-foreground">{user.username}</p>
            <p className="text-sm text-muted-foreground">{user.email}</p>
          </div>
        </div>
      </td>
      <td className="px-4 py-3">
        <Badge variant={user.role === 'admin' ? 'default' : 'secondary'}>
          {user.role === 'admin' ? <Shield className="w-3 h-3 mr-1" /> : null}
          {user.role}
        </Badge>
      </td>
      <td className="px-4 py-3">
        <Badge variant={user.isActive ? 'default' : 'destructive'}>
          {user.isActive ? 'Active' : 'Inactive'}
        </Badge>
      </td>
      <td className="px-4 py-3 text-sm text-muted-foreground">
        {user.lastLogin.toLocaleDateString()}
      </td>
      <td className="px-4 py-3 text-sm text-muted-foreground">
        {user.documentsCount}
      </td>
      <td className="px-4 py-3 text-sm text-muted-foreground">
        {user.queriesCount}
      </td>
      <td className="px-4 py-3">
        <div className="flex items-center gap-2">
          <Button 
            variant="ghost" 
            size="sm"
            onClick={() => handleUserAction(user.id, 'view')}
            title="View Details"
          >
            <Eye className="w-4 h-4" />
          </Button>
          <Button 
            variant="ghost" 
            size="sm"
            onClick={() => handleUserAction(user.id, 'edit')}
            title="Edit User"
          >
            <Settings className="w-4 h-4" />
          </Button>
          <Button 
            variant="ghost" 
            size="sm"
            onClick={() => handleUserAction(user.id, user.isActive ? 'deactivate' : 'activate')}
            title={user.isActive ? 'Deactivate' : 'Activate'}
          >
            {user.isActive ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
          </Button>
          <Button 
            variant="ghost" 
            size="sm" 
            className="text-destructive"
            onClick={() => handleUserAction(user.id, 'delete')}
            title="Delete User"
          >
            <Trash2 className="w-4 h-4" />
          </Button>
        </div>
      </td>
    </tr>
  );

  const DocumentRow = ({ document }) => (
    <tr className="border-b border-border hover:bg-muted/50 transition-colors">
      <td className="px-4 py-3">
        <div className="flex items-center gap-2">
          <FileText className="w-4 h-4 text-primary" />
          <div>
            <p className="font-medium text-foreground truncate max-w-xs">{document.filename}</p>
            <p className="text-sm text-muted-foreground">{document.type}</p>
          </div>
        </div>
      </td>
      <td className="px-4 py-3">
        <span className="text-sm text-muted-foreground">{document.uploadedBy}</span>
      </td>
      <td className="px-4 py-3">
        <Badge 
          variant={
            document.status === 'processed' ? 'default' :
            document.status === 'processing' ? 'secondary' : 'destructive'
          }
        >
          {document.status === 'processed' && <CheckCircle className="w-3 h-3 mr-1" />}
          {document.status === 'processing' && <RefreshCw className="w-3 h-3 mr-1 animate-spin" />}
          {document.status === 'failed' && <XCircle className="w-3 h-3 mr-1" />}
          {document.status}
        </Badge>
      </td>
      <td className="px-4 py-3 text-sm text-muted-foreground">
        {document.size.toFixed(1)} MB
      </td>
      <td className="px-4 py-3 text-sm text-muted-foreground">
        {document.uploadedAt.toLocaleDateString()}
      </td>
      <td className="px-4 py-3 text-sm text-muted-foreground">
        {document.queriesCount}
      </td>
      <td className="px-4 py-3">
        <div className="flex items-center gap-2">
          <Button 
            variant="ghost" 
            size="sm"
            onClick={() => handleDocumentAction(document.id, 'view')}
            title="View Document"
          >
            <Eye className="w-4 h-4" />
          </Button>
          <Button 
            variant="ghost" 
            size="sm"
            onClick={() => handleDocumentAction(document.id, 'download')}
            title="Download"
          >
            <Download className="w-4 h-4" />
          </Button>
          {document.status === 'failed' && (
            <Button 
              variant="ghost" 
              size="sm"
              onClick={() => handleDocumentAction(document.id, 'reprocess')}
              title="Retry Processing"
            >
              <RefreshCw className="w-4 h-4" />
            </Button>
          )}
          <Button 
            variant="ghost" 
            size="sm" 
            className="text-destructive"
            onClick={() => handleDocumentAction(document.id, 'delete')}
            title="Delete Document"
          >
            <Trash2 className="w-4 h-4" />
          </Button>
        </div>
      </td>
    </tr>
  );

  const LogRow = ({ log }) => (
    <tr className="border-b border-border hover:bg-muted/50 transition-colors">
      <td className="px-4 py-3">
        <span className="text-sm text-muted-foreground">
          {log.timestamp.toLocaleString()}
        </span>
      </td>
      <td className="px-4 py-3">
        <Badge 
          variant={
            log.level === 'error' ? 'destructive' :
            log.level === 'warning' ? 'secondary' : 'default'
          }
        >
          {log.level === 'error' && <XCircle className="w-3 h-3 mr-1" />}
          {log.level === 'warning' && <AlertTriangle className="w-3 h-3 mr-1" />}
          {log.level === 'info' && <CheckCircle className="w-3 h-3 mr-1" />}
          {log.level}
        </Badge>
      </td>
      <td className="px-4 py-3">
        <span className="text-sm font-medium text-foreground">{log.action}</span>
      </td>
      <td className="px-4 py-3">
        <span className="text-sm text-muted-foreground">{log.user}</span>
      </td>
      <td className="px-4 py-3">
        <span className="text-sm text-muted-foreground">{log.ip}</span>
      </td>
      <td className="px-4 py-3">
        <p className="text-sm text-muted-foreground truncate max-w-xs" title={log.details}>
          {log.details}
        </p>
      </td>
    </tr>
  );

  const renderOverview = () => (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricsCard 
          title="Total Users" 
          value={metrics.totalUsers} 
          icon={Users}
        />
        <MetricsCard 
          title="Active Users" 
          value={metrics.activeUsers} 
          icon={Activity}
          color="green-500"
        />
        <MetricsCard 
          title="Documents Processed" 
          value={metrics.totalDocuments} 
          icon={FileText}
          color="blue-500"
        />
        <MetricsCard 
          title="AI Queries" 
          value={metrics.totalQueries} 
          icon={MessageSquare}
          color="purple-500"
        />
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricsCard 
          title="New Users Today" 
          value={metrics.newUsersToday} 
          icon={UserPlus}
          color="green-600"
        />
        <MetricsCard 
          title="Documents Today" 
          value={metrics.documentsToday} 
          icon={Archive}
          color="blue-600"
        />
        <MetricsCard 
          title="Queries Today" 
          value={metrics.queriesToday} 
          icon={Zap}
          color="yellow-500"
        />
        <MetricsCard 
          title="Processing Queue" 
          value={metrics.documentProcessingQueue} 
          icon={Clock}
          color="orange-500"
        />
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Activity className="w-5 h-5" />
            System Performance
          </h3>
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-sm text-muted-foreground">Avg Response Time</span>
              <span className="font-medium">{metrics.avgResponseTime}s</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-muted-foreground">System Uptime</span>
              <span className="font-medium text-green-500">{metrics.systemUptime}%</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-muted-foreground">Storage Used</span>
              <span className="font-medium">{metrics.storageUsed}%</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-muted-foreground">Error Rate</span>
              <span className="font-medium text-red-500">{(metrics.errorRate * 100).toFixed(2)}%</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-muted-foreground">Peak Concurrent Users</span>
              <span className="font-medium">{metrics.peakConcurrentUsers}</span>
            </div>
          </div>
        </Card>
        
        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <TrendingUp className="w-5 h-5" />
            API & Usage Stats
          </h3>
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-sm text-muted-foreground">API Calls Today</span>
              <span className="font-medium">{metrics.apiCallsToday}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-muted-foreground">API Calls This Month</span>
              <span className="font-medium">{metrics.apiCallsThisMonth.toLocaleString()}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-muted-foreground">Avg Session Duration</span>
              <span className="font-medium">{metrics.avgSessionDuration} min</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-muted-foreground">Storage Total</span>
              <span className="font-medium">{metrics.storageTotal} GB</span>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );

  const renderUserManagement = () => (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
        <div className="flex flex-1 gap-4">
          <div className="relative flex-1 max-w-sm">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <input
              type="text"
              placeholder="Search users..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-9 pr-3 py-2 w-full rounded-md border border-border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>
          <select
            value={filterType}
            onChange={(e) => setFilterType(e.target.value)}
            className="px-3 py-2 rounded-md border border-border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-primary"
          >
            <option value="all">All Users</option>
            <option value="active">Active</option>
            <option value="inactive">Inactive</option>
            <option value="admin">Admins</option>
          </select>
        </div>
        <Button>
          <Download className="w-4 h-4 mr-2" />
          Export
        </Button>
      </div>

      <Card>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="border-b border-border">
              <tr>
                <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">User</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">Role</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">Status</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">Last Login</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">Documents</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">Queries</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredUsers.map((user) => (
                <UserRow key={user.id} user={user} />
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );

  const renderSystemHealth = () => (
    <div className="space-y-6">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Database className="w-5 h-5" />
            Database Status
          </h3>
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-sm">Connection Status</span>
              <Badge variant="default" className="bg-green-500">Connected</Badge>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm">Query Performance</span>
              <span className="text-sm font-medium">98.5ms avg</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm">Active Connections</span>
              <span className="text-sm font-medium">23/100</span>
            </div>
          </div>
        </Card>

        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <AlertTriangle className="w-5 h-5" />
            System Alerts
          </h3>
          <div className="space-y-3">
            <div className="p-3 rounded-md bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800">
              <p className="text-sm font-medium text-yellow-800 dark:text-yellow-200">
                High Storage Usage
              </p>
              <p className="text-xs text-yellow-600 dark:text-yellow-300">
                Storage is at 85% capacity
              </p>
            </div>
            <div className="p-3 rounded-md bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800">
              <p className="text-sm font-medium text-green-800 dark:text-green-200">
                All Systems Operational
              </p>
              <p className="text-xs text-green-600 dark:text-green-300">
                No critical issues detected
              </p>
            </div>
          </div>
        </Card>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Cpu className="w-5 h-5" />
            Server Utilization
          </h3>
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-sm">CPU Load</span>
              <span className="text-sm font-medium">{metrics.systemLoad?.cpu}%</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm">Memory Usage</span>
              <span className="text-sm font-medium">{metrics.systemLoad?.memory}%</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm">Disk Space Used</span>
              <span className="text-sm font-medium">{metrics.systemLoad?.disk}%</span>
            </div>
          </div>
        </Card>

        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Server className="w-5 h-5" />
            Network Activity
          </h3>
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-sm">Inbound</span>
              <span className="text-sm font-medium">{metrics.networkStats?.inbound} MB/s</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm">Outbound</span>
              <span className="text-sm font-medium">{metrics.networkStats?.outbound} MB/s</span>
            </div>
          </div>
        </Card>      
      </div>
    </div>
  );

  const renderDocumentManagement = () => (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
        <div className="flex-1 gap-4 flex">
          <div className="relative flex-1 max-w-sm">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <input
              type="text"
              placeholder="Search documents..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-9 pr-3 py-2 w-full rounded-md border border-border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>
          <select
            value={selectedDateRange}
            onChange={(e) => setSelectedDateRange(e.target.value)}
            className="px-3 py-2 rounded-md border border-border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-primary"
          >
            <option value="7d">Last 7 Days</option>
            <option value="30d">Last 30 Days</option>
            <option value="12m">Last 12 Months</option>
          </select>
        </div>
        <Button onClick={handleRefresh} disabled={refreshing}>
          {refreshing ? (
            <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
          ) : (
            <RefreshCw className="w-4 h-4 mr-2" />
          )}
          Refresh
        </Button>
      </div>

      <Card>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="border-b border-border">
              <tr>
                <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">Document</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">Uploader</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">Status</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">Size</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">Uploaded</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">Queries</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">Actions</th>
              </tr>
            </thead>
            <tbody>
              {documents.map((document) => (
                <DocumentRow key={document.id} document={document} />
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );

  const renderSystemLogs = () => (
    <div className="space-y-6">
      <Card>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="border-b border-border">
              <tr>
                <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">Timestamp</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">Level</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">Action</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">User</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">IP</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">Details</th>
              </tr>
            </thead>
            <tbody>
              {systemLogs.map((log) => (
                <LogRow key={log.id} log={log} />
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      {error && (
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 p-4 mx-6 mt-4 rounded-md">
          <p className="text-sm font-medium text-red-800 dark:text-red-200">Error: {error}</p>
        </div>
      )}
      <div className="border-b border-border bg-background/95 backdrop-blur-lg">
        <div className="flex items-center justify-between px-6 py-4">
          <div className="flex items-center gap-4">
            <Button variant="ghost" onClick={onClose}>
              ← Back to Chat
            </Button>
            <div>
              <h1 className="text-2xl font-bold">Admin Dashboard</h1>
              <p className="text-sm text-muted-foreground">
                Welcome back, {user.username}
              </p>
            </div>
          </div>
          <Badge variant="default" className="bg-primary">
            <Shield className="w-3 h-3 mr-1" />
            Admin
          </Badge>
        </div>
        
        <div className="px-6">
          <nav className="flex space-x-6 overflow-x-auto">
            {[
              { id: 'overview', label: 'Overview', icon: BarChart3 },
              { id: 'users', label: 'User Management', icon: Users },
              { id: 'documents', label: 'Document Management', icon: FileText },
              { id: 'logs', label: 'System Logs', icon: Activity },
              { id: 'system', label: 'System Health', icon: Server }
            ].map(({ id, label, icon: Icon }) => (
              <button
                key={id}
                onClick={() => setActiveTab(id)}
                className={`flex items-center gap-2 px-3 py-2 border-b-2 font-medium text-sm transition-colors whitespace-nowrap ${
                  activeTab === id
                    ? 'border-primary text-primary'
                    : 'border-transparent text-muted-foreground hover:text-foreground'
                }`}
              >
                <Icon className="w-4 h-4" />
                {label}
              </button>
            ))}
          </nav>
        </div>
      </div>

      <div className="p-6">
        {activeTab === 'overview' && renderOverview()}
        {activeTab === 'users' && renderUserManagement()}
        {activeTab === 'documents' && renderDocumentManagement()}
        {activeTab === 'logs' && renderSystemLogs()}
        {activeTab === 'system' && renderSystemHealth()}
      </div>
    </div>
  );
};

export default AdminDashboard;
