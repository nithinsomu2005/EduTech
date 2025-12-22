import React from 'react';
import { Link } from 'react-router-dom';
import { BookOpen, Target, Trophy, TrendingUp, Users, Award, ArrowRight } from 'lucide-react';
import { Button } from '../components/ui/button';

const Landing = () => {
  return (
    <div className="min-h-screen">
      <nav className="fixed top-0 w-full bg-white/80 backdrop-blur-md z-50 border-b border-gray-200" data-testid="landing-navbar">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-2">
              <BookOpen className="w-8 h-8 text-[hsl(var(--primary))]" />
              <span className="text-2xl font-bold gradient-text">EduBridge</span>
            </div>
            <div className="flex items-center space-x-4">
              <Link to="/login">
                <Button variant="ghost" data-testid="nav-login-btn">Login</Button>
              </Link>
              <Link to="/register">
                <Button className="btn-hover" data-testid="nav-register-btn">Get Started</Button>
              </Link>
            </div>
          </div>
        </div>
      </nav>

      <section className="pt-32 pb-20 px-4 sm:px-6 lg:px-8" data-testid="hero-section">
        <div className="max-w-7xl mx-auto text-center">
          <div className="inline-block mb-4 px-4 py-2 bg-[hsl(var(--primary))]/10 rounded-full text-[hsl(var(--primary))] text-sm font-semibold">
            Complete EdTech Platform
          </div>
          <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold mb-6 leading-tight">
            Learn, Grow,
            <br />
            <span className="gradient-text">Succeed Together</span>
          </h1>
          <p className="text-lg sm:text-xl text-gray-600 mb-10 max-w-3xl mx-auto">
            From Kindergarten to BTech - Master academics, build career skills, and track your progress all in one place.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link to="/register">
              <Button size="lg" className="btn-hover text-lg px-8 py-6" data-testid="hero-get-started-btn">
                Get Started Free
                <ArrowRight className="ml-2 w-5 h-5" />
              </Button>
            </Link>
            <Link to="/login">
              <Button size="lg" variant="outline" className="btn-hover text-lg px-8 py-6" data-testid="hero-login-btn">
                Sign In
              </Button>
            </Link>
          </div>
        </div>
      </section>

      <section className="py-20 bg-white" data-testid="features-section">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-4xl font-bold text-center mb-4">Everything You Need to Excel</h2>
          <p className="text-center text-gray-600 mb-16 text-lg">Comprehensive learning platform for students of all levels</p>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div className="card-hover p-8 rounded-2xl bg-gradient-to-br from-blue-50 to-cyan-50 border border-blue-100" data-testid="feature-academics">
              <div className="w-14 h-14 bg-[hsl(var(--primary))] rounded-xl flex items-center justify-center mb-4">
                <BookOpen className="w-7 h-7 text-white" />
              </div>
              <h3 className="text-2xl font-bold mb-3">Complete Academics</h3>
              <p className="text-gray-600">Structured courses from KG to BTech with video lessons, quizzes, and textbooks</p>
            </div>

            <div className="card-hover p-8 rounded-2xl bg-gradient-to-br from-green-50 to-emerald-50 border border-green-100" data-testid="feature-career">
              <div className="w-14 h-14 bg-[hsl(var(--secondary))] rounded-xl flex items-center justify-center mb-4">
                <Target className="w-7 h-7 text-white" />
              </div>
              <h3 className="text-2xl font-bold mb-3">Career Guidance</h3>
              <p className="text-gray-600">Explore career roadmaps, skill development, and placement readiness tracking</p>
            </div>

            <div className="card-hover p-8 rounded-2xl bg-gradient-to-br from-purple-50 to-pink-50 border border-purple-100" data-testid="feature-rewards">
              <div className="w-14 h-14 bg-purple-500 rounded-xl flex items-center justify-center mb-4">
                <Trophy className="w-7 h-7 text-white" />
              </div>
              <h3 className="text-2xl font-bold mb-3">Rewards & Badges</h3>
              <p className="text-gray-600">Earn credits, unlock badges, level up, and celebrate your achievements</p>
            </div>

            <div className="card-hover p-8 rounded-2xl bg-gradient-to-br from-amber-50 to-orange-50 border border-amber-100" data-testid="feature-progress">
              <div className="w-14 h-14 bg-amber-500 rounded-xl flex items-center justify-center mb-4">
                <TrendingUp className="w-7 h-7 text-white" />
              </div>
              <h3 className="text-2xl font-bold mb-3">Track Progress</h3>
              <p className="text-gray-600">Real-time progress tracking, performance analytics, and personalized insights</p>
            </div>

            <div className="card-hover p-8 rounded-2xl bg-gradient-to-br from-rose-50 to-red-50 border border-rose-100" data-testid="feature-parent">
              <div className="w-14 h-14 bg-rose-500 rounded-xl flex items-center justify-center mb-4">
                <Users className="w-7 h-7 text-white" />
              </div>
              <h3 className="text-2xl font-bold mb-3">Parent Portal</h3>
              <p className="text-gray-600">Parents can monitor children's progress and activity with secure OTP login</p>
            </div>

            <div className="card-hover p-8 rounded-2xl bg-gradient-to-br from-indigo-50 to-blue-50 border border-indigo-100" data-testid="feature-compete">
              <div className="w-14 h-14 bg-indigo-500 rounded-xl flex items-center justify-center mb-4">
                <Award className="w-7 h-7 text-white" />
              </div>
              <h3 className="text-2xl font-bold mb-3">Compete & Win</h3>
              <p className="text-gray-600">Join challenges, climb leaderboards, and compete with peers nationwide</p>
            </div>
          </div>
        </div>
      </section>

      <section className="py-20" data-testid="cta-section">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="bg-gradient-to-r from-[hsl(var(--primary))] to-[hsl(var(--secondary))] rounded-3xl p-12 text-white">
            <h2 className="text-4xl font-bold mb-4">Ready to Start Your Learning Journey?</h2>
            <p className="text-xl mb-8 opacity-90">Join thousands of students already excelling with EduBridge</p>
            <Link to="/register">
              <Button size="lg" variant="secondary" className="btn-hover text-lg px-10 py-6 bg-white text-[hsl(var(--primary))] hover:bg-gray-100" data-testid="cta-register-btn">
                Create Free Account
              </Button>
            </Link>
          </div>
        </div>
      </section>

      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="flex items-center justify-center space-x-2 mb-4">
            <BookOpen className="w-6 h-6" />
            <span className="text-xl font-bold">EduBridge</span>
          </div>
          <p className="text-gray-400">Empowering learners from KG to BTech</p>
          <p className="text-gray-500 text-sm mt-4">© 2025 EduBridge. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};

export default Landing;
