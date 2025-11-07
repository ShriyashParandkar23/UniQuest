import React from "react";
import Header from '../components/Header';
import { useUser, useClerk } from '@clerk/clerk-react'
import { Link, useNavigate } from 'react-router-dom'
import Footer from '../components/Footer';
import { 
  BookOpen, Calendar, Clock, CheckCircle, AlertCircle, 
  TrendingUp, FileText, GraduationCap, Bell 
} from "lucide-react";

export default function Dashboard() {
  const { isLoaded, isSignedIn, user } = useUser()
  const clerk = useClerk()
  const navigate = useNavigate()

  const displayName =
    user?.firstName ||
    user?.fullName ||
    user?.primaryEmailAddress?.emailAddress ||
    user?.emailAddresses?.[0]?.emailAddress ||
    'User'

  // Dummy data
  const journeySteps = [
    { id: 1, title: 'Profile Setup', status: 'completed', description: 'Complete your academic profile' },
    { id: 2, title: 'University Research', status: 'completed', description: 'Explore and shortlist universities' },
    { id: 3, title: 'Application Prep', status: 'in-progress', description: 'Prepare application documents' },
    { id: 4, title: 'Submit Applications', status: 'pending', description: 'Submit your applications' },
    { id: 5, title: 'Interview Prep', status: 'pending', description: 'Prepare for interviews' },
    { id: 6, title: 'Visa Process', status: 'pending', description: 'Apply for student visa' },
    { id: 7, title: 'Pre-Departure', status: 'pending', description: 'Prepare for your journey' }
  ];

  const mockApplications = [
    { id: 1, name: "Harvard University", program: "Computer Science MSc", status: "Submitted", documents: 5, totalDocuments: 7, deadline: "2025-12-01" },
    { id: 2, name: "MIT", program: "Software Engineering MSc", status: "In Progress", documents: 2, totalDocuments: 6, deadline: "2025-11-20" },
    { id: 3, name: "Stanford University", program: "AI & ML MSc", status: "Accepted", documents: 6, totalDocuments: 6, deadline: "2025-10-15" }
  ];

  const mockNotifications = [
    { id: 1, title: "Visa Interview Scheduled", message: "Your visa interview is on 20th October.", urgent: true, read: false, date: "2025-10-05" },
    { id: 2, title: "Document Missing", message: "Missing transcripts for MIT application.", urgent: true, read: false, date: "2025-10-06" },
    { id: 3, title: "Weekly Tip", message: "Check deadlines regularly.", urgent: false, read: true, date: "2025-10-01" }
  ];

  const completedSteps = journeySteps.filter(s => s.status === 'completed').length;
  const overallProgress = (completedSteps / journeySteps.length) * 100;
  const urgentNotifications = mockNotifications.filter(n => n.urgent && !n.read);

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed': return <CheckCircle className="h-5 w-5 text-green-600" />;
      case 'in-progress': return <Clock className="h-5 w-5 text-blue-600" />;
      default: return <div className="h-5 w-5 rounded-full border-2 border-gray-300" />;
    }
  };

  const getBadgeColor = (status) => {
    switch(status){
      case 'Accepted': return "bg-green-100 text-green-800 px-2 py-0.5 rounded text-xs";
      case 'Submitted': return "bg-blue-100 text-blue-800 px-2 py-0.5 rounded text-xs";
      case 'In Progress': return "bg-yellow-100 text-yellow-800 px-2 py-0.5 rounded text-xs";
      case 'Rejected': return "bg-red-100 text-red-800 px-2 py-0.5 rounded text-xs";
      default: return "bg-gray-100 text-gray-800 px-2 py-0.5 rounded text-xs";
    }
  };

  return (
    <>
    <Header />
    <div className="space-y-6 p-6 mx-40">
      {/* Welcome Section */}
      <div className="bg-gradient-to-r from-blue-600 to-indigo-600 rounded-lg p-6 text-white">
        <h1 className="text-2xl font-bold mb-2">Welcome back, {displayName}!</h1>
        <p className="text-blue-100 mb-4">You're making great progress on your university journey. Keep it up!</p>
        <div className="w-full bg-blue-200 h-2 rounded-full overflow-hidden">
          <div className="bg-white h-2" style={{ width: `${overallProgress}%` }} />
        </div>
        <p className="text-sm mt-1">{Math.round(overallProgress)}% Complete</p>
      </div>

      {/* Quick Stats */}
      <div className="grid md:grid-cols-4 gap-4">
        {[
          { icon: BookOpen, label: "Universities", value: 12, bg: "bg-blue-100", color: "text-blue-600" },
          { icon: FileText, label: "Applications", value: 5, bg: "bg-green-100", color: "text-green-600" },
          { icon: TrendingUp, label: "Match Score", value: "94%", bg: "bg-yellow-100", color: "text-yellow-600" },
          { icon: GraduationCap, label: "Scholarships", value: 8, bg: "bg-purple-100", color: "text-purple-600" },
        ].map((stat, idx) => (
          <div key={idx} className="bg-white shadow rounded-lg p-4 flex items-center space-x-4">
            <div className={`${stat.bg} p-3 rounded-lg flex items-center justify-center`}>
              <stat.icon className={`${stat.color} h-6 w-6`} />
            </div>
            <div>
              <p className="text-sm text-gray-600">{stat.label}</p>
              <p className="text-xl font-bold">{stat.value}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Journey Timeline & Applications */}
      <div className="grid lg:grid-cols-2 gap-6">
        {/* Timeline */}
        <div className="bg-white shadow rounded-lg p-4">
          <h2 className="font-bold text-lg mb-2">Your Journey Timeline</h2>
          <div className="space-y-4">
            {journeySteps.map((step, idx) => (
              <div key={step.id} className="flex items-start space-x-4">
                <div className="flex flex-col items-center">
                  {getStatusIcon(step.status)}
                  {idx < journeySteps.length - 1 && <div className="w-px h-12 bg-gray-200 mt-2" />}
                </div>
                <div>
                  <div className="flex items-center justify-between">
                    <p className="font-medium">{step.title}</p>
                    <span className={`text-xs px-2 py-0.5 rounded ${step.status==='completed'?'bg-green-100 text-green-800':step.status==='in-progress'?'bg-blue-100 text-blue-800':'bg-gray-100 text-gray-800'}`}>
                      {step.status.replace('-', ' ')}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600">{step.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Applications */}
        <div className="bg-white shadow rounded-lg p-4">
          <h2 className="font-bold text-lg mb-2">Application Status</h2>
          <div className="space-y-4">
            {mockApplications.map(app => (
              <div key={app.id} className="border rounded-lg p-3">
                <div className="flex justify-between items-center mb-1">
                  <div>
                    <p className="font-medium">{app.name}</p>
                    <p className="text-sm text-gray-600">{app.program}</p>
                  </div>
                  <span className={getBadgeColor(app.status)}>{app.status}</span>
                </div>
                <div className="w-full bg-gray-200 h-2 rounded-full overflow-hidden">
                  <div className="bg-blue-600 h-2" style={{ width: `${(app.documents / app.totalDocuments)*100}%` }} />
                </div>
                <p className="text-xs text-gray-500 mt-1">Deadline: {app.deadline}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Quick Actions & Alerts */}
      <div className="grid lg:grid-cols-2 gap-6">
        {/* Quick Actions */}
        <div className="bg-white shadow rounded-lg p-4">
          <h2 className="font-bold text-lg mb-2">Quick Actions</h2>
          <div className="grid grid-cols-2 gap-3">
            {[
              { icon: BookOpen, label: "Find Universities",path:"/UserProfile" },
              { icon: FileText, label: "SOP Helper", path: "/ai-chat" },
              { icon: TrendingUp, label: "Scholarships", path:"/ScholarshipScreen" },
              { icon: GraduationCap, label: "Ask UniQuest", path:"/ai-chat" },
            ].map((action, idx) => (
              <Link key={idx} to={action.path} className="flex flex-col items-center p-4 border rounded hover:bg-gray-50">
                <action.icon className="h-5 w-5 mb-1" />
                <span className="text-xs">{action.label}</span>
              </Link>
            ))}
          </div>
        </div>

        {/* Urgent Alerts */}
        <div className="bg-white shadow rounded-lg p-4">
          <h2 className="font-bold text-lg flex items-center mb-2">
            <Bell className="h-5 w-5 mr-2" /> Urgent Alerts
          </h2>
          <div className="space-y-3">
            {urgentNotifications.length > 0 ? urgentNotifications.map(n => (
              <div key={n.id} className="flex items-start space-x-3 p-3 bg-red-50 border border-red-200 rounded-lg">
                <AlertCircle className="h-5 w-5 text-red-600 mt-0.5" />
                <div>
                  <p className="font-medium text-red-900">{n.title}</p>
                  <p className="text-sm text-red-700">{n.message}</p>
                  <p className="text-xs text-red-600 mt-1">{n.date}</p>
                </div>
              </div>
            )) : (
              <div className="text-center py-6">
                <CheckCircle className="h-12 w-12 text-green-600 mx-auto mb-3" />
                <p className="text-sm text-gray-600">No urgent alerts</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
    <Footer/>
    </>
  );
}
