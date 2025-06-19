
import { Link } from 'react-router-dom';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Upload, Search, FileText, Brain, TrendingUp } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import Navigation from '../components/Navigation';

const Dashboard = () => {
  const { user } = useAuth();

  const quickActions = [
    {
      title: 'Upload Document',
      description: 'Add new PDFs, presentations, or spreadsheets',
      icon: Upload,
      path: '/upload',
      color: 'bg-blue-500',
    },
    {
      title: 'Ask a Question',
      description: 'Query your documents with AI assistance',
      icon: Search,
      path: '/query',
      color: 'bg-green-500',
    },
  ];

  const stats = [
    { label: 'Documents', value: '0', icon: FileText },
    { label: 'Queries', value: '0', icon: Brain },
    { label: 'Insights', value: '0', icon: TrendingUp },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-blue-100">
      <Navigation />
      
      <main className="container mx-auto px-6 py-8">
        <div className="animate-fade-in">
          {/* Welcome Section */}
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              Welcome back, {user?.fullName}! 👋
            </h1>
            <p className="text-gray-600 text-lg">
              Ready to explore your documents with AI-powered insights?
            </p>
          </div>

          {/* Stats Grid */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            {stats.map((stat) => {
              const Icon = stat.icon;
              return (
                <Card key={stat.label} className="bg-white/80 backdrop-blur-sm border-0 shadow-lg">
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-medium text-gray-600">{stat.label}</p>
                        <p className="text-3xl font-bold text-gray-900">{stat.value}</p>
                      </div>
                      <div className="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center">
                        <Icon className="h-6 w-6 text-blue-600" />
                      </div>
                    </div>
                  </CardContent>
                </Card>
              );
            })}
          </div>

          {/* Quick Actions */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {quickActions.map((action) => {
              const Icon = action.icon;
              return (
                <Card key={action.title} className="bg-white/80 backdrop-blur-sm border-0 shadow-lg hover:shadow-xl transition-shadow duration-300">
                  <CardHeader className="pb-4">
                    <div className="flex items-center space-x-3">
                      <div className={`w-10 h-10 ${action.color} rounded-lg flex items-center justify-center`}>
                        <Icon className="h-5 w-5 text-white" />
                      </div>
                      <div>
                        <CardTitle className="text-xl text-gray-900">{action.title}</CardTitle>
                        <CardDescription className="text-gray-600">
                          {action.description}
                        </CardDescription>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent className="pt-0">
                    <Link to={action.path}>
                      <Button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium">
                        Get Started
                      </Button>
                    </Link>
                  </CardContent>
                </Card>
              );
            })}
          </div>

          {/* Getting Started Tips */}
          <Card className="mt-8 bg-gradient-to-r from-blue-50 to-indigo-50 border-0 shadow-lg">
            <CardHeader>
              <CardTitle className="text-xl text-gray-900 flex items-center space-x-2">
                <Brain className="h-5 w-5 text-blue-600" />
                <span>Getting Started Tips</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3 text-gray-700">
                <div className="flex items-start space-x-3">
                  <div className="w-6 h-6 bg-blue-600 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                    <span className="text-white text-xs font-bold">1</span>
                  </div>
                  <p>Upload your first document using the Upload tab - we support PDFs, PowerPoint, CSV, and more.</p>
                </div>
                <div className="flex items-start space-x-3">
                  <div className="w-6 h-6 bg-blue-600 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                    <span className="text-white text-xs font-bold">2</span>
                  </div>
                  <p>Once uploaded, use the Query tab to ask natural language questions about your documents.</p>
                </div>
                <div className="flex items-start space-x-3">
                  <div className="w-6 h-6 bg-blue-600 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                    <span className="text-white text-xs font-bold">3</span>
                  </div>
                  <p>Get AI-powered insights with context and citations from your document content.</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
