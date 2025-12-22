import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Landing from './pages/Landing';
import Login from './pages/Login';
import Register from './pages/Register';
import StudentDashboard from './pages/StudentDashboard';
import CoursePage from './pages/CoursePage';
import CoursesPage from './pages/CoursesPage';
import CareerPage from './pages/CareerPage';
import ResourcesPage from './pages/ResourcesPage';
import ParentDashboard from './pages/ParentDashboard';
import { Toaster } from './components/ui/sonner';
import './App.css';

const ProtectedRoute = ({ children, allowedRoles }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" />;
  }

  if (allowedRoles && !allowedRoles.includes(user.role)) {
    return <Navigate to="/" />;
  }

  return children;
};

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <div className="App">
          <Routes>
            <Route path="/" element={<Landing />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            
            <Route
              path="/student/dashboard"
              element={
                <ProtectedRoute allowedRoles={['student']}>
                  <StudentDashboard />
                </ProtectedRoute>
              }
            />
            <Route
              path="/student/courses"
              element={
                <ProtectedRoute allowedRoles={['student']}>
                  <CoursesPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/student/course/:courseId"
              element={
                <ProtectedRoute allowedRoles={['student']}>
                  <CoursePage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/student/career"
              element={
                <ProtectedRoute allowedRoles={['student']}>
                  <CareerPage />
                </ProtectedRoute>
              }
            />
            
            <Route
              path="/student/resources"
              element={
                <ProtectedRoute allowedRoles={['student']}>
                  <ResourcesPage />
                </ProtectedRoute>
              }
            />
            
            <Route
              path="/parent/dashboard"
              element={
                <ProtectedRoute allowedRoles={['parent']}>
                  <ParentDashboard />
                </ProtectedRoute>
              }
            />
            
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
          <Toaster />
        </div>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
