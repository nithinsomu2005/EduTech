import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { BookOpen, User, Mail, Phone, Lock, Building, AlertCircle, CheckCircle } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { Alert, AlertDescription } from '../components/ui/alert';

const Register = () => {
  const navigate = useNavigate();
  const { register } = useAuth();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  
  const [formData, setFormData] = useState({
    institution_id: '',
    email: '',
    full_name: '',
    mobile: '',
    password: '',
    confirmPassword: '',
    role: 'student'
  });

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }
    
    if (formData.password.length < 6) {
      setError('Password must be at least 6 characters long');
      return;
    }
    
    setLoading(true);
    
    try {
      const { confirmPassword, ...dataToSend } = formData;
      await register(dataToSend);
      setSuccess(true);
      setTimeout(() => {
        navigate('/login');
      }, 2000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 py-12" style={{background: 'linear-gradient(135deg, #e0f2fe 0%, #dbeafe 50%, #e0e7ff 100%)'}}>
      <div className="w-full max-w-2xl">
        <div className="text-center mb-8">
          <div className="flex items-center justify-center space-x-2 mb-4">
            <BookOpen className="w-10 h-10 text-[hsl(var(--primary))]" />
            <span className="text-3xl font-bold gradient-text">EduBridge</span>
          </div>
          <h1 className="text-2xl font-bold">Create Your Account</h1>
          <p className="text-gray-600 mt-2">Join thousands of learners on EduBridge</p>
        </div>

        <div className="bg-white rounded-2xl shadow-xl p-8" data-testid="register-form-container">
          {success ? (
            <Alert className="bg-green-50 border-green-200 mb-6" data-testid="success-alert">
              <CheckCircle className="h-5 w-5 text-green-600" />
              <AlertDescription className="text-green-800 ml-2">
                Registration successful! Redirecting to login...
              </AlertDescription>
            </Alert>
          ) : null}

          {error && (
            <Alert variant="destructive" className="mb-6" data-testid="error-alert">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            <div className="grid md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="full_name">Full Name</Label>
                <div className="relative">
                  <User className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
                  <Input
                    id="full_name"
                    data-testid="full-name-input"
                    type="text"
                    placeholder="John Doe"
                    className="pl-10"
                    value={formData.full_name}
                    onChange={(e) => handleChange('full_name', e.target.value)}
                    required
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <div className="relative">
                  <Mail className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
                  <Input
                    id="email"
                    data-testid="email-input"
                    type="email"
                    placeholder="john@example.com"
                    className="pl-10"
                    value={formData.email}
                    onChange={(e) => handleChange('email', e.target.value)}
                    required
                  />
                </div>
              </div>
            </div>

            <div className="grid md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="institution_id">Institution ID</Label>
                <div className="relative">
                  <Building className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
                  <Input
                    id="institution_id"
                    data-testid="institution-id-input"
                    type="text"
                    placeholder="INST001"
                    className="pl-10"
                    value={formData.institution_id}
                    onChange={(e) => handleChange('institution_id', e.target.value)}
                    required
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="mobile">Mobile Number</Label>
                <div className="relative">
                  <Phone className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
                  <Input
                    id="mobile"
                    data-testid="mobile-input"
                    type="tel"
                    placeholder="9876543210"
                    className="pl-10"
                    value={formData.mobile}
                    onChange={(e) => handleChange('mobile', e.target.value)}
                    required
                  />
                </div>
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="role">I am a</Label>
              <Select value={formData.role} onValueChange={(value) => handleChange('role', value)}>
                <SelectTrigger data-testid="role-select">
                  <SelectValue placeholder="Select your role" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="student">Student</SelectItem>
                  <SelectItem value="teacher">Teacher</SelectItem>
                  <SelectItem value="admin">Admin</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="grid md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="password">Password</Label>
                <div className="relative">
                  <Lock className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
                  <Input
                    id="password"
                    data-testid="password-input"
                    type="password"
                    placeholder="Min. 6 characters"
                    className="pl-10"
                    value={formData.password}
                    onChange={(e) => handleChange('password', e.target.value)}
                    required
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="confirmPassword">Confirm Password</Label>
                <div className="relative">
                  <Lock className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
                  <Input
                    id="confirmPassword"
                    data-testid="confirm-password-input"
                    type="password"
                    placeholder="Re-enter password"
                    className="pl-10"
                    value={formData.confirmPassword}
                    onChange={(e) => handleChange('confirmPassword', e.target.value)}
                    required
                  />
                </div>
              </div>
            </div>

            <Button type="submit" className="w-full btn-hover" disabled={loading} data-testid="register-submit-btn">
              {loading ? 'Creating Account...' : 'Create Account'}
            </Button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-sm text-gray-600">
              Already have an account?{' '}
              <Link to="/login" className="text-[hsl(var(--primary))] font-semibold hover:underline" data-testid="login-link">
                Sign in here
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Register;
