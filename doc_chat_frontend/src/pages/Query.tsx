import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Search, Brain, MessageCircle, FileText, Sparkles } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { useToast } from '@/hooks/use-toast';
import Navigation from '../components/Navigation';

interface QueryResult {
  id: string;
  question: string;
  answer: string;
  context: string[];
  timestamp: Date;
}

const Query = () => {
  const [query, setQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [queryHistory, setQueryHistory] = useState<QueryResult[]>([]);
  const [error, setError] = useState<string | null>(null);
  const { token } = useAuth();
  const { toast } = useToast();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setIsLoading(true);
    const currentQuery = query;
    setQuery('');

    try {
      console.log('Sending query:', currentQuery); // Debug log
      console.log('Token available:', !!token); // Debug log
      
      const response = await fetch('/api/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ question: currentQuery }),
      });

      console.log('Response status:', response.status); // Debug log

      if (response.ok) {
        const data = await response.json();
        console.log('Response data:', data); // Debug log
        
        const newResult: QueryResult = {
          id: `query-${Date.now()}`,
          question: currentQuery,
          answer: data.answer || 'No answer received',
          context: Array.isArray(data.context) ? data.context : [],
          timestamp: new Date(),
        };
        
        console.log('New result:', newResult); // Debug log
        setQueryHistory(prev => [newResult, ...prev]);
        toast({
          title: "Query processed",
          description: "Your question has been analyzed successfully.",
        });
      } else {
        const errorData = await response.json();
        console.error('Response error:', errorData); // Debug log
        toast({
          title: "Query failed",
          description: errorData.detail || "Failed to process query",
          variant: "destructive",
        });
      }
    } catch (error) {
      console.error('Query error:', error);
      toast({
        title: "Query failed",
        description: "Network error. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const suggestedQueries = [
    "What are the key findings in my research documents?",
    "Summarize the main points from the presentation slides",
    "What trends can you identify from the data?",
    "Extract action items from the meeting notes",
  ];

  // Error boundary for rendering
  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-blue-100 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-xl font-semibold text-red-600 mb-2">Something went wrong</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <button 
            onClick={() => setError(null)}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  try {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-blue-100">
        <Navigation />
        
        <main className="container mx-auto px-6 py-8">
          <div className="animate-fade-in">
            {/* Header */}
            <div className="mb-8">
              <h1 className="text-3xl font-bold text-gray-900 mb-2">Ask Questions</h1>
              <p className="text-gray-600 text-lg">
                Query your uploaded documents using natural language and get AI-powered insights.
              </p>
            </div>

            {/* Query Input */}
            <Card className="mb-8 bg-white/80 backdrop-blur-sm border-0 shadow-lg">
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Brain className="h-5 w-5 text-blue-600" />
                  <span>Ask Anything</span>
                </CardTitle>
                <CardDescription>
                  Ask questions about your documents in natural language
                </CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleSubmit} className="space-y-4">
                  <div className="flex space-x-2">
                    <Input
                      placeholder="Ask anything about your documents..."
                      value={query}
                      onChange={(e) => setQuery(e.target.value)}
                      className="flex-1 border-gray-200 focus:border-blue-500 focus:ring-blue-500"
                      disabled={isLoading}
                    />
                    <Button
                      type="submit"
                      disabled={isLoading || !query.trim()}
                      className="bg-blue-600 hover:bg-blue-700 text-white px-6"
                    >
                      {isLoading ? (
                        <div className="flex items-center space-x-2">
                          <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                          <span>Thinking...</span>
                        </div>
                      ) : (
                        <div className="flex items-center space-x-2">
                          <Search className="h-4 w-4" />
                          <span>Ask</span>
                        </div>
                      )}
                    </Button>
                  </div>
                </form>

                {/* Suggested Queries */}
                {queryHistory.length === 0 && (
                  <div className="mt-6">
                    <p className="text-sm font-medium text-gray-700 mb-3">Suggested questions:</p>
                    <div className="flex flex-wrap gap-2">
                      {suggestedQueries.map((suggestion, index) => (
                        <Badge
                          key={index}
                          variant="secondary"
                          className="cursor-pointer hover:bg-blue-100 hover:text-blue-700 transition-colors"
                          onClick={() => setQuery(suggestion)}
                        >
                          {suggestion}
                        </Badge>
                      ))}
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Query Results */}
            {queryHistory.length > 0 && (
              <div className="space-y-6">
                <h2 className="text-xl font-semibold text-gray-900 flex items-center space-x-2">
                  <MessageCircle className="h-5 w-5 text-blue-600" />
                  <span>Query History</span>
                </h2>
                
                {queryHistory.map((result) => (
                  <Card key={result.id} className="bg-white/80 backdrop-blur-sm border-0 shadow-lg">
                    <CardHeader className="pb-3">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center space-x-2 mb-2">
                            <Sparkles className="h-4 w-4 text-blue-600" />
                            <span className="text-sm font-medium text-blue-600">Question</span>
                          </div>
                          <p className="text-gray-900 font-medium">{result.question}</p>
                        </div>
                        <Badge variant="outline" className="text-xs">
                          {result.timestamp.toLocaleTimeString()}
                        </Badge>
                      </div>
                    </CardHeader>
                    <CardContent className="space-y-4">
                      <div>
                        <div className="flex items-center space-x-2 mb-2">
                          <Brain className="h-4 w-4 text-green-600" />
                          <span className="text-sm font-medium text-green-600">AI Response</span>
                        </div>
                        <p className="text-gray-700 leading-relaxed bg-gray-50 p-4 rounded-lg">
                          {typeof result.answer === 'object'
                            ? JSON.stringify(result.answer, null, 2)
                            : result.answer}
                        </p>
                      </div>
                      
                      {result.context.length > 0 && (
                        <div>
                          <div className="flex items-center space-x-2 mb-2">
                            <FileText className="h-4 w-4 text-orange-600" />
                            <span className="text-sm font-medium text-orange-600">Sources</span>
                          </div>
                          <div className="space-y-1">
                            {result.context.map((ctx, index) => (
                              <div key={index} className="text-sm text-gray-600 bg-orange-50 px-3 py-1 rounded">
                                {ctx}
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}

            {/* Empty State */}
            {queryHistory.length === 0 && !isLoading && (
              <Card className="bg-gradient-to-r from-blue-50 to-indigo-50 border-0 shadow-lg">
                <CardContent className="text-center py-12">
                  <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Brain className="h-8 w-8 text-blue-600" />
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">Ready to explore your documents?</h3>
                  <p className="text-gray-600 mb-6 max-w-md mx-auto">
                    Ask questions about your uploaded documents and get AI-powered insights with relevant context and citations.
                  </p>
                  <div className="flex justify-center">
                    <Badge variant="secondary" className="text-sm">
                      Tip: Try asking specific questions about data, trends, or key findings
                    </Badge>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        </main>
      </div>
    );
  } catch (err) {
    console.error('Rendering error:', err);
    setError(err instanceof Error ? err.message : 'Unknown error occurred');
    return null;
  }
};

export default Query;
