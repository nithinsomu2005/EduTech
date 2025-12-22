import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../utils/api';
import { BookOpen, Users, TrendingUp, Clock, Trophy, ArrowRight, LogOut } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { Progress } from '../components/ui/progress';

const ParentDashboard = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [children, setChildren] = useState([]);
  const [selectedChild, setSelectedChild] = useState(null);
  const [childProgress, setChildProgress] = useState(null);
  const [childActivity, setChildActivity] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchChildren();
  }, []);

  useEffect(() => {
    if (selectedChild) {
      fetchChildData(selectedChild.student_id);
    }
  }, [selectedChild]);

  const fetchChildren = async () => {
    try {
      const response = await api.get('/parent/children');
      setChildren(response.data);
      if (response.data.length > 0) {
        setSelectedChild(response.data[0]);
      }
    } catch (error) {
      console.error('Failed to fetch children:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchChildData = async (studentId) => {
    try {
      const [progressRes, activityRes] = await Promise.all([
        api.get(`/parent/progress/${studentId}`),
        api.get(`/parent/activity/${studentId}`)
      ]);
      setChildProgress(progressRes.data);
      setChildActivity(activityRes.data);
    } catch (error) {
      console.error('Failed to fetch child data:', error);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[hsl(var(--primary))] mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white border-b border-gray-200" data-testid="parent-navbar">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-2">
              <BookOpen className="w-7 h-7 text-[hsl(var(--primary))]" />
              <span className="text-xl font-bold gradient-text">EduBridge</span>
              <span className="ml-4 text-sm text-gray-600">Parent Portal</span>
            </div>
            <Button variant="ghost" onClick={handleLogout} data-testid="logout-btn">
              <LogOut className="w-4 h-4 mr-2" />
              Logout
            </Button>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8 fade-in">
          <h1 className="text-4xl font-bold mb-2">Your Children's Progress</h1>
          <p className="text-gray-600 text-lg">Monitor learning activity and achievements</p>
        </div>

        {children.length === 0 ? (
          <div className="bg-white rounded-2xl p-12 text-center" data-testid="no-children">
            <Users className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600">No children linked to this mobile number</p>
          </div>
        ) : (
          <div className="grid lg:grid-cols-3 gap-6">
            <div className="lg:col-span-1">
              <div className="bg-white rounded-2xl shadow-sm p-6" data-testid="children-list">
                <h2 className="text-xl font-bold mb-4">Your Children</h2>
                <div className="space-y-3">
                  {children.map((child) => (
                    <div
                      key={child.student_id}
                      onClick={() => setSelectedChild(child)}
                      className={`p-4 rounded-xl border-2 cursor-pointer transition-all ${
                        selectedChild?.student_id === child.student_id
                          ? 'border-[hsl(var(--primary))] bg-blue-50'
                          : 'border-gray-200 hover:border-gray-300'
                      }`}
                      data-testid={`child-card-${child.student_id}`}
                    >
                      <div className="flex items-center space-x-3">
                        <div className="w-12 h-12 bg-gradient-to-br from-blue-400 to-cyan-400 rounded-full flex items-center justify-center text-white font-bold text-lg">
                          {child.user_info?.full_name?.charAt(0) || 'S'}
                        </div>
                        <div className="flex-1">
                          <p className="font-semibold">{child.user_info?.full_name || 'Student'}</p>
                          <p className="text-sm text-gray-600">
                            Grade {child.grade_year} {child.stream ? `- ${child.stream}` : ''}
                          </p>
                        </div>
                      </div>
                      <div className="mt-3 pt-3 border-t border-gray-200">
                        <div className="flex justify-between text-sm">
                          <span className="text-gray-600">Credits:</span>
                          <span className="font-semibold">{child.total_credits}</span>
                        </div>
                        <div className="flex justify-between text-sm mt-1">
                          <span className="text-gray-600">Level:</span>
                          <span className="font-semibold">{child.level}</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            <div className="lg:col-span-2">
              {selectedChild && childProgress && (
                <div className="space-y-6">
                  <div className="grid md:grid-cols-3 gap-4">
                    <div className="bg-gradient-to-br from-blue-500 to-cyan-500 rounded-xl p-6 text-white" data-testid="child-stats-credits">
                      <Trophy className="w-8 h-8 mb-3" />
                      <p className="text-3xl font-bold mb-1">{childProgress.student.total_credits}</p>
                      <p className="text-sm opacity-90">Total Credits</p>
                    </div>
                    <div className="bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl p-6 text-white" data-testid="child-stats-level">
                      <TrendingUp className="w-8 h-8 mb-3" />
                      <p className="text-3xl font-bold mb-1">Level {childProgress.student.level}</p>
                      <p className="text-sm opacity-90">Current Level</p>
                    </div>
                    <div className="bg-gradient-to-br from-green-500 to-emerald-500 rounded-xl p-6 text-white" data-testid="child-stats-courses">
                      <BookOpen className="w-8 h-8 mb-3" />
                      <p className="text-3xl font-bold mb-1">{childProgress.progress.filter(p => p.quiz_passed).length}</p>
                      <p className="text-sm opacity-90">Completed</p>
                    </div>
                  </div>

                  <div className="bg-white rounded-2xl shadow-sm p-6" data-testid="recent-activity-section">
                    <h2 className="text-xl font-bold mb-6">Recent Activity</h2>
                    
                    <Tabs defaultValue="courses" className="w-full">
                      <TabsList className="grid w-full grid-cols-2 mb-6">
                        <TabsTrigger value="courses">Courses</TabsTrigger>
                        <TabsTrigger value="badges">Badges</TabsTrigger>
                      </TabsList>

                      <TabsContent value="courses" className="space-y-4">
                        {childActivity?.recent_courses.length > 0 ? (
                          childActivity.recent_courses.map((item, index) => (
                            <div key={index} className="border border-gray-200 rounded-lg p-4" data-testid={`recent-course-${index}`}>
                              <div className="flex items-start justify-between">
                                <div className="flex-1">
                                  <p className="font-semibold mb-1">{item.course_title}</p>
                                  <div className="flex items-center space-x-4 text-sm text-gray-600">
                                    <span className="flex items-center">
                                      <Clock className="w-4 h-4 mr-1" />
                                      {item.watch_duration} mins watched
                                    </span>
                                    {item.quiz_passed && (
                                      <span className="flex items-center text-green-600">
                                        <Trophy className="w-4 h-4 mr-1" />
                                        Quiz Passed
                                      </span>
                                    )}
                                  </div>
                                </div>
                                <div className="ml-4">
                                  {item.quiz_passed ? (
                                    <Progress value={100} className="w-20 h-2" />
                                  ) : item.video_completed ? (
                                    <Progress value={60} className="w-20 h-2" />
                                  ) : (
                                    <Progress value={30} className="w-20 h-2" />
                                  )}
                                </div>
                              </div>
                            </div>
                          ))
                        ) : (
                          <p className="text-gray-500 text-center py-8">No recent course activity</p>
                        )}
                      </TabsContent>

                      <TabsContent value="badges" className="space-y-4">
                        {childActivity?.recent_badges.length > 0 ? (
                          <div className="grid md:grid-cols-2 gap-4">
                            {childActivity.recent_badges.map((item, index) => (
                              <div key={index} className="border border-gray-200 rounded-lg p-4 flex items-center space-x-4" data-testid={`recent-badge-${index}`}>
                                <div className="text-4xl">{item.badge_icon}</div>
                                <div>
                                  <p className="font-semibold">{item.badge_name}</p>
                                  <p className="text-sm text-gray-600">Earned recently</p>
                                </div>
                              </div>
                            ))}
                          </div>
                        ) : (
                          <p className="text-gray-500 text-center py-8">No badges earned yet</p>
                        )}
                      </TabsContent>
                    </Tabs>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ParentDashboard;
