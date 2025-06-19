
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { FileText, Brain, Shield, Upload } from 'lucide-react';

const Index = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-blue-100">
      {/* Header */}
      <header className="container mx-auto px-6 py-6">
        <nav className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <FileText className="h-8 w-8 text-blue-600" />
            <span className="text-2xl font-semibold text-gray-900">DocuMind</span>
          </div>
          <div className="flex items-center space-x-4">
            <Link to="/login">
              <Button variant="ghost" className="text-gray-700 hover:text-blue-600">
                Login
              </Button>
            </Link>
            <Link to="/register">
              <Button className="bg-blue-600 hover:bg-blue-700 text-white">
                Register
              </Button>
            </Link>
          </div>
        </nav>
      </header>

      {/* Hero Section */}
      <main className="container mx-auto px-6 py-20">
        <div className="text-center max-w-4xl mx-auto animate-fade-in">
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6 text-balance">
            Securely upload, manage, and query your documents using{' '}
            <span className="text-blue-600">AI</span>
          </h1>
          <p className="text-xl text-gray-600 mb-12 max-w-2xl mx-auto leading-relaxed">
            Transform your document workflow with intelligent AI-powered search and analysis. 
            Upload any document and get instant answers to your questions.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-16">
            <Link to="/register">
              <Button size="lg" className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 text-lg font-medium">
                Get Started Free
              </Button>
            </Link>
            <Link to="/login">
              <Button size="lg" variant="outline" className="border-blue-200 text-blue-700 hover:bg-blue-50 px-8 py-4 text-lg font-medium">
                Try Demo
              </Button>
            </Link>
          </div>
        </div>

        {/* Features Section */}
        <div className="grid md:grid-cols-3 gap-8 mt-24 animate-slide-in">
          <div className="bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-shadow duration-300">
            <div className="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center mb-6">
              <Upload className="h-6 w-6 text-blue-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-4">Easy Upload</h3>
            <p className="text-gray-600 leading-relaxed">
              Drag and drop your PDFs, PowerPoints, CSVs, and other documents. 
              Our system processes them instantly for AI analysis.
            </p>
          </div>

          <div className="bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-shadow duration-300">
            <div className="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center mb-6">
              <Brain className="h-6 w-6 text-blue-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-4">AI-Powered Queries</h3>
            <p className="text-gray-600 leading-relaxed">
              Ask natural language questions about your documents. 
              Get intelligent answers with relevant context and citations.
            </p>
          </div>

          <div className="bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-shadow duration-300">
            <div className="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center mb-6">
              <Shield className="h-6 w-6 text-blue-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-4">Secure & Private</h3>
            <p className="text-gray-600 leading-relaxed">
              Your documents are encrypted and stored securely. 
              Only you have access to your content and AI interactions.
            </p>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-blue-100 mt-32 py-12 bg-white/50">
        <div className="container mx-auto px-6 text-center">
          <div className="flex items-center justify-center space-x-2 mb-4">
            <FileText className="h-6 w-6 text-blue-600" />
            <span className="text-xl font-semibold text-gray-900">DocuMind</span>
          </div>
          <p className="text-gray-600">
            © 2025 DocuMind. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Index;
