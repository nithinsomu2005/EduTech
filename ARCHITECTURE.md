# EDUBRIDGE - Complete EdTech Platform Architecture

## 1. HIGH-LEVEL SYSTEM ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────┐
│                        PRESENTATION LAYER                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │ Student  │  │ Teacher  │  │  Parent  │  │  Admin   │       │
│  │Dashboard │  │Dashboard │  │Dashboard │  │  Panel   │       │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘       │
└───────┼─────────────┼─────────────┼─────────────┼──────────────┘
        │             │             │             │
┌───────┴─────────────┴─────────────┴─────────────┴──────────────┐
│                     API GATEWAY LAYER                            │
│                    (FastAPI + JWT Auth)                          │
└──────┬──────┬──────┬──────┬──────┬──────┬──────┬───────────────┘
       │      │      │      │      │      │      │
┌──────┴──┐ ┌┴──────┴┐ ┌──┴───┐ ┌┴──────┴┐ ┌──┴────┐ ┌─────┴──┐
│  Auth   │ │Academic│ │Career│ │ Rewards│ │Parent │ │ Admin  │
│ Service │ │Service │ │Service│ │Service │ │Service│ │Service │
└──┬──────┘ └────┬───┘ └───┬──┘ └────┬───┘ └───┬───┘ └────┬───┘
   │             │          │         │         │          │
