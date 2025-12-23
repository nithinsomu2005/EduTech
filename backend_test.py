#!/usr/bin/env python3

import requests
import sys
import json
from datetime import datetime

class EdTechAPITester:
    def __init__(self, base_url="https://edlearn.preview.emergentagent.com"):
        self.base_url = base_url
        self.student_token = None
        self.parent_token = None
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []
        self.student_id = None
        self.course_id = None
        self.quiz_id = None

    def log_result(self, test_name, success, details=""):
        """Log test results"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {test_name} - PASSED")
        else:
            print(f"❌ {test_name} - FAILED: {details}")
            self.failed_tests.append({"test": test_name, "error": details})

    def make_request(self, method, endpoint, data=None, token=None, expected_status=200):
        """Make HTTP request with proper error handling"""
        url = f"{self.base_url}/api/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        if token:
            headers['Authorization'] = f'Bearer {token}'

        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=10)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers, timeout=10)
            
            success = response.status_code == expected_status
            return success, response.json() if response.content else {}, response.status_code
            
        except requests.exceptions.RequestException as e:
            return False, {"error": str(e)}, 0
        except json.JSONDecodeError:
            return False, {"error": "Invalid JSON response"}, response.status_code

    def test_health_check(self):
        """Test API health endpoint"""
        success, data, status = self.make_request('GET', 'health')
        if success and data.get('status') == 'healthy':
            self.log_result("Health Check", True)
            return True
        else:
            self.log_result("Health Check", False, f"Status: {status}, Data: {data}")
            return False

    def test_student_registration(self):
        """Test student registration"""
        timestamp = datetime.now().strftime('%H%M%S')
        registration_data = {
            "name": f"Test Student {timestamp}",
            "username": f"test_student_{timestamp}",
            "mobile": f"987654{timestamp[-4:]}",
            "password": "password123",
            "standard": "Grade 10"
        }
        
        success, data, status = self.make_request('POST', 'auth/register', registration_data, expected_status=200)
        if success and data.get('student_id'):
            self.student_id = data['student_id']
            self.test_username = registration_data['username']
            self.test_password = registration_data['password']
            self.log_result("Student Registration", True)
            return True
        else:
            self.log_result("Student Registration", False, f"Status: {status}, Data: {data}")
            return False

    def test_student_login(self):
        """Test student login"""
        if not hasattr(self, 'test_username'):
            self.log_result("Student Login", False, "No username from registration")
            return False
            
        login_data = {
            "username": self.test_username,
            "password": self.test_password
        }
        
        success, data, status = self.make_request('POST', 'auth/login', login_data)
        if success and data.get('access_token'):
            self.student_token = data['access_token']
            self.log_result("Student Login", True)
            return True
        else:
            self.log_result("Student Login", False, f"Status: {status}, Data: {data}")
            return False

    def test_existing_student_login(self):
        """Test login with existing credentials"""
        login_data = {
            "username": "nanda_123",
            "password": "password123"
        }
        
        success, data, status = self.make_request('POST', 'auth/login', login_data)
        if success and data.get('access_token'):
            self.student_token = data['access_token']
            self.student_id = data['user']['student_id']
            self.log_result("Existing Student Login", True)
            return True
        else:
            self.log_result("Existing Student Login", False, f"Status: {status}, Data: {data}")
            return False

    def test_get_student_profile(self):
        """Test getting student profile"""
        if not self.student_token:
            self.log_result("Get Student Profile", False, "No student token")
            return False
            
        success, data, status = self.make_request('GET', 'auth/me', token=self.student_token)
        if success and data.get('student_id'):
            self.log_result("Get Student Profile", True)
            return True
        else:
            self.log_result("Get Student Profile", False, f"Status: {status}, Data: {data}")
            return False

    def test_get_courses(self):
        """Test getting courses for student"""
        if not self.student_token:
            self.log_result("Get Courses", False, "No student token")
            return False
            
        success, data, status = self.make_request('GET', 'courses', token=self.student_token)
        if success and isinstance(data, list):
            if len(data) > 0:
                self.course_id = data[0]['course_id']
            self.log_result("Get Courses", True)
            return True
        else:
            self.log_result("Get Courses", False, f"Status: {status}, Data: {data}")
            return False

    def test_get_course_details(self):
        """Test getting specific course details"""
        if not self.student_token or not self.course_id:
            self.log_result("Get Course Details", False, "No token or course ID")
            return False
            
        success, data, status = self.make_request('GET', f'courses/{self.course_id}', token=self.student_token)
        if success and data.get('course_id'):
            self.log_result("Get Course Details", True)
            return True
        else:
            self.log_result("Get Course Details", False, f"Status: {status}, Data: {data}")
            return False

    def test_start_course_progress(self):
        """Test starting course progress"""
        if not self.student_token or not self.course_id:
            self.log_result("Start Course Progress", False, "No token or course ID")
            return False
            
        success, data, status = self.make_request('POST', f'progress/start?course_id={self.course_id}', token=self.student_token)
        if success and data.get('progress'):
            self.log_result("Start Course Progress", True)
            return True
        else:
            self.log_result("Start Course Progress", False, f"Status: {status}, Data: {data}")
            return False

    def test_complete_video(self):
        """Test marking video as complete"""
        if not self.student_token or not self.course_id:
            self.log_result("Complete Video", False, "No token or course ID")
            return False
            
        success, data, status = self.make_request('PUT', f'progress/video-complete?course_id={self.course_id}&watch_duration=15', token=self.student_token)
        if success and data.get('video_completed'):
            self.log_result("Complete Video", True)
            return True
        else:
            self.log_result("Complete Video", False, f"Status: {status}, Data: {data}")
            return False

    def test_get_quiz(self):
        """Test getting quiz for course"""
        if not self.student_token or not self.course_id:
            self.log_result("Get Quiz", False, "No token or course ID")
            return False
            
        success, data, status = self.make_request('GET', f'courses/{self.course_id}/quiz', token=self.student_token)
        if success and data.get('quiz_id'):
            self.quiz_id = data['quiz_id']
            self.log_result("Get Quiz", True)
            return True
        else:
            self.log_result("Get Quiz", False, f"Status: {status}, Data: {data}")
            return False

    def test_submit_quiz(self):
        """Test submitting quiz"""
        if not self.student_token or not self.quiz_id:
            self.log_result("Submit Quiz", False, "No token or quiz ID")
            return False
            
        # Get quiz first to get questions
        success, quiz_data, status = self.make_request('GET', f'courses/{self.course_id}/quiz', token=self.student_token)
        if not success:
            self.log_result("Submit Quiz", False, "Could not fetch quiz questions")
            return False
            
        # Create answers (select first option for all questions)
        answers = {}
        for question in quiz_data.get('questions', []):
            answers[question['question']] = question['options'][0]
            
        quiz_submission = {
            "quiz_id": self.quiz_id,
            "answers": answers
        }
        
        success, data, status = self.make_request('POST', 'progress/submit-quiz', quiz_submission, token=self.student_token)
        if success and 'score' in data:
            self.log_result("Submit Quiz", True)
            return True
        else:
            self.log_result("Submit Quiz", False, f"Status: {status}, Data: {data}")
            return False

    def test_get_student_stats(self):
        """Test getting student stats"""
        if not self.student_token:
            self.log_result("Get Student Stats", False, "No student token")
            return False
            
        success, data, status = self.make_request('GET', 'rewards/stats', token=self.student_token)
        if success and 'total_credits' in data:
            self.log_result("Get Student Stats", True)
            return True
        else:
            self.log_result("Get Student Stats", False, f"Status: {status}, Data: {data}")
            return False

    def test_parent_send_otp(self):
        """Test sending OTP to parent"""
        otp_data = {"mobile": "9876543210"}
        
        success, data, status = self.make_request('POST', 'auth/parent/send-otp', otp_data)
        if success and data.get('otp'):
            self.parent_otp = data['otp']
            self.log_result("Parent Send OTP", True)
            return True
        else:
            self.log_result("Parent Send OTP", False, f"Status: {status}, Data: {data}")
            return False

    def test_parent_verify_otp(self):
        """Test verifying parent OTP"""
        if not hasattr(self, 'parent_otp'):
            self.log_result("Parent Verify OTP", False, "No OTP from send request")
            return False
            
        verify_data = {
            "mobile": "9876543210",
            "otp": self.parent_otp
        }
        
        success, data, status = self.make_request('POST', 'auth/parent/verify-otp', verify_data)
        if success and data.get('access_token'):
            self.parent_token = data['access_token']
            self.log_result("Parent Verify OTP", True)
            return True
        else:
            self.log_result("Parent Verify OTP", False, f"Status: {status}, Data: {data}")
            return False

    def test_parent_get_children(self):
        """Test getting parent's children"""
        if not self.parent_token:
            self.log_result("Parent Get Children", False, "No parent token")
            return False
            
        success, data, status = self.make_request('GET', 'parent/children', token=self.parent_token)
        if success and isinstance(data, list):
            self.log_result("Parent Get Children", True)
            return True
        else:
            self.log_result("Parent Get Children", False, f"Status: {status}, Data: {data}")
            return False

    def run_all_tests(self):
        """Run all tests in sequence"""
        print("🚀 Starting EdTech Platform API Tests")
        print("=" * 50)
        
        # Basic health check
        if not self.test_health_check():
            print("❌ Health check failed - stopping tests")
            return False
            
        # Student authentication flow
        print("\n📚 Testing Student Authentication...")
        self.test_existing_student_login()  # Use existing credentials
        self.test_get_student_profile()
        
        # Student course flow
        print("\n📖 Testing Student Course Flow...")
        self.test_get_courses()
        self.test_get_course_details()
        self.test_start_course_progress()
        self.test_complete_video()
        self.test_get_quiz()
        self.test_submit_quiz()
        self.test_get_student_stats()
        
        # Parent authentication flow
        print("\n👨‍👩‍👧‍👦 Testing Parent Authentication...")
        self.test_parent_send_otp()
        self.test_parent_verify_otp()
        self.test_parent_get_children()
        
        # Print results
        print("\n" + "=" * 50)
        print(f"📊 Test Results: {self.tests_passed}/{self.tests_run} passed")
        
        if self.failed_tests:
            print("\n❌ Failed Tests:")
            for test in self.failed_tests:
                print(f"  - {test['test']}: {test['error']}")
        
        success_rate = (self.tests_passed / self.tests_run * 100) if self.tests_run > 0 else 0
        print(f"\n✨ Success Rate: {success_rate:.1f}%")
        
        return success_rate >= 80

def main():
    tester = EdTechAPITester()
    success = tester.run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())