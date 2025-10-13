import Footer from '../components/Footer'
import Header from '../components/Header'
import { useClerk, useUser } from '@clerk/clerk-react';

const LandingPage = () => {

  const {user} = useUser();
  const {openSignIn} = useClerk();
  return (
   <div className="bg-white">

    <Header />

      {/* Hero Section */}
<section id="home" className="relative bg-gradient-to-r from-blue-50 to-indigo-50 pt-16 pb-20">
  <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div className="grid lg:grid-cols-2 gap-12 items-center">
      {/* Content */}
      <div className="space-y-8">
        <div className="space-y-6">
          <h1 className="text-4xl lg:text-6xl font-bold text-gray-900 leading-tight">
            Find Your Perfect
            <span className="text-blue-600 block">University Match</span>
          </h1>
          <p className="text-xl text-gray-600 leading-relaxed">
            Discover the ideal university for your international study journey. 
            Get personalized recommendations based on your academic profile, 
            preferences, and career goals.
          </p>
        </div>

        <div className="flex flex-col sm:flex-row gap-4">
          <button className="bg-blue-600 text-white text-lg px-8 py-4 rounded-lg flex items-center justify-center hover:bg-blue-700 transition">
            {/* Search Icon Placeholder */}
            <svg className="mr-2 h-5 w-5" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
              <path d="M21 21l-4.35-4.35M17 10A7 7 0 1 1 3 10a7 7 0 0 1 14 0z" />
            </svg>
            Start Your Quest
          </button>
          <button className="border border-blue-600 text-blue-600 text-lg px-8 py-4 rounded-lg hover:bg-blue-50 transition">
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
            <div className="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center">
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
      {/* Service Cards */}
      {[
        { title: 'University Matching', desc: 'AI-powered university recommendations...', color: 'blue' },
        { title: 'AI Assistant', desc: '24/7 AI chat support...', color: 'purple' },
        { title: 'Scholarship Search', desc: 'Discover funding opportunities...', color: 'green' },
        { title: 'Application Tracking', desc: 'Track your application progress...', color: 'orange' },
        { title: 'Visa Guidance', desc: 'Step-by-step visa application...', color: 'indigo' },
        { title: 'SOP & Interview Prep', desc: 'AI-powered assistance for SOP...', color: 'red' },
      ].map((service, i) => (
        <div key={i} className="bg-white rounded-xl p-8 shadow-lg border hover:shadow-xl transition-shadow">
          <div className={`w-12 h-12 bg-${service.color}-100 rounded-lg flex items-center justify-center mb-6`}>
            <svg className={`h-6 w-6 text-${service.color}-600`} fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
              <circle cx="12" cy="12" r="10" />
            </svg>
          </div>
          <h3 className="text-xl font-semibold text-gray-900 mb-4">{service.title}</h3>
          <p className="text-gray-600">{service.desc}</p>
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
          { name: 'Yashasvini Pardeshi', initials: 'YP', from: 'indigo', to: 'blue' },
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

  <Footer/>

</div>


  )
}

export default LandingPage