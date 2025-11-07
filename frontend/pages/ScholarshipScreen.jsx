import { useState } from 'react';
import { Button } from '../src/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../src/components/ui/card';
import { Badge } from '../src/components/ui/badge';
import { Input } from '../src/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../src/components/ui/select';
//import { Checkbox } from '.../src/components/ui/checkbox';
import { Separator } from '../src/components/ui/separator';
import { mockScholarships } from '../data/mockData';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { 

  Search, Filter, DollarSign, Calendar, MapPin, 
  BookOpen, Award, Heart, ExternalLink, Info 
} from 'lucide-react';

export function ScholarshipsScreen() {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCountry, setSelectedCountry] = useState('all');
  const [selectedField, setSelectedField] = useState('all');
  const [selectedType, setSelectedType] = useState('all');
  const [maxAmount, setMaxAmount] = useState('all');
  const [savedScholarships, setSavedScholarships] = useState([]);

  const countries = ['All Countries', ...new Set(mockScholarships.flatMap(s => s.countries))];
  const fields = ['All Fields', ...new Set(mockScholarships.flatMap(s => s.fields))];
  const types = ['All Types', 'Merit', 'Need-based', 'Country-specific', 'Field-specific'];

  const filteredScholarships = mockScholarships.filter(scholarship => {
    const matchesSearch = scholarship.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         scholarship.provider.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         scholarship.description.toLowerCase().includes(searchQuery.toLowerCase());
    
    const matchesCountry = selectedCountry === 'all' || scholarship.countries.includes(selectedCountry);
    const matchesField = selectedField === 'all' || scholarship.fields.includes(selectedField);
    const matchesType = selectedType === 'all' || scholarship.type === selectedType;
    
    let matchesAmount = true;
    if (maxAmount !== 'all') {
      const amount = parseInt(maxAmount);
      matchesAmount = scholarship.amount <= amount;
    }

    return matchesSearch && matchesCountry && matchesField && matchesType && matchesAmount;
  });

  const toggleSaved = (scholarshipId) => {
    setSavedScholarships(prev => 
      prev.includes(scholarshipId) 
        ? prev.filter(id => id !== scholarshipId)
        : [...prev, scholarshipId]
    );
  };

  const getTypeColor = (type) => {
    switch (type) {
      case 'Merit':
        return 'bg-blue-100 text-blue-800';
      case 'Need-based':
        return 'bg-green-100 text-green-800';
      case 'Country-specific':
        return 'bg-purple-100 text-purple-800';
      case 'Field-specific':
        return 'bg-orange-100 text-orange-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getDaysUntilDeadline = (deadline) => {
    const deadlineDate = new Date(deadline);
    const today = new Date();
    const diffTime = deadlineDate.getTime() - today.getTime();
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays;
  };

  return (
    <>
    <Header />
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-3xl font-bold mb-2">Scholarship Opportunities</h1>
        <p className="text-gray-600">
          Discover funding opportunities to support your international education
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="flex items-center p-6">
            <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
              <Award className="h-6 w-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Available</p>
              <p className="text-2xl font-bold">{mockScholarships.length}</p>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="flex items-center p-6">
            <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
              <DollarSign className="h-6 w-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Value</p>
              <p className="text-2xl font-bold">$2.5M</p>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="flex items-center p-6">
            <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
              <Heart className="h-6 w-6 text-purple-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Saved</p>
              <p className="text-2xl font-bold">{savedScholarships.length}</p>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="flex items-center p-6">
            <div className="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center">
              <Calendar className="h-6 w-6 text-orange-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Deadline Soon</p>
              <p className="text-2xl font-bold">3</p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Search and Filters */}
      <Card>
        <CardContent className="p-6">
          <div className="grid lg:grid-cols-6 gap-4">
            <div className="lg:col-span-2">
              <div className="relative">
                <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                <Input
                  placeholder="Search scholarships..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10"
                />
              </div>
            </div>

            <Select value={selectedCountry} onValueChange={setSelectedCountry}>
              <SelectTrigger>
                <SelectValue placeholder="Country" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Countries</SelectItem>
                {countries.slice(1).map((country) => (
                  <SelectItem key={country} value={country}>
                    {country}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>

            <Select value={selectedField} onValueChange={setSelectedField}>
              <SelectTrigger>
                <SelectValue placeholder="Field" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Fields</SelectItem>
                {fields.slice(1).map((field) => (
                  <SelectItem key={field} value={field}>
                    {field}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>

            <Select value={selectedType} onValueChange={setSelectedType}>
              <SelectTrigger>
                <SelectValue placeholder="Type" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Types</SelectItem>
                {types.slice(1).map((type) => (
                  <SelectItem key={type} value={type}>
                    {type}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>

            <Select value={maxAmount} onValueChange={setMaxAmount}>
              <SelectTrigger>
                <SelectValue placeholder="Max Amount" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Any Amount</SelectItem>
                <SelectItem value="20000">Up to $20,000</SelectItem>
                <SelectItem value="30000">Up to $30,000</SelectItem>
                <SelectItem value="50000">Up to $50,000</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      {/* Results */}
      <div className="flex items-center justify-between">
        <p className="text-gray-600">
          Showing {filteredScholarships.length} scholarship{filteredScholarships.length !== 1 ? 's' : ''}
        </p>
        <Button variant="outline" size="sm">
          <Filter className="h-4 w-4 mr-2" />
          More Filters
        </Button>
      </div>

      {/* Scholarship Cards */}
      <div className="grid lg:grid-cols-2 gap-6">
        {filteredScholarships.map((scholarship) => {
          const daysLeft = getDaysUntilDeadline(scholarship.deadline);
          const isDeadlineSoon = daysLeft <= 30 && daysLeft > 0;
          const isOverdue = daysLeft < 0;

          return (
            <Card key={scholarship.id} className="overflow-hidden">
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <CardTitle className="text-lg mb-1">{scholarship.name}</CardTitle>
                    <CardDescription className="flex items-center">
                      <BookOpen className="h-4 w-4 mr-1" />
                      {scholarship.provider}
                    </CardDescription>
                  </div>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => toggleSaved(scholarship.id)}
                    className="p-2"
                  >
                    <Heart 
                      className={`h-5 w-5 ${
                        savedScholarships.includes(scholarship.id) 
                          ? 'fill-red-500 text-red-500' 
                          : 'text-gray-400'
                      }`} 
                    />
                  </Button>
                </div>
              </CardHeader>

              <CardContent className="space-y-4">
                {/* Amount and Deadline */}
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <DollarSign className="h-5 w-5 text-green-600" />
                    <span className="text-2xl font-bold text-green-600">
                      ${scholarship.amount.toLocaleString()}
                    </span>
                  </div>
                  <div className="text-right">
                    <div className="flex items-center space-x-1">
                      <Calendar className="h-4 w-4 text-gray-500" />
                      <span className="text-sm text-gray-600">
                        {new Date(scholarship.deadline).toLocaleDateString()}
                      </span>
                    </div>
                    {isDeadlineSoon && (
                      <Badge variant="destructive" className="text-xs mt-1">
                        {daysLeft} days left
                      </Badge>
                    )}
                    {isOverdue && (
                      <Badge variant="destructive" className="text-xs mt-1">
                        Overdue
                      </Badge>
                    )}
                  </div>
                </div>

                {/* Type and Countries */}
                <div className="flex items-center justify-between">
                  <Badge className={`${getTypeColor(scholarship.type)} text-xs`}>
                    {scholarship.type}
                  </Badge>
                  <div className="flex items-center space-x-1 text-sm text-gray-600">
                    <MapPin className="h-4 w-4" />
                    <span>{scholarship.countries.join(', ')}</span>
                  </div>
                </div>

                {/* Description */}
                <p className="text-sm text-gray-600 line-clamp-2">
                  {scholarship.description}
                </p>

                {/* Fields */}
                <div>
                  <p className="text-xs font-medium text-gray-700 mb-2">Eligible Fields:</p>
                  <div className="flex flex-wrap gap-1">
                    {scholarship.fields.map((field) => (
                      <Badge key={field} variant="outline" className="text-xs">
                        {field}
                      </Badge>
                    ))}
                  </div>
                </div>

                {/* Eligibility */}
                <div>
                  <p className="text-xs font-medium text-gray-700 mb-2">Key Requirements:</p>
                  <div className="flex flex-wrap gap-1">
                    {scholarship.eligibility.slice(0, 3).map((req, index) => (
                      <Badge key={index} variant="secondary" className="text-xs">
                        {req}
                      </Badge>
                    ))}
                    {scholarship.eligibility.length > 3 && (
                      <Badge variant="outline" className="text-xs">
                        +{scholarship.eligibility.length - 3} more
                      </Badge>
                    )}
                  </div>
                </div>

                <Separator />

                {/* Actions */}
                <div className="flex space-x-2">
                  <Button className="flex-1">
                    Apply Now
                  </Button>
                  <Button variant="outline">
                    <Info className="h-4 w-4 mr-2" />
                    Details
                  </Button>
                  <Button variant="outline" size="sm">
                    <ExternalLink className="h-4 w-4" />
                  </Button>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {filteredScholarships.length === 0 && (
        <Card>
          <CardContent className="text-center py-12">
            <Award className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 mb-2">No scholarships found</h3>
            <p className="text-gray-600 mb-4">
              Try adjusting your search criteria or filters to find more opportunities.
            </p>
            <Button variant="outline" onClick={() => {
              setSearchQuery('');
              setSelectedCountry('all');
              setSelectedField('all');
              setSelectedType('all');
              setMaxAmount('all');
            }}>
              Clear Filters
            </Button>
          </CardContent>
        </Card>
      )}
    </div>
    <Footer />
    </>
  );
}