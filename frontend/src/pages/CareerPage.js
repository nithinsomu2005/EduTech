import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../utils/api';
import { ArrowLeft, Target, TrendingUp, Briefcase, DollarSign, ExternalLink } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';

const CareerPage = () => {
  const navigate = useNavigate();
  const [roadmaps, setRoadmaps] = useState([]);
  const [selectedRoadmap, setSelectedRoadmap] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchRoadmaps();
  }, []);

  const fetchRoadmaps = async () => {
    try {
      const response = await api.get('/career/roadmaps');
      setRoadmaps(response.data);
      if (response.data.length > 0) {
        setSelectedRoadmap(response.data[0]);
      }
    } catch (error) {
      console.error('Failed to fetch roadmaps:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[hsl(var(--primary))] mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading career paths...</p>
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
              <Target className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-4xl font-bold">Career Roadmaps</h1>
              <p className="text-gray-600 text-lg">Explore career paths and skill requirements</p>
            </div>
          </div>
        </div>

        <div className="grid lg:grid-cols-3 gap-6">
          <div className="lg:col-span-1">
            <div className="bg-white rounded-2xl shadow-sm p-6 sticky top-4" data-testid="roadmaps-list">
              <h2 className="text-xl font-bold mb-4">Available Paths</h2>
              <div className="space-y-3">
                {roadmaps.map((roadmap) => (
                  <div
                    key={roadmap.roadmap_id}
                    onClick={() => setSelectedRoadmap(roadmap)}
                    className={`p-4 rounded-xl border-2 cursor-pointer transition-all ${
                      selectedRoadmap?.roadmap_id === roadmap.roadmap_id
                        ? 'border-[hsl(var(--primary))] bg-blue-50'
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                    data-testid={`roadmap-item-${roadmap.roadmap_id}`}
                  >
                    <p className="font-semibold text-lg">{roadmap.title}</p>
                    <p className="text-sm text-gray-600 mt-1">{roadmap.skills.length} skills required</p>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="lg:col-span-2">
            {selectedRoadmap && (
              <div className="space-y-6 fade-in">
                <div className="bg-white rounded-2xl shadow-sm p-8" data-testid="roadmap-header">
                  <h2 className="text-3xl font-bold mb-4">{selectedRoadmap.title}</h2>
                  
                  <div className="grid md:grid-cols-2 gap-4 mb-6">
                    <div className="flex items-center space-x-3 p-4 bg-green-50 rounded-xl">
                      <DollarSign className="w-8 h-8 text-green-600" />
                      <div>
                        <p className="text-sm text-gray-600">Average Salary</p>
                        <p className="font-bold text-lg">{selectedRoadmap.avg_salary}</p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-3 p-4 bg-purple-50 rounded-xl">
                      <Briefcase className="w-8 h-8 text-purple-600" />
                      <div>
                        <p className="text-sm text-gray-600">Job Roles</p>
                        <p className="font-bold text-lg">{selectedRoadmap.job_roles.length}+ roles</p>
                      </div>
                    </div>
                  </div>

                  <Tabs defaultValue="skills" className="w-full">
                    <TabsList className="grid w-full grid-cols-3 mb-6">
                      <TabsTrigger value="skills">Skills</TabsTrigger>
                      <TabsTrigger value="milestones">Roadmap</TabsTrigger>
                      <TabsTrigger value="roles">Job Roles</TabsTrigger>
                    </TabsList>

                    <TabsContent value="skills" data-testid="skills-tab">
                      <div className="grid md:grid-cols-3 gap-3">
                        {selectedRoadmap.skills.map((skill, index) => (
                          <div
                            key={index}
                            className="px-4 py-3 bg-gradient-to-br from-blue-50 to-cyan-50 border border-blue-100 rounded-lg font-semibold text-center"
                            data-testid={`skill-${index}`}
                          >
                            {skill}
                          </div>
                        ))}
                      </div>
                    </TabsContent>

                    <TabsContent value="milestones" data-testid="milestones-tab">
                      <div className="space-y-4">
                        {selectedRoadmap.milestones.map((milestone, index) => (
                          <div key={index} className="relative pl-8 pb-8 border-l-2 border-[hsl(var(--primary))] last:border-l-0 last:pb-0" data-testid={`milestone-${index}`}>
                            <div className="absolute -left-3 top-0 w-6 h-6 bg-[hsl(var(--primary))] rounded-full flex items-center justify-center text-white text-sm font-bold">
                              {index + 1}
                            </div>
                            <div className="bg-white border border-gray-200 rounded-xl p-5">
                              <h3 className="font-bold text-lg mb-2">{milestone.title}</h3>
                              <p className="text-sm text-gray-600 mb-3">
                                <TrendingUp className="w-4 h-4 inline mr-1" />
                                Duration: {milestone.duration}
                              </p>
                              <div className="space-y-2">
                                {milestone.resources.map((resource, rIndex) => (
                                  <a
                                    key={rIndex}
                                    href={resource}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="flex items-center text-[hsl(var(--primary))] hover:underline text-sm"
                                  >
                                    <ExternalLink className="w-4 h-4 mr-2" />
                                    Resource {rIndex + 1}
                                  </a>
                                ))}
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </TabsContent>

                    <TabsContent value="roles" data-testid="roles-tab">
                      <div className="grid md:grid-cols-2 gap-4">
                        {selectedRoadmap.job_roles.map((role, index) => (
                          <div
                            key={index}
                            className="p-5 bg-gradient-to-br from-purple-50 to-pink-50 border border-purple-100 rounded-xl"
                            data-testid={`job-role-${index}`}
                          >
                            <Briefcase className="w-6 h-6 text-purple-600 mb-2" />
                            <p className="font-bold text-lg">{role}</p>
                          </div>
                        ))}
                      </div>
                    </TabsContent>
                  </Tabs>
                </div>

                <div className="bg-gradient-to-r from-[hsl(var(--primary))] to-[hsl(var(--secondary))] rounded-2xl p-8 text-white text-center">
                  <h3 className="text-2xl font-bold mb-3">Ready to Start Your Journey?</h3>
                  <p className="mb-6 opacity-90">Complete relevant courses and build your skills for this career path</p>
                  <Button
                    size="lg"
                    variant="secondary"
                    className="bg-white text-[hsl(var(--primary))] hover:bg-gray-100 btn-hover"
                    onClick={() => navigate('/student/courses')}
                    data-testid="browse-courses-btn"
                  >
                    Browse Courses
                  </Button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default CareerPage;