┌──┴─────────────┴──────────┴─────────┴─────────┴──────────┴────┐
│                      DATA LAYER                                 │
│                   MongoDB Collections                           │
└─────────────────────────────────────────────────────────────────┘
```

## 2. TECH STACK

### Frontend
- **Framework**: React 19
- **Routing**: React Router v7
- **Styling**: Tailwind CSS + Custom CSS
- **UI Components**: Shadcn/UI (Radix UI)
- **Forms**: React Hook Form + Zod
- **HTTP Client**: Axios
- **State**: React Context + Hooks
- **Icons**: Lucide React

### Backend
- **Framework**: FastAPI (Python)
- **Database**: MongoDB (Motor - async driver)
- **Authentication**: JWT + bcrypt
- **OTP**: In-memory cache (production: Redis/SMS service)
- **Validation**: Pydantic v2
- **CORS**: Starlette middleware

### Infrastructure
- **Database**: MongoDB
- **Auth Strategy**: JWT tokens (15d expiry)
- **File Storage**: External URLs (YouTube, Google Drive, etc.)

## 3. DATABASE SCHEMA

### users
```json
{
  "_id": ObjectId,
  "user_id": "uuid",
  "role": "student|teacher|parent|admin",
  "institution_id": "string",
  "email": "string",
  "password_hash": "string",
  "full_name": "string",
  "mobile": "string",
  "created_at": "ISO datetime",
  "last_login": "ISO datetime",
  "is_active": boolean,
  "profile_image": "url"
}
```

### students
```json
{
  "_id": ObjectId,
  "student_id": "uuid",
  "user_id": "uuid",
  "grade": "KG|1-5|6-10|Inter|BTech",
  "grade_year": number,
  "stream": "MPC|BiPC|HEC|CEC|CSE|ECE|etc",
  "parent_mobile": "string",
  "institution_name": "string",
  "dob": "date",
  "total_credits": number,
  "level": number,
  "placement_readiness": number,
  "created_at": "ISO datetime"
}
```

### parents_otp
```json
{
  "_id": ObjectId,
  "mobile": "string",
  "otp": "string",
  "student_ids": ["uuid"],
  "created_at": "ISO datetime",
  "expires_at": "ISO datetime",
  "attempts": number
}
```

### courses
```json
{
  "_id": ObjectId,
  "course_id": "uuid",
  "title": "string",
  "grade_level": "KG|1-5|6-10|Inter|BTech",
  "subject": "string",
  "video_url": "string",
  "duration_minutes": number,
  "credits": number,
  "description": "string",
  "thumbnail": "url",
  "order": number,
  "created_by": "user_id",
  "created_at": "ISO datetime"
}
```

### quizzes
```json
{
  "_id": ObjectId,
  "quiz_id": "uuid",
  "course_id": "uuid",
  "title": "string",
  "questions": [
    {
      "question": "string",
      "options": ["A", "B", "C", "D"],
      "correct_answer": "string",
      "marks": number
    }
  ],
  "passing_marks": number,
  "total_marks": number,
  "created_at": "ISO datetime"
}
```

### student_progress
```json
{
  "_id": ObjectId,
  "progress_id": "uuid",
  "student_id": "uuid",
  "course_id": "uuid",
  "video_completed": boolean,
  "watch_duration": number,
  "quiz_attempts": number,
  "quiz_passed": boolean,
  "quiz_score": number,
  "credits_earned": number,
  "completed_at": "ISO datetime",
  "last_accessed": "ISO datetime"
}
```

### badges
```json
{
  "_id": ObjectId,
  "badge_id": "uuid",
  "name": "string",
  "description": "string",
  "icon": "url",
  "criteria": {
    "type": "credits|courses|streak",
    "threshold": number
  },
  "rarity": "common|rare|epic|legendary"
}
```

### student_badges
```json
{
  "_id": ObjectId,
  "student_id": "uuid",
  "badge_id": "uuid",
  "earned_at": "ISO datetime"
}
```

### certificates
```json
{
  "_id": ObjectId,
  "certificate_id": "uuid",
  "student_id": "uuid",
  "course_id": "uuid",
  "issued_at": "ISO datetime",
  "certificate_url": "string"
}
```

### resources
```json
{
  "_id": ObjectId,
  "resource_id": "uuid",
  "grade_level": "string",
  "type": "textbook|question_paper|formula_sheet|game",
  "title": "string",
  "subject": "string",
  "url": "string",
  "thumbnail": "url",
  "year": number,
  "description": "string",
  "created_at": "ISO datetime"
}
```

### challenges
```json
{
  "_id": ObjectId,
  "challenge_id": "uuid",
  "title": "string",
  "description": "string",
  "start_date": "ISO datetime",
  "end_date": "ISO datetime",
  "grade_levels": ["string"],
  "credits_reward": number,
  "type": "quiz|coding|project",
  "difficulty": "easy|medium|hard"
}
```

### leaderboards
```json
{
  "_id": ObjectId,
  "student_id": "uuid",
  "institution_name": "string",
  "total_credits": number,
  "rank": number,
  "last_updated": "ISO datetime"
}
```

### career_roadmaps
```json
{
  "_id": ObjectId,
  "roadmap_id": "uuid",
  "title": "Full Stack Developer|Data Scientist|etc",
  "skills": ["skill1", "skill2"],
  "milestones": [
    {
      "title": "string",
      "duration": "string",
      "resources": ["url"]
    }
  ],
  "job_roles": ["string"],
  "avg_salary": "string"
}
```

## 4. AUTHENTICATION FLOW

### Student/Teacher/Admin Login
```
1. User enters institution_id + password
2. POST /api/auth/login
3. Backend validates credentials (bcrypt)
4. Generate JWT token (15 days expiry)
5. Return token + user profile
6. Frontend stores token in localStorage
7. All subsequent requests include: Authorization: Bearer <token>
```

### Parent OTP Login
```
1. Parent enters mobile number
2. POST /api/auth/parent/send-otp
3. Backend generates 6-digit OTP
4. Store in parents_otp collection (5 min expiry)
5. Send OTP (demo: return in response)
6. Parent enters OTP
7. POST /api/auth/parent/verify-otp
8. Backend validates OTP + checks expiry + attempts
9. Generate JWT token linked to student_ids
10. Return token + student data
```

### Protected Routes Middleware
```python
- Verify JWT token
- Extract user_id + role
- Check token expiry
- Attach user context to request
- Role-based access control
```

## 5. API DESIGN

### Authentication
- POST /api/auth/register - Register new user
- POST /api/auth/login - Login (institution_id + password)
- POST /api/auth/parent/send-otp - Send OTP to parent
- POST /api/auth/parent/verify-otp - Verify OTP
- GET /api/auth/me - Get current user profile
- POST /api/auth/logout - Logout

### Academic Modules
- GET /api/courses - List courses (filtered by grade)
- GET /api/courses/{course_id} - Get course details
- POST /api/progress/start - Start course
- PUT /api/progress/video-complete - Mark video complete
- POST /api/progress/submit-quiz - Submit quiz
- GET /api/student/progress - Get student progress

### Resources
- GET /api/resources - List resources (textbooks, papers, etc.)
- GET /api/resources/{resource_id} - Get resource details

### Rewards & Gamification
- GET /api/rewards/badges - List all badges
- GET /api/rewards/my-badges - Student's earned badges
- GET /api/rewards/certificates - Student's certificates
- GET /api/rewards/stats - Student stats (credits, level, rank)

### Career
- GET /api/career/roadmaps - List career roadmaps
- GET /api/career/roadmaps/{roadmap_id} - Get roadmap details
- GET /api/career/readiness - Placement readiness meter

### Parent Portal
- GET /api/parent/children - List linked students
- GET /api/parent/progress/{student_id} - Child's progress
- GET /api/parent/activity/{student_id} - Recent activity

### Teacher Portal
- POST /api/teacher/assign-course - Assign course to students
- GET /api/teacher/students - List students
- GET /api/teacher/performance - Class performance analytics
- POST /api/teacher/quiz/create - Create quiz

### Admin CMS
- POST /api/admin/courses - Create course
- PUT /api/admin/courses/{course_id} - Update course
- DELETE /api/admin/courses/{course_id} - Delete course
- POST /api/admin/resources - Add resource
- GET /api/admin/analytics - Platform analytics
- GET /api/admin/users - User management

### Challenges & Leaderboard
- GET /api/challenges - Active challenges
- POST /api/challenges/participate - Join challenge
- GET /api/leaderboard - Global/institution leaderboard

## 6. FRONTEND FOLDER STRUCTURE

```
/app/frontend/src/
├── components/
│   ├── ui/              # Shadcn components
│   ├── auth/
│   │   ├── LoginForm.js
│   │   ├── RegisterForm.js
│   │   └── ParentOTPLogin.js
│   ├── student/
│   │   ├── Dashboard.js
│   │   ├── CourseCard.js
│   │   ├── QuizPlayer.js
│   │   ├── VideoPlayer.js
│   │   ├── ProgressTracker.js
│   │   ├── BadgeDisplay.js
│   │   └── CertificateViewer.js
│   ├── teacher/
│   │   ├── TeacherDashboard.js
│   │   ├── StudentList.js
│   │   ├── PerformanceChart.js
│   │   └── QuizCreator.js
│   ├── parent/
│   │   ├── ParentDashboard.js
│   │   ├── ChildProgress.js
│   │   └── ActivityTimeline.js
│   ├── admin/
│   │   ├── AdminDashboard.js
│   │   ├── CourseManager.js
│   │   ├── UserManager.js
│   │   └── AnalyticsDashboard.js
│   ├── shared/
│   │   ├── Navbar.js
│   │   ├── Sidebar.js
│   │   ├── LoadingSpinner.js
│   │   └── ProtectedRoute.js
│   └── landing/
│       ├── Hero.js
│       ├── Features.js
│       └── Footer.js
├── pages/
│   ├── Landing.js
│   ├── Login.js
│   ├── Register.js
│   ├── StudentDashboard.js
│   ├── TeacherDashboard.js
│   ├── ParentDashboard.js
│   ├── AdminDashboard.js
│   ├── CoursePage.js
│   ├── CareerPage.js
│   └── LeaderboardPage.js
├── context/
│   ├── AuthContext.js
│   └── ThemeContext.js
├── utils/
│   ├── api.js
│   ├── auth.js
│   └── constants.js
├── hooks/
│   ├── useAuth.js
│   └── useProgress.js
├── App.js
├── App.css
└── index.css
```

## 7. BACKEND FOLDER STRUCTURE

```
/app/backend/
├── server.py            # Main FastAPI app
├── models.py            # Pydantic models
├── database.py          # MongoDB connection
├── auth/
│   ├── jwt_handler.py   # JWT generation/validation
│   ├── password.py      # Password hashing
│   └── otp_service.py   # OTP generation/validation
├── routers/
│   ├── auth.py
│   ├── courses.py
│   ├── progress.py
│   ├── rewards.py
│   ├── career.py
│   ├── parent.py
│   ├── teacher.py
│   ├── admin.py
│   └── leaderboard.py
├── services/
│   ├── academic_service.py
│   ├── reward_service.py
│   ├── analytics_service.py
│   └── certificate_service.py
├── middleware/
│   └── auth_middleware.py
├── utils/
│   ├── helpers.py
│   └── validators.py
├── requirements.txt
└── .env
```

## 8. CORE COMPONENTS & SERVICES

### Frontend Components
1. **Auth Components**: LoginForm, RegisterForm, ParentOTPLogin
2. **Student Dashboard**: Course grid, Progress bars, Badge showcase
3. **Video Player**: Track watch time, Auto-advance to quiz
4. **Quiz Player**: MCQ interface, Instant feedback, Score display
5. **Progress Tracker**: Visual timeline, Milestone markers
6. **Career Explorer**: Roadmap viewer, Skill tracker
7. **Leaderboard**: Rank display, Filter by institution
8. **Parent Dashboard**: Multi-child view, Activity feed
9. **Teacher Dashboard**: Class analytics, Assignment manager
10. **Admin CMS**: Content editor, User management

### Backend Services
1. **Auth Service**: JWT, OTP, Password management
2. **Academic Service**: Course delivery, Quiz validation
3. **Progress Service**: Track completion, Calculate credits
4. **Reward Service**: Badge assignment, Level calculation
5. **Analytics Service**: Performance metrics, Reports
6. **Certificate Service**: Generate certificates
7. **Career Service**: Roadmap delivery, Readiness calculation
8. **Leaderboard Service**: Rank calculation, Updates

## 9. UI SCREEN LAYOUTS (TEXT-BASED)

### Landing Page
```
┌─────────────────────────────────────────────────────────┐
│ [LOGO]  About  Features  Contact      [Login] [Register]│
├─────────────────────────────────────────────────────────┤
│                                                          │
│      🎓 EDUBRIDGE - Learn, Grow, Succeed                │
│      Complete EdTech Platform from KG to BTech          │
│                                                          │
│           [Get Started →]  [Watch Demo]                 │
│                                                          │
├─────────────────────────────────────────────────────────┤
│  📚 Academics  |  💼 Career  |  🏆 Rewards  |  📊 Track │
├─────────────────────────────────────────────────────────┤
│  For Students | For Teachers | For Parents              │
├─────────────────────────────────────────────────────────┤
│  Footer: Links, Social, Contact                         │
└─────────────────────────────────────────────────────────┘
```

### Student Dashboard
```
┌─────────────────────────────────────────────────────────┐
│ [LOGO]  Dashboard  Courses  Career  Leaderboard  [👤]   │
├───────────────┬─────────────────────────────────────────┤
│   Sidebar     │  Welcome, [Name] 🎉                     │
│               │  Level 5 | 2,450 Credits               │
│ 📚 My Courses │  ━━━━━━━━━━━━━━━ 65% to Level 6        │
│ 🏆 Badges     ├─────────────────────────────────────────┤
│ 📊 Progress   │  Continue Learning                      │
│ 💼 Career     │  ┌───────┐ ┌───────┐ ┌───────┐        │
│ 📋 Resources  │  │Course1│ │Course2│ │Course3│        │
│ ⚡ Challenges │  │ 45%   │ │ 80%   │ │  New  │        │
│               │  └───────┘ └───────┘ └───────┘        │
│               ├─────────────────────────────────────────┤
│               │  Your Badges (12)                       │
│               │  🥇 🏅 ⭐ 🎖️ ...                       │
│               ├─────────────────────────────────────────┤
│               │  Upcoming Challenges                    │
│               │  • Weekly Math Challenge (2 days left)  │
│               │  • Coding Sprint (Starting tomorrow)    │
└───────────────┴─────────────────────────────────────────┘
```

### Course Page (Video + Quiz)
```
┌─────────────────────────────────────────────────────────┐
│ ← Back to Courses                                        │
├─────────────────────────────────────────────────────────┤
│  Introduction to Photosynthesis                         │
│  Grade: 6-10 | Subject: Science | Duration: 15 mins     │
├─────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────┐      │
│  │                                                │      │
│  │        [YouTube Video Player]                 │      │
│  │                                                │      │
│  └──────────────────────────────────────────────┘      │
│  ━━━━━━━━━━━━━━━━━━━━━━━━ 45%                         │
│  Watch time: 7/15 mins                                  │
│                                                          │
│  [Continue Watching]                                    │
│                                                          │
│  ⚠️ Complete video to unlock quiz (Earn 50 credits!)   │
├─────────────────────────────────────────────────────────┤
│  Description:                                            │
│  Learn about photosynthesis process...                  │
└─────────────────────────────────────────────────────────┘
```

### Quiz Interface
```
┌─────────────────────────────────────────────────────────┐
│  Quiz: Photosynthesis Basics                            │
│  Question 3 of 10                          Time: 5:23   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  What is the primary pigment in photosynthesis?         │
│                                                          │
│  ○ A. Carotene                                          │
│  ○ B. Chlorophyll                                       │
│  ○ C. Xanthophyll                                       │
│  ○ D. Melanin                                           │
│                                                          │
│                    [Next Question →]                     │
│                                                          │
│  ━━━━━━━━━━━━━━━━━━━━━ 30%                            │
└─────────────────────────────────────────────────────────┘
```

### Parent Dashboard
```
┌─────────────────────────────────────────────────────────┐
│ [LOGO]  My Children  Activity  Settings  [Logout]       │
├─────────────────────────────────────────────────────────┤
│  Your Children                                           │
│                                                          │
│  ┌────────────────────────┬────────────────────────┐   │
│  │ 👦 Rahul Kumar         │ 👧 Priya Kumar         │   │
│  │ Grade 8 | MPC          │ Grade 6                │   │
│  │                        │                        │   │
│  │ Credits: 1,250         │ Credits: 850           │   │
│  │ Level: 4               │ Level: 3               │   │
│  │ Courses: 12/20         │ Courses: 8/15          │   │
│  │                        │                        │   │
│  │ Last Active: 2h ago    │ Last Active: 5h ago    │   │
│  │                        │                        │   │
│  │ [View Details]         │ [View Details]         │   │
│  └────────────────────────┴────────────────────────┘   │
│                                                          │
│  Recent Activity                                         │
│  • Rahul completed "Physics - Motion" (45 mins ago)     │
│  • Priya earned "Math Wizard" badge (3h ago)            │
│  • Rahul scored 85% in Chemistry quiz (Yesterday)       │
└─────────────────────────────────────────────────────────┘
```

### Teacher Dashboard
```
┌─────────────────────────────────────────────────────────┐
│ [LOGO]  Classes  Students  Assignments  Analytics [👤]  │
├───────────────┬─────────────────────────────────────────┤
│  Classes      │  Class Performance Overview             │
│               │                                          │
│ 📘 Grade 8-A  │  Average Score: 78%                     │
│ 📗 Grade 8-B  │  Completion Rate: 85%                   │
│ 📙 Grade 9-A  │  Active Students: 32/35                 │
│               │                                          │
│               │  [Bar Chart: Subject-wise Performance]  │
│               ├─────────────────────────────────────────┤
│               │  Recent Submissions                     │
│               │  • 12 students completed Math Quiz      │
│               │  • 8 pending Physics assignments        │
│               │                                          │
│               │  [Create New Assignment]                │
│               │  [View All Students]                    │
└───────────────┴─────────────────────────────────────────┘
```

### Admin Dashboard
```
┌─────────────────────────────────────────────────────────┐
│ [LOGO]  Users  Courses  Resources  Analytics  [Admin]   │
├───────────────┬─────────────────────────────────────────┤
│  Quick Stats  │  Platform Overview                      │
│               │                                          │
│ 👥 15,234     │  ┌──────────┬──────────┬──────────┐    │
│ Students      │  │ Students │ Teachers │  Courses │    │
│               │  │  15,234  │    456   │    892   │    │
│ 👨‍🏫 456       │  └──────────┴──────────┴──────────┘    │
│ Teachers      │                                          │
│               │  Recent Activity                         │
│ 📚 892        │  • 145 new registrations (Today)        │
│ Courses       │  • 2,340 courses completed (This week)  │
│               │  • 567 badges earned (This week)        │
│ 🏆 12,456     │                                          │
│ Badges Earned │  [Manage Content]                       │
│               │  [User Management]                      │
│               │  [View Reports]                         │
└───────────────┴─────────────────────────────────────────┘
```

## 10. DEMO FLOW FOR HACKATHON JUDGES

### Demo Script (5-minute walkthrough)

1. **Landing Page** (30 sec)
   - Show modern, attractive UI
   - Highlight: Academics + Career + Skills

2. **Student Registration & Login** (1 min)
   - Register new student with institution ID
   - Login with credentials
   - Show JWT authentication in action

3. **Student Dashboard** (1.5 min)
   - Display personalized dashboard
   - Show progress, badges, level
   - Navigate to course

4. **Course Learning** (1 min)
   - Play video (simulated watch)
   - Complete video → Auto-unlock quiz
   - Take quiz → Instant feedback
   - Earn credits and badge

5. **Parent Login** (1 min)
   - Switch to parent OTP login
   - Enter mobile → Receive OTP
   - Verify OTP → View child's progress
   - Show activity timeline

6. **Career & Leaderboard** (30 sec)
   - Browse career roadmaps
   - View placement readiness
   - Check leaderboard rankings

7. **Teacher/Admin Preview** (30 sec)
   - Quick tour of teacher dashboard
   - Show admin content management

### Key Talking Points
- ✅ Full authentication (JWT + OTP)
- ✅ Role-based dashboards
- ✅ Real-time progress tracking
- ✅ Gamification (credits, badges, levels)
- ✅ Career integration
- ✅ Parent monitoring
- ✅ Scalable architecture
- ✅ Production-ready code

## 11. SCALABILITY & FUTURE ENHANCEMENTS

### Immediate Scalability
- MongoDB horizontal scaling (sharding)
- JWT stateless authentication (no session server)
- Async FastAPI (high concurrency)
- CDN for static resources
- Database indexing on user_id, student_id, course_id

### Phase 2 Features
- Real SMS OTP integration (Twilio)
- Video hosting (own platform)
- Live classes (WebRTC)
- Discussion forums
- Peer-to-peer learning
- Mobile apps (React Native)

### Monetization Strategy
- Freemium model (basic free, premium paid)
- Institution subscriptions
- Premium courses & certifications
- Ad-free experience
- 1-on-1 tutoring marketplace
- Placement assistance services

### Advanced Features
- Offline mode (PWA)
- Multi-language support
- Advanced analytics (ML-based insights)
- Personalized learning paths
- Social learning (groups, study buddies)
- Virtual labs (simulations)

---

**Built with**: React + FastAPI + MongoDB  
**Authentication**: JWT + bcrypt + OTP  
**Design**: Modern, responsive, accessible  
**Status**: Production-ready MVP
