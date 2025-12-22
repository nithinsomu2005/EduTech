import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../utils/api';
import { BookOpen, Trophy, Target, TrendingUp, Play, LogOut, Award, Star, ArrowRight } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Progress } from '../components/ui/progress';

const StudentDashboard = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [stats, setStats] = useState(null);
  const [courses, setCourses] = useState([]);
  const [progress, setProgress] = useState([]);
  const [badges, setBadges] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const [statsRes, coursesRes, progressRes, badgesRes] = await Promise.all([
        api.get('/rewards/stats'),
        api.get('/courses'),
        api.get('/progress/my-progress'),
        api.get('/rewards/my-badges')
      ]);
      
      setStats(statsRes.data);
      setCourses(coursesRes.data.slice(0, 6));
      setProgress(progressRes.data);
      setBadges(badgesRes.data);
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const getCourseProgress = (courseId) => {
    const prog = progress.find(p => p.course_id === courseId);
    if (!prog) return 0;
    if (prog.quiz_passed) return 100;
    if (prog.video_completed) return 60;
    if (prog.watch_duration > 0) return 30;
    return 0;
  };

  const creditsProgress = stats ? ((stats.total_credits % 500) / 500) * 100 : 0;

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[hsl(var(--primary))] mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading your dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white border-b border-gray-200" data-testid="student-navbar">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-2">
              <BookOpen className="w-7 h-7 text-[hsl(var(--primary))]" />
              <span className="text-xl font-bold gradient-text">EduBridge</span>
            </div>
            <div className="flex items-center space-x-4">
              <Button variant="ghost" onClick={() => navigate('/student/courses')} data-testid="nav-courses-btn">
                <BookOpen className="w-4 h-4 mr-2" />
                Courses
              </Button>
              <Button variant="ghost" onClick={() => navigate('/student/career')} data-testid="nav-career-btn">
                <Target className="w-4 h-4 mr-2" />
                Career
              </Button>
              <Button variant="ghost" onClick={handleLogout} data-testid="nav-logout-btn">
                <LogOut className="w-4 h-4 mr-2" />
                Logout
              </Button>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8 fade-in" data-testid="welcome-section">
          <h1 className="text-4xl font-bold mb-2">Welcome back, {user?.full_name}! 🎉</h1>
          <p className="text-gray-600 text-lg">Continue your learning journey</p>
        </div>

        <div className="grid md:grid-cols-4 gap-6 mb-8">
          <div className="bg-gradient-to-br from-blue-500 to-cyan-500 rounded-2xl p-6 text-white card-hover" data-testid="stats-credits">
            <div className="flex items-center justify-between mb-4">
              <Trophy className="w-8 h-8" />
              <span className="text-3xl font-bold">{stats?.total_credits || 0}</span>
            </div>
            <p className="text-sm opacity-90">Total Credits</p>
          </div>

          <div className="bg-gradient-to-br from-purple-500 to-pink-500 rounded-2xl p-6 text-white card-hover" data-testid="stats-level">
            <div className="flex items-center justify-between mb-4">
              <Star className="w-8 h-8" />
              <span className="text-3xl font-bold">Level {stats?.level || 1}</span>
            </div>
            <p className="text-sm opacity-90">{stats?.credits_to_next_level || 0} to next level</p>
          </div>

          <div className="bg-gradient-to-br from-green-500 to-emerald-500 rounded-2xl p-6 text-white card-hover" data-testid="stats-courses">
            <div className="flex items-center justify-between mb-4">
              <BookOpen className="w-8 h-8" />
              <span className="text-3xl font-bold">{stats?.completed_courses || 0}</span>
            </div>
            <p className="text-sm opacity-90">Courses Completed</p>
          </div>

          <div className="bg-gradient-to-br from-orange-500 to-amber-500 rounded-2xl p-6 text-white card-hover" data-testid="stats-badges">
            <div className="flex items-center justify-between mb-4">
              <Award className="w-8 h-8" />
              <span className="text-3xl font-bold">{stats?.total_badges || 0}</span>
            </div>
            <p className="text-sm opacity-90">Badges Earned</p>
          </div>
        </div>

        <div className="bg-white rounded-2xl p-6 mb-8 shadow-sm" data-testid="level-progress-section">
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-xl font-bold">Level {stats?.level || 1} Progress</h2>
            <span className="text-sm text-gray-600">{stats?.total_credits % 500 || 0} / 500 credits</span>
          </div>
          <Progress value={creditsProgress} className="h-3" />
        </div>

        <div className="mb-8">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold">Available Courses</h2>
            <Button variant="ghost" onClick={() => navigate('/student/courses')} data-testid="view-all-courses-btn">
              View All
              <ArrowRight className="w-4 h-4 ml-2" />
            </Button>
          </div>

          <div className="grid md:grid-cols-3 gap-6">
            {courses.map((course) => {
              const courseProgress = getCourseProgress(course.course_id);
              return (
                <div
                  key={course.course_id}
                  className="bg-white rounded-xl overflow-hidden shadow-sm card-hover border border-gray-200 cursor-pointer"
                  onClick={() => navigate(`/student/course/${course.course_id}`)}
                  data-testid={`course-card-${course.course_id}`}
                >
                  <div className="h-40 bg-cover bg-center" style={{ backgroundImage: `url(${course.thumbnail})` }}>
                    <div className="h-full bg-gradient-to-t from-black/60 to-transparent flex items-end p-4">
                      <span className="text-white text-xs font-semibold bg-[hsl(var(--primary))] px-2 py-1 rounded">
                        {course.grade_level}
                      </span>
                    </div>
                  </div>
                  <div className="p-4">
                    <h3 className="font-bold text-lg mb-2 line-clamp-2">{course.title}</h3>
                    <p className="text-sm text-gray-600 mb-3 line-clamp-2">{course.description}</p>
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm text-gray-500">{course.subject}</span>
                      <span className="text-sm font-semibold text-[hsl(var(--primary))]">{course.credits} credits</span>
                    </div>
                    {courseProgress > 0 ? (
                      <div>
                        <Progress value={courseProgress} className="h-2 mb-1" />
                        <span className="text-xs text-gray-500">{courseProgress}% complete</span>
                      </div>
                    ) : (
                      <Button size="sm" className="w-full btn-hover" data-testid={`start-course-btn-${course.course_id}`}>
                        <Play className="w-4 h-4 mr-2" />
                        Start Course
                      </Button>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {badges.length > 0 && (
          <div className="bg-white rounded-2xl p-6 shadow-sm" data-testid="badges-section">
            <h2 className="text-2xl font-bold mb-6">Your Badges ({badges.length})</h2>
            <div className="flex flex-wrap gap-4">
              {badges.map((badge) => (
                <div
                  key={badge.badge_id}
                  className="flex flex-col items-center p-4 bg-gradient-to-br from-yellow-50 to-amber-50 rounded-xl border border-yellow-200 card-hover"
                  data-testid={`badge-${badge.badge_id}`}
                >
                  <div className="text-4xl mb-2">{badge.icon}</div>
                  <p className="font-semibold text-center text-sm">{badge.name}</p>
                  <p className="text-xs text-gray-600 text-center mt-1">{badge.description}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default StudentDashboard;
