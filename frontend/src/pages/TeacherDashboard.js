import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../utils/api';
import { BookOpen, Users, TrendingUp, Award, LogOut } from 'lucide-react';
import { Button } from '../components/ui/button';

const TeacherDashboard = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [students, setStudents] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTeacherData();
  }, []);

  const fetchTeacherData = async () => {
    try {
      const response = await api.get('/teacher/students');
      setStudents(response.data.students || []);
      setStats(response.data.stats || {});
    } catch (error) {
      console.error('Failed to fetch teacher data:', error);
    } finally {
      setLoading(false);
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
      <nav className="bg-white border-b border-gray-200" data-testid="teacher-navbar">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-2">
              <BookOpen className="w-7 h-7 text-[hsl(var(--primary))]" />
              <span className="text-xl font-bold gradient-text">EduBridge</span>
              <span className="ml-4 text-sm text-gray-600">Teacher Portal</span>
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
          <h1 className="text-4xl font-bold mb-2">Welcome, {user?.full_name}!</h1>
          <p className="text-gray-600 text-lg">Manage your students and track their progress</p>
        </div>

        <div className="grid md:grid-cols-4 gap-6 mb-8">
          <div className="bg-gradient-to-br from-blue-500 to-cyan-500 rounded-2xl p-6 text-white" data-testid="stats-students">
            <div className="flex items-center justify-between mb-4">
              <Users className="w-8 h-8" />
              <span className="text-3xl font-bold">{students.length}</span>
            </div>
            <p className="text-sm opacity-90">Total Students</p>
          </div>

          <div className="bg-gradient-to-br from-green-500 to-emerald-500 rounded-2xl p-6 text-white" data-testid="stats-active">
            <div className="flex items-center justify-between mb-4">
              <TrendingUp className="w-8 h-8" />
              <span className="text-3xl font-bold">{stats?.active_students || 0}</span>
            </div>
            <p className="text-sm opacity-90">Active Students</p>
          </div>

          <div className="bg-gradient-to-br from-purple-500 to-pink-500 rounded-2xl p-6 text-white" data-testid="stats-courses">
            <div className="flex items-center justify-between mb-4">
              <BookOpen className="w-8 h-8" />
              <span className="text-3xl font-bold">{stats?.total_courses || 16}</span>
            </div>
            <p className="text-sm opacity-90">Available Courses</p>
          </div>

          <div className="bg-gradient-to-br from-orange-500 to-amber-500 rounded-2xl p-6 text-white" data-testid="stats-completion">
            <div className="flex items-center justify-between mb-4">
              <Award className="w-8 h-8" />
              <span className="text-3xl font-bold">{stats?.avg_completion || 0}%</span>
            </div>
            <p className="text-sm opacity-90">Avg Completion</p>
          </div>
        </div>

        <div className="bg-white rounded-2xl shadow-sm p-6" data-testid="students-list">
          <h2 className="text-2xl font-bold mb-6">Students in Your Institution</h2>
          
          {students.length === 0 ? (
            <div className="text-center py-12">
              <Users className="w-16 h-16 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-600">No students enrolled yet</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-gray-200">
                    <th className="text-left py-3 px-4 font-semibold">Student Name</th>
                    <th className="text-left py-3 px-4 font-semibold">Grade</th>
                    <th className="text-left py-3 px-4 font-semibold">Stream</th>
                    <th className="text-left py-3 px-4 font-semibold">Credits</th>
                    <th className="text-left py-3 px-4 font-semibold">Level</th>
                    <th className="text-left py-3 px-4 font-semibold">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {students.map((student, index) => (
                    <tr key={index} className="border-b border-gray-100 hover:bg-gray-50" data-testid={`student-row-${index}`}>
                      <td className="py-4 px-4">
                        <div className="flex items-center space-x-3">
                          <div className="w-10 h-10 bg-gradient-to-br from-blue-400 to-cyan-400 rounded-full flex items-center justify-center text-white font-bold">
                            {student.full_name?.charAt(0) || 'S'}
                          </div>
                          <div>
                            <p className="font-semibold">{student.full_name}</p>
                            <p className="text-sm text-gray-600">{student.email}</p>
                          </div>
                        </div>
                      </td>
                      <td className="py-4 px-4">{student.grade || 'N/A'}</td>
                      <td className="py-4 px-4">{student.stream || '-'}</td>
                      <td className="py-4 px-4">
                        <span className="font-semibold text-[hsl(var(--primary))]">
                          {student.total_credits || 0}
                        </span>
                      </td>
                      <td className="py-4 px-4">
                        <span className="inline-block px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm font-semibold">
                          Level {student.level || 1}
                        </span>
                      </td>
                      <td className="py-4 px-4">
                        <span className="inline-block px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm">
                          Active
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default TeacherDashboard;
