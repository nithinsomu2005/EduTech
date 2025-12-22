import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../utils/api';
import { ArrowLeft, BookOpen, Play } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { Progress } from '../components/ui/progress';

const CoursesPage = () => {
  const navigate = useNavigate();
  const [courses, setCourses] = useState([]);
  const [progress, setProgress] = useState([]);
  const [selectedGrade, setSelectedGrade] = useState('All');
  const [loading, setLoading] = useState(true);

  const grades = ['All', 'KG', '6-10', 'Inter', 'BTech'];

  useEffect(() => {
    fetchCourses();
  }, []);

  const fetchCourses = async () => {
    try {
      const [coursesRes, progressRes] = await Promise.all([
        api.get('/courses'),
        api.get('/progress/my-progress')
      ]);
      setCourses(coursesRes.data);
      setProgress(progressRes.data);
    } catch (error) {
      console.error('Failed to fetch courses:', error);
    } finally {
      setLoading(false);
    }
  };

  const getCourseProgress = (courseId) => {
    const prog = progress.find(p => p.course_id === courseId);
    if (!prog) return 0;
    if (prog.quiz_passed) return 100;
    if (prog.video_completed) return 60;
    if (prog.watch_duration > 0) return 30;
    return 0;
  };

  const filteredCourses = selectedGrade === 'All' 
    ? courses 
    : courses.filter(c => c.grade_level === selectedGrade);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[hsl(var(--primary))] mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading courses...</p>
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
          <h1 className="text-4xl font-bold mb-2">All Courses</h1>
          <p className="text-gray-600 text-lg">Explore courses from all grades</p>
        </div>

        <div className="bg-white rounded-2xl shadow-sm p-6 mb-8" data-testid="grade-filter">
          <div className="flex flex-wrap gap-3">
            {grades.map((grade) => (
              <Button
                key={grade}
                variant={selectedGrade === grade ? 'default' : 'outline'}
                onClick={() => setSelectedGrade(grade)}
                data-testid={`grade-filter-${grade}`}
              >
                {grade}
              </Button>
            ))}
          </div>
        </div>

        <div className="grid md:grid-cols-3 gap-6">
          {filteredCourses.map((course) => {
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
                    <Button size="sm" className="w-full btn-hover" data-testid={`start-btn-${course.course_id}`}>
                      <Play className="w-4 h-4 mr-2" />
                      Start Course
                    </Button>
                  )}
                </div>
              </div>
            );
          })}
        </div>

        {filteredCourses.length === 0 && (
          <div className="text-center py-12" data-testid="no-courses">
            <BookOpen className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600">No courses available for this grade</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default CoursesPage;
