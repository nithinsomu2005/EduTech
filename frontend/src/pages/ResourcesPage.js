import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../utils/api';
import { ArrowLeft, BookOpen, FileText, Download, ExternalLink } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';

const ResourcesPage = () => {
  const navigate = useNavigate();
  const [resources, setResources] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchResources();
  }, []);

  const fetchResources = async () => {
    try {
      const response = await api.get('/resources');
      setResources(response.data);
    } catch (error) {
      console.error('Failed to fetch resources:', error);
    } finally {
      setLoading(false);
    }
  };

  const getResourceIcon = (type) => {
    switch (type) {
      case 'textbook':
        return <BookOpen className="w-6 h-6" />;
      case 'question_paper':
        return <FileText className="w-6 h-6" />;
      case 'formula_sheet':
        return <FileText className="w-6 h-6" />;
      default:
        return <BookOpen className="w-6 h-6" />;
    }
  };

  const textbooks = resources.filter(r => r.type === 'textbook');
  const questionPapers = resources.filter(r => r.type === 'question_paper');
  const formulaSheets = resources.filter(r => r.type === 'formula_sheet');

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[hsl(var(--primary))] mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading resources...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <Button variant="ghost" onClick={() => navigate('/student/dashboard')} data-testid="back-btn">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Dashboard
          </Button>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8 fade-in">
          <div className="flex items-center space-x-3 mb-4">
            <div className="w-12 h-12 bg-[hsl(var(--primary))] rounded-xl flex items-center justify-center">
              <BookOpen className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-4xl font-bold">Learning Resources</h1>
              <p className="text-gray-600 text-lg">NCERT textbooks, question papers, and study materials</p>
            </div>
          </div>
        </div>

        <Tabs defaultValue="textbooks" className="w-full">
          <TabsList className="grid w-full grid-cols-3 mb-8">
            <TabsTrigger value="textbooks">NCERT Textbooks ({textbooks.length})</TabsTrigger>
            <TabsTrigger value="papers">Question Papers ({questionPapers.length})</TabsTrigger>
            <TabsTrigger value="formulas">Formula Sheets ({formulaSheets.length})</TabsTrigger>
          </TabsList>

          <TabsContent value="textbooks" className="space-y-6">
            <div className="grid md:grid-cols-3 gap-6">
              {textbooks.map((resource) => (
                <div
                  key={resource.resource_id}
                  className="bg-white rounded-xl overflow-hidden shadow-sm card-hover border border-gray-200"
                  data-testid={`resource-${resource.resource_id}`}
                >
                  <div className="h-48 bg-cover bg-center" style={{ backgroundImage: `url(${resource.thumbnail})` }}>
                    <div className="h-full bg-gradient-to-t from-black/70 to-transparent flex items-end p-4">
                      <span className="text-white text-xs font-semibold bg-[hsl(var(--primary))] px-3 py-1 rounded">
                        {resource.grade_level}
                      </span>
                    </div>
                  </div>
                  <div className="p-5">
                    <div className="flex items-start space-x-3 mb-3">
                      <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center text-[hsl(var(--primary))]">
                        {getResourceIcon(resource.type)}
                      </div>
                      <div className="flex-1">
                        <h3 className="font-bold text-lg mb-1">{resource.title}</h3>
                        <p className="text-sm text-gray-600">{resource.subject}</p>
                      </div>
                    </div>
                    <p className="text-sm text-gray-600 mb-4">{resource.description}</p>
                    <a
                      href={resource.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="block"
                    >
                      <Button className="w-full btn-hover" data-testid={`open-resource-${resource.resource_id}`}>
                        <ExternalLink className="w-4 h-4 mr-2" />
                        Open Textbook
                      </Button>
                    </a>
                  </div>
                </div>
              ))}
            </div>
          </TabsContent>

          <TabsContent value="papers" className="space-y-6">
            <div className="grid md:grid-cols-3 gap-6">
              {questionPapers.map((resource) => (
                <div
                  key={resource.resource_id}
                  className="bg-white rounded-xl overflow-hidden shadow-sm card-hover border border-gray-200"
                >
                  <div className="h-48 bg-cover bg-center" style={{ backgroundImage: `url(${resource.thumbnail})` }}>
                    <div className="h-full bg-gradient-to-t from-black/70 to-transparent flex items-end p-4">
                      <span className="text-white text-xs font-semibold bg-purple-500 px-3 py-1 rounded">
                        {resource.year}
                      </span>
                    </div>
                  </div>
                  <div className="p-5">
                    <div className="flex items-start space-x-3 mb-3">
                      <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center text-purple-600">
                        {getResourceIcon(resource.type)}
                      </div>
                      <div className="flex-1">
                        <h3 className="font-bold text-lg mb-1">{resource.title}</h3>
                        <p className="text-sm text-gray-600">{resource.subject}</p>
                      </div>
                    </div>
                    <p className="text-sm text-gray-600 mb-4">{resource.description}</p>
                    <a
                      href={resource.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="block"
                    >
                      <Button className="w-full btn-hover" variant="secondary">
                        <Download className="w-4 h-4 mr-2" />
                        View Paper
                      </Button>
                    </a>
                  </div>
                </div>
              ))}
            </div>
          </TabsContent>

          <TabsContent value="formulas" className="space-y-6">
            <div className="grid md:grid-cols-3 gap-6">
              {formulaSheets.map((resource) => (
                <div
                  key={resource.resource_id}
                  className="bg-white rounded-xl overflow-hidden shadow-sm card-hover border border-gray-200"
                >
                  <div className="h-48 bg-cover bg-center" style={{ backgroundImage: `url(${resource.thumbnail})` }}>
                    <div className="h-full bg-gradient-to-t from-black/70 to-transparent flex items-end p-4">
                      <span className="text-white text-xs font-semibold bg-green-500 px-3 py-1 rounded">
                        {resource.grade_level}
                      </span>
                    </div>
                  </div>
                  <div className="p-5">
                    <div className="flex items-start space-x-3 mb-3">
                      <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center text-green-600">
                        {getResourceIcon(resource.type)}
                      </div>
                      <div className="flex-1">
                        <h3 className="font-bold text-lg mb-1">{resource.title}</h3>
                        <p className="text-sm text-gray-600">{resource.subject}</p>
                      </div>
                    </div>
                    <p className="text-sm text-gray-600 mb-4">{resource.description}</p>
                    <a
                      href={resource.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="block"
                    >
                      <Button className="w-full btn-hover" variant="secondary">
                        <ExternalLink className="w-4 h-4 mr-2" />
                        Open Resource
                      </Button>
                    </a>
                  </div>
                </div>
              ))}
            </div>
          </TabsContent>
        </Tabs>

        {resources.length === 0 && (
          <div className="text-center py-12">
            <BookOpen className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600">No resources available</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ResourcesPage;
