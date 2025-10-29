import React from 'react'
import { Search, Brain, Award, FileText, Map, MessageCircle } from "lucide-react";
import Header from '../components/Header';
import { useClerk,useUser } from '@clerk/clerk-react';


const LandingPage = () => {

  const { user } = useUser();
  const {openSignIn} = useClerk();
  
const devs = [
  { name: 'Anurag Chakraborty', initials: 'AC', gradient: 'from-blue-500 to-purple-600' },
  { name: 'Shriyash Parandkar', initials: 'SP', gradient: 'from-green-500 to-teal-600' },
  { name: 'Vishal Sharma', initials: 'VS', gradient: 'from-orange-500 to-red-600' },
  { name: 'Shaunak Pawar', initials: 'SP', gradient: 'from-purple-500 to-pink-600' },
  { name: 'Yashaswini Pardeshi', initials: 'YP', gradient: 'from-indigo-500 to-blue-600' },
];
const services = [
  {
    title: "University Matching",
    desc: "AI-powered university recommendations based on your academic profile, preferences, and career goals.",
    color: "blue",
    icon: Search,
  },
  {
    title: "AI Assistant",
    desc: "24/7 AI chat support to answer your questions about applications, requirements, and study abroad processes.",
    color: "yellow",
    icon: Brain,
  },
  {
    title: "Scholarship Search",
    desc: "Discover funding opportunities and scholarships tailored to your academic background and financial needs.",
    color: "green",
    icon: Award,
  },
  {
    title: "Application Tracking",
    desc: "Track your application progress and receive real-time updates on submissions and results.",
    color: "blue",
    icon: FileText,
  },
  {
    title: "Visa Guidance",
    desc: "Step-by-step visa application assistance and documentation support for your destination country.",
    color: "green",
    icon: Map,
  },
  {
    title: "SOP & Interview Prep",
    desc: "AI-powered assistance for creating strong SOPs and preparing for university interviews.",
    color: "yellow",
    icon: MessageCircle,
  },
];
  return (
   <div className="bg-white">
    {/* Header */}
    <Header />

      {/* Hero Section */}                                       
<section id="home" className="relative bg-gradient-to-r from-blue-50 to-indigo-50 pt-16 pb-20">
  <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div className="grid  lg:grid-cols-2 gap-12 items-center">
      {/* Content */}
      <div className="space-y-8">
        <div className="space-y-6">
          <h1 className="text-4xl lg:text-6xl font-bold text-gray-900 leading-tight">
            Find Your Perfect
            <span className="text-black block">University Match</span>
          </h1>
          <p className="text-xl text-gray-600 leading-relaxed">
            Discover the ideal university for your international study journey. 
            Get personalized recommendations based on your academic profile, 
            preferences, and career goals.
          </p>
        </div>
<div className="flex flex-col sm:flex-row gap-4">
  {/* Primary Button */}
  <button className="group bg-black text-white text-lg px-8 py-4 rounded-lg flex items-center justify-center border border-transparent transition-all duration-300 hover:bg-slate-200 hover:text-black hover:border-black">
    <svg
      className="mr-2 h-5 w-5 transition-transform duration-300 group-hover:rotate-12"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      viewBox="0 0 24 24"
    >
      <path d="M21 21l-4.35-4.35M17 10A7 7 0 1 1 3 10a7 7 0 0 1 14 0z" />
    </svg>
    Start Your Quest
  </button>

  {/* Secondary Button */}
  <button className="border border-black text-black text-lg px-8 py-4 rounded-lg transition-all duration-300 hover:bg-black hover:text-white hover:shadow-md">
    Learn More
  </button>
</div>


        {/* Stats */}
        <div className="grid grid-cols-3 gap-8 pt-8">
          <div className="text-center">
            <div className="flex items-center justify-center mb-2">
              {/* Star Icon Placeholder */}
              <svg className="h-6 w-6 text-yellow-500" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10 15l-5.878 3.09 1.122-6.545L.488 6.91l6.561-.955L10 0l2.951 5.955 6.561.955-4.756 4.635 1.122 6.545z" />
              </svg>
            </div>
            <div className="text-2xl font-bold text-gray-900">500+</div>
            <div className="text-sm text-gray-600">Universities</div>
          </div>
          <div className="text-center">
            <div className="flex items-center justify-center mb-2">
              {/* Users Icon */}
              <svg className="h-6 w-6 text-blue-500" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                <path d="M17 20h5v-2a4 4 0 0 0-3-3.87M9 20H4v-2a4 4 0 0 1 3-3.87M16 7a4 4 0 1 1-8 0 4 4 0 0 1 8 0zm6 13v-2a4 4 0 0 0-3-3.87M3 20v-2a4 4 0 0 1 3-3.87" />
              </svg>
            </div>
            <div className="text-2xl font-bold text-gray-900">10K+</div>
            <div className="text-sm text-gray-600">Students Helped</div>
          </div>
          <div className="text-center">
            <div className="flex items-center justify-center mb-2">
              {/* Globe Icon */}
              <svg className="h-6 w-6 text-green-500" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                <path d="M21 12A9 9 0 1 1 3 12a9 9 0 0 1 18 0z" />
              </svg>
            </div>
            <div className="text-2xl font-bold text-gray-900">50+</div>
            <div className="text-sm text-gray-600">Countries</div>
          </div>
        </div>
      </div>

      {/* Image */}
      <div className="relative">
        <div className="relative rounded-2xl overflow-hidden shadow-2xl">
          <img
            src="https://images.unsplash.com/photo-1590579491624-f98f36d4c763?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixlib=rb-4.1.0&q=80&w=1080"
            alt="University campus with diverse students studying"
            className="w-full h-96 lg:h-[500px] object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent"></div>
        </div>

        {/* Floating Card */}
        <div className="absolute -bottom-8 -left-8 bg-white rounded-xl shadow-lg p-6 border">
          <div className="flex items-center space-x-4">
            <div className="w-12 h-12 bg-black rounded-full flex items-center justify-center">
              {/* Star Icon */}
              <svg className="h-6 w-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10 15l-5.878 3.09 1.122-6.545L.488 6.91l6.561-.955L10 0l2.951 5.955 6.561.955-4.756 4.635 1.122 6.545z" />
              </svg>
            </div>
            <div>
              <div className="text-sm text-gray-600">Match Rate</div>
              <div className="text-xl font-bold text-gray-900">98.5%</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  {/* Services Section */}
  <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
    <div className="text-center mb-16">
      <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-4">Services We Offer</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">
        Comprehensive support for your international education journey, from university selection to visa guidance.
      </p>
    </div>

     <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
      {services.map(({ title, desc, color, icon: Icon }, i) => (
        <div
          key={i}
          className="bg-white rounded-xl p-8 shadow-lg border hover:shadow-xl transition-shadow"
        >
          <div
            className={`w-12 h-12 flex items-center justify-center rounded-lg mb-6`}
          >
            <Icon className={`h-8 w-8  text-${color}-500`} />
          </div>
          <h3 className="text-xl font-semibold text-gray-900 mb-4">{title}</h3>
          <p className="text-gray-600">{desc}</p>
        </div>
      ))}
    </div>
  </div>

  {/* Developed By Section */}
  <div className="bg-gray-50 py-16">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="text-center mb-12">
        <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-4">Developed By</h2>
        <p className="text-xl text-gray-600">Meet the team behind UniQuest</p>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-5 gap-8 max-w-4xl mx-auto">
        {[
          { name: 'Anurag Chakraborty', initials: 'AC', from: 'blue', to: 'purple' },
          { name: 'Shriyash Parandkar', initials: 'SP', from: 'green', to: 'teal' },
          { name: 'Vishal Sharma', initials: 'VS', from: 'orange', to: 'red' },
          { name: 'Shaunak Pawar', initials: 'SP', from: 'purple', to: 'pink' },
          { name: 'Yashaswini Pardeshi', initials: 'YP', from: 'indigo', to: 'blue' },
        ].map((dev, i) => (
          <div key={i} className="text-center">
            <div className={`w-20 h-20 bg-gradient-to-br from-${dev.from}-500 to-${dev.to}-600 rounded-full flex items-center justify-center mx-auto mb-4`}>
              <span className="text-white font-bold text-xl">{dev.initials}</span>
            </div>
            <h3 className="font-semibold text-gray-900">{dev.name}</h3>
          </div>
        ))}
      </div>
    </div>
  </div>
</section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <h3 className="text-lg font-semibold mb-4">UniQuest</h3>
              <p className="text-gray-400">
                Your AI-powered companion for international education. From university selection to visa guidance.
              </p>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Platform</h4>
              <ul className="space-y-2 text-gray-400 text-sm">
                <li>University Matching</li>
                <li>AI Assistant</li>
                <li>Application Tracking</li>
                <li>Scholarship Search</li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Support</h4>
              <ul className="space-y-2 text-gray-400 text-sm">
                <li>Visa Guidance</li>
                <li>SOP Helper</li>
                <li>Interview Prep</li>
                <li>Pre-departure</li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Company</h4>
              <ul className="space-y-2 text-gray-400 text-sm">
                <li>About Us</li>
                <li>Contact</li>
                <li>Privacy Policy</li>
                <li>Terms of Service</li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400 text-sm">
            &copy; {new Date().getFullYear()} UniQuest. Empowering international students worldwide.
          </div>
        </div>
      </footer>
    </div>  )
}

export default LandingPage