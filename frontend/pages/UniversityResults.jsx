import { useState } from 'react';
import { Button } from '../src/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../src/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../src/components/ui/select';
import { Badge } from '../src/components/ui/badge';
import UniversityCard from '../components/UniversityCard';
import { filterUniversities } from '../data/universities';
import { Link, useNavigate, useLocation } from 'react-router-dom'
import Header from '/components/Header';
import Footer from '/components/Footer';
import { Filter, SortAsc, Users, MapPin, DollarSign } from 'lucide-react';

export default function UniversityResults({ 
  onUniversitySelect, 
  onCompareUniversity,
  comparisonList = []
}) {
  const navigate = useNavigate();
  const location = useLocation();

  const handleNewSearch = () => {
  navigate('/UserProfile', { state: { profile } });
};

  
  // FIX: Get profile from router state
  const profile = location.state?.profile;
  const [sortBy, setSortBy] = useState('ranking');
  const [filterCountry, setFilterCountry] = useState('all');

if (!profile) {
  return (
    <section className="py-20 bg-gray-50 min-h-screen">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <Card className="text-center py-12">
          <CardContent>
            <h3 className="text-xl font-semibold mb-2">No Profile Data Found</h3>
            <p className="text-gray-600 mb-4">
              Please complete your profile first to see university matches.
            </p>
            <Button onClick={() => navigate('/profile')}>
              Create Your Profile
            </Button>
          </CardContent>
        </Card>
      </div>
    </section>
  );
}

  // Filter universities based on profile
  const matchingUniversities = filterUniversities({
    maxTuition: profile.maxTuition,
    countries: profile.preferredCountries.length > 0 ? profile.preferredCountries : undefined,
    programs: profile.preferredPrograms.length > 0 ? profile.preferredPrograms : undefined,
    gpa: profile.gpa
  });

  // Apply additional sorting and filtering
  let displayUniversities = [...matchingUniversities];

  // Filter by country if selected
  if (filterCountry !== 'all') {
    displayUniversities = displayUniversities.filter(uni => uni.country === filterCountry);
  }

  // Sort universities
  displayUniversities.sort((a, b) => {
    switch (sortBy) {
      case 'ranking':
        return a.ranking - b.ranking;
      case 'tuition-low':
        return a.tuitionFee - b.tuitionFee;
      case 'tuition-high':
        return b.tuitionFee - a.tuitionFee;
      case 'acceptance':
        return b.acceptanceRate - a.acceptanceRate;
      default:
        return a.ranking - b.ranking;
    }
  });

  const countries = [...new Set(matchingUniversities.map(uni => uni.country))];

  return (
    <>
    <Header />
    <section className="py-20 bg-gray-50 min-h-screen">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Your University Matches
          </h2>
          <p className="text-xl text-gray-600 mb-6">
            Found {displayUniversities.length} universities matching your profile
          </p>
          
          <Button variant="outline" onClick={handleNewSearch}>
            Refine Your Profile
          </Button>
        </div>

        {/* Profile Summary */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center">
              <Users className="h-5 w-5 mr-2" />
              Your Profile Summary
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-3 gap-6">
              <div>
                <h4 className="font-semibold mb-2">Academic Level</h4>
                <Badge variant="secondary">{profile.academicLevel}</Badge>
                <div className="mt-2 text-sm text-gray-600">
                  GPA: {profile.gpa} | IELTS: {profile.ieltsScore} | TOEFL: {profile.toeflScore}
                </div>
              </div>
              <div>
                <h4 className="font-semibold mb-2">Preferred Programs</h4>
                <div className="flex flex-wrap gap-1">
                  {profile.preferredPrograms.slice(0, 3).map(program => (
                    <Badge key={program} variant="outline" className="text-xs">
                      {program}
                    </Badge>
                  ))}
                  {profile.preferredPrograms.length > 3 && (
                    <Badge variant="outline" className="text-xs">
                      +{profile.preferredPrograms.length - 3} more
                    </Badge>
                  )}
                </div>
              </div>
              <div>
                <h4 className="font-semibold mb-2">Budget & Location</h4>
                <div className="space-y-1">
                  <div className="flex items-center text-sm text-gray-600">
                    <DollarSign className="h-4 w-4 mr-1" />
                    Up to ${profile.maxTuition.toLocaleString()}/year
                  </div>
                  <div className="flex items-center text-sm text-gray-600">
                    <MapPin className="h-4 w-4 mr-1" />
                    {profile.preferredCountries.length > 0 
                      ? profile.preferredCountries.join(', ') 
                      : 'Any country'
                    }
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Filters and Sorting */}
        <div className="flex flex-col sm:flex-row gap-4 mb-8">
          <div className="flex items-center space-x-2">
            <Filter className="h-5 w-5 text-gray-500" />
            <span className="text-sm font-medium">Filter by Country:</span>
            <Select value={filterCountry} onValueChange={setFilterCountry}>
              <SelectTrigger className="w-48">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Countries</SelectItem>
                {countries.map(country => (
                  <SelectItem className="bg-white" key={country} value={country}>
                    {country}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="flex items-center space-x-2">
            <SortAsc className="h-5 w-5 text-gray-500" />
            <span className="text-sm font-medium">Sort by:</span>
            <Select value={sortBy} onValueChange={setSortBy}>
              <SelectTrigger className="w-48">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="ranking">Best Ranking</SelectItem>
                <SelectItem value="tuition-low">Lowest Tuition</SelectItem>
                <SelectItem value="tuition-high">Highest Tuition</SelectItem>
                <SelectItem value="acceptance">Highest Acceptance Rate</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {comparisonList.length > 0 && (
            <div className="ml-auto">
              <Badge variant="outline" className="px-3 py-1">
                {comparisonList.length} universities in comparison
              </Badge>
            </div>
          )}
        </div>

        {/* Results Grid */}
        {displayUniversities.length > 0 ? (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {displayUniversities.map((university) => (
              <UniversityCard
                key={university.id}
                university={university}
                onViewDetails={onUniversitySelect}
                onCompare={onCompareUniversity}
                isInComparison={comparisonList.some(u => u.id === university.id)}
              />
            ))}
          </div>
        ) : (
          <Card className="text-center py-12">
            <CardContent>
              <h3 className="text-xl font-semibold mb-2">No universities found</h3>
              <p className="text-gray-600 mb-4">
                Try adjusting your preferences or budget to see more options.
              </p>
              <Button onClick={handleNewSearch}>Update Your Profile</Button>
            </CardContent>
          </Card>
        )}

        {/* Comparison CTA */}
        {comparisonList.length > 1 && (
          <div className="fixed bottom-6 right-6 z-50">
            <Button size="lg" className="shadow-lg">
              Compare {comparisonList.length} Universities
            </Button>
          </div>
        )}
      </div>
    </section>
    <Footer />
    </>
  );
}