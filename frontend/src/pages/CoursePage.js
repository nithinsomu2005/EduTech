import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../utils/api';
import { ArrowLeft, Play, CheckCircle, Lock, Trophy } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Progress } from '../components/ui/progress';
import { Alert, AlertDescription } from '../components/ui/alert';

const CoursePage = () => {
  const { courseId } = useParams();
  const navigate = useNavigate();
  const [course, setCourse] = useState(null);
  const [quiz, setQuiz] = useState(null);
  const [courseProgress, setCourseProgress] = useState(null);
  const [loading, setLoading] = useState(true);
  const [videoCompleted, setVideoCompleted] = useState(false);
  const [showQuiz, setShowQuiz] = useState(false);
  const [answers, setAnswers] = useState({});
  const [quizResult, setQuizResult] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    fetchCourseData();
  }, [courseId]);

  const fetchCourseData = async () => {
    try {
      const [courseRes, quizRes] = await Promise.all([
        api.get(`/courses/${courseId}`),
        api.get(`/courses/${courseId}/quiz`).catch(() => null)
      ]);
      
      setCourse(courseRes.data);
      if (quizRes) setQuiz(quizRes.data);
      
      try {
        const progressRes = await api.get('/progress/my-progress');
        const prog = progressRes.data.find(p => p.course_id === courseId);
        if (prog) {
          setCourseProgress(prog);
          setVideoCompleted(prog.video_completed);
        } else {
          await api.post(`/progress/start?course_id=${courseId}`);
        }
      } catch (error) {
        console.error('Progress error:', error);
      }
    } catch (error) {
      console.error('Failed to fetch course:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleVideoComplete = async () => {
    try {
      await api.put(`/progress/video-complete?course_id=${courseId}&watch_duration=${course.duration_minutes}`);
      setVideoCompleted(true);
      alert('Video completed! Quiz unlocked!');
    } catch (error) {
      console.error('Failed to mark video complete:', error);
    }
  };

  const handleAnswerChange = (question, answer) => {
    setAnswers(prev => ({ ...prev, [question]: answer }));
  };

  const handleQuizSubmit = async () => {
    setSubmitting(true);
    try {
      const result = await api.post('/progress/submit-quiz', {
        quiz_id: quiz.quiz_id,
        answers
      });
      setQuizResult(result.data);
      setTimeout(() => {
        navigate('/student/dashboard');
      }, 3000);
    } catch (error) {
      console.error('Failed to submit quiz:', error);
      alert('Failed to submit quiz');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[hsl(var(--primary))] mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading course...</p>
        </div>
      </div>
    );
  }

  if (quizResult) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
        <div className="max-w-md w-full bg-white rounded-2xl shadow-xl p-8 text-center" data-testid="quiz-result">
          {quizResult.passed ? (
            <>
              <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Trophy className="w-10 h-10 text-green-600" />
              </div>
              <h2 className="text-3xl font-bold text-green-600 mb-2">Congratulations!</h2>
              <p className="text-gray-600 mb-4">You passed the quiz!</p>
              <div className="bg-gray-50 rounded-xl p-4 mb-6">
                <div className="flex justify-between mb-2">
                  <span className="font-semibold">Your Score:</span>
                  <span className="font-bold text-[hsl(var(--primary))]">{quizResult.score}/{quizResult.total}</span>
                </div>
                <div className="flex justify-between">
                  <span className="font-semibold">Credits Earned:</span>
                  <span className="font-bold text-green-600">+{quizResult.credits_earned}</span>
                </div>
              </div>
            </>
          ) : (
            <>
              <div className="w-20 h-20 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Trophy className="w-10 h-10 text-orange-600" />
              </div>
              <h2 className="text-3xl font-bold text-orange-600 mb-2">Keep Trying!</h2>
              <p className="text-gray-600 mb-4">You can retake the quiz</p>
              <div className="bg-gray-50 rounded-xl p-4 mb-6">
                <div className="flex justify-between">
                  <span className="font-semibold">Your Score:</span>
                  <span className="font-bold">{quizResult.score}/{quizResult.total}</span>
                </div>
              </div>
            </>
          )}
          <p className="text-sm text-gray-500">Redirecting to dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <Button variant="ghost" onClick={() => navigate('/student/dashboard')} data-testid="back-btn">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Dashboard
          </Button>
        </div>
      </div>

      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {!showQuiz ? (
          <div className="fade-in" data-testid="video-section">
            <div className="mb-6">
              <span className="inline-block px-3 py-1 bg-[hsl(var(--primary))]/10 text-[hsl(var(--primary))] rounded-full text-sm font-semibold mb-3">
                {course.grade_level} | {course.subject}
              </span>
              <h1 className="text-4xl font-bold mb-3">{course.title}</h1>
              <p className="text-gray-600 text-lg">{course.description}</p>
            </div>

            <div className="bg-white rounded-2xl shadow-lg overflow-hidden mb-6">
              <div className="aspect-video bg-black flex items-center justify-center">
                <iframe
                  width="100%"
                  height="100%"
                  src={course.video_url.replace('watch?v=', 'embed/')}                  allowFullScreen
                  title={course.title}
                  data-testid="video-player"
                ></iframe>
              </div>
              <div className="p-6">
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <p className="text-sm text-gray-600">Duration: {course.duration_minutes} minutes</p>
                    <p className="text-sm font-semibold text-[hsl(var(--primary))]">Earn {course.credits} credits</p>
                  </div>
                  {!videoCompleted && (
                    <Button onClick={handleVideoComplete} className="btn-hover" data-testid="mark-complete-btn">
                      <CheckCircle className="w-4 h-4 mr-2" />
                      Mark as Complete
                    </Button>
                  )}
                  {videoCompleted && !courseProgress?.quiz_passed && (
                    <Button onClick={() => setShowQuiz(true)} className="btn-hover" data-testid="take-quiz-btn">
                      <Play className="w-4 h-4 mr-2" />
                      Take Quiz
                    </Button>
                  )}
                  {courseProgress?.quiz_passed && (
                    <div className="flex items-center text-green-600 font-semibold">
                      <CheckCircle className="w-5 h-5 mr-2" />
                      Completed
                    </div>
                  )}
                </div>
                
                {!videoCompleted && (
                  <Alert className="bg-amber-50 border-amber-200">
                    <Lock className="h-4 w-4 text-amber-600" />
                    <AlertDescription className="text-amber-800">
                      Complete the video to unlock the quiz
                    </AlertDescription>
                  </Alert>
                )}
              </div>
            </div>
          </div>
        ) : (
          <div className="bg-white rounded-2xl shadow-lg p-8 fade-in" data-testid="quiz-section">
            <div className="mb-8">
              <h2 className="text-3xl font-bold mb-2">{quiz.title}</h2>
              <p className="text-gray-600">Answer all questions to earn {course.credits} credits</p>
              <div className="mt-4 p-4 bg-blue-50 rounded-lg">
                <p className="text-sm font-semibold">Passing Marks: {quiz.passing_marks}/{quiz.total_marks}</p>
              </div>
            </div>

            <div className="space-y-8">
              {quiz.questions.map((q, index) => (
                <div key={index} className="border-b border-gray-200 pb-6" data-testid={`question-${index}`}>
                  <p className="font-semibold text-lg mb-4">
                    {index + 1}. {q.question}
                  </p>
                  <div className="space-y-3">
                    {q.options.map((option, optIndex) => (
                      <label
                        key={optIndex}
                        className="flex items-center p-4 border border-gray-200 rounded-lg cursor-pointer hover:border-[hsl(var(--primary))] hover:bg-blue-50 transition-all"
                        data-testid={`option-${index}-${optIndex}`}
                      >
                        <input
                          type="radio"
                          name={`question-${index}`}
                          value={option}
                          onChange={() => handleAnswerChange(q.question, option)}
                          className="mr-3"
                        />
                        <span>{option}</span>
                      </label>
                    ))}
                  </div>
                </div>
              ))}
            </div>

            <div className="mt-8 flex gap-4">
              <Button
                variant="outline"
                onClick={() => setShowQuiz(false)}
                disabled={submitting}
                data-testid="cancel-quiz-btn"
              >
                Cancel
              </Button>
              <Button
                onClick={handleQuizSubmit}
                disabled={submitting || Object.keys(answers).length !== quiz.questions.length}
                className="btn-hover"
                data-testid="submit-quiz-btn"
              >
                {submitting ? 'Submitting...' : 'Submit Quiz'}
              </Button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default CoursePage;
