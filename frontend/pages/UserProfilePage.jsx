import { useState } from 'react';
import { Button } from '../src/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../src/components/ui/card';
import { Input } from '../src/components/ui/input';
import { Label } from '../src/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../src/components/ui/select';
import { Checkbox } from '../src/components/ui/checkbox';
import { Slider } from '../src/components/ui/slider';
import { Dialog, DialogContent, DialogTrigger } from '../src/components/ui/dialog';
import { Textarea } from '../src/components/ui/textarea';
import Header from '../components/Header';
import CVUploadsSimple from '/components/CVUploadsSimple';
import { GraduationCap, MapPin, DollarSign, Target, Upload, Sparkles, Plus, Trash2, Briefcase, Award } from 'lucide-react';

const programs = [
  'Computer Science', 'Engineering', 'Business', 'Medicine', 'Law', 
  'Liberal Arts', 'Sciences', 'Mathematics', 'Architecture', 'Philosophy'
];

const countries = [
  'United States', 'United Kingdom', 'Canada', 'Australia', 
  'Germany', 'Netherlands', 'Switzerland', 'Singapore', 'France', 'Sweden'
];

const academicLevels = [
  { value: 'high-school', label: 'High School' },
  { value: 'diploma', label: 'Diploma' },
  { value: 'bachelors', label: 'Bachelor\'s Degree' },
  { value: 'masters', label: 'Master\'s Degree' },
  { value: 'phd', label: 'PhD/Doctorate' },
  { value: 'certification', label: 'Professional Certification' },
  { value: 'other', label: 'Other' }
];

const currencies = [
  { code: 'USD', symbol: '$', name: 'US Dollar' },
  { code: 'GBP', symbol: '£', name: 'British Pound' },
  { code: 'EUR', symbol: '€', name: 'Euro' },
  { code: 'CAD', symbol: 'C$', name: 'Canadian Dollar' },
  { code: 'AUD', symbol: 'A$', name: 'Australian Dollar' },
  { code: 'INR', symbol: '₹', name: 'Indian Rupee' },
  { code: 'SGD', symbol: 'S$', name: 'Singapore Dollar' },
  { code: 'CHF', symbol: 'CHF', name: 'Swiss Franc' },
  { code: 'SEK', symbol: 'kr', name: 'Swedish Krona' },
  { code: 'JPY', symbol: '¥', name: 'Japanese Yen' },
  { code: 'CNY', symbol: '¥', name: 'Chinese Yuan' },
];

const availableExams = [
  { id: 'ielts', name: 'IELTS', min: 4.0, max: 9.0, step: 0.5, description: 'International English Language Testing System', defaultScore: 6.5 },
  { id: 'toefl', name: 'TOEFL', min: 60, max: 120, step: 5, description: 'Test of English as a Foreign Language', defaultScore: 90 },
  { id: 'gre', name: 'GRE', min: 260, max: 340, step: 5, description: 'Graduate Record Examination', defaultScore: 300 },
  { id: 'gmat', name: 'GMAT', min: 400, max: 800, step: 10, description: 'Graduate Management Admission Test', defaultScore: 600 },
  { id: 'sat', name: 'SAT', min: 800, max: 1600, step: 50, description: 'Scholastic Assessment Test', defaultScore: 1200 },
  { id: 'act', name: 'ACT', min: 1, max: 36, step: 1, description: 'American College Testing', defaultScore: 24 },
  { id: 'pte', name: 'PTE', min: 10, max: 90, step: 5, description: 'Pearson Test of English', defaultScore: 60 },
  { id: 'duolingo', name: 'Duolingo English Test', min: 10, max: 160, step: 5, description: 'Duolingo English Test', defaultScore: 110 },
];

export default function UserProfilePage({ onProfileSubmit }) {
  const [profile, setProfile] = useState({
    academicLevel: '',
    academicBackground: [],
    workExperience: [],
    gpa: 3.0,
    testScores: [],
    preferredPrograms: [],
    preferredCountries: [],
    budgetCurrency: 'USD',
    maxTuition: 50000,
    campusPreference: [],
    careerGoals: ''
  });

  const [showCVUpload, setShowCVUpload] = useState(false);
  const [isProfilePrefilled, setIsProfilePrefilled] = useState(false);
  const [selectedExams, setSelectedExams] = useState([]);

  const handleSubmit = (e) => {
    e.preventDefault();
    onProfileSubmit(profile);
  };

  const handleProgramChange = (program, checked) => {
    if (checked) {
      setProfile(prev => ({
        ...prev,
        preferredPrograms: [...prev.preferredPrograms, program]
      }));
    } else {
      setProfile(prev => ({
        ...prev,
        preferredPrograms: prev.preferredPrograms.filter(p => p !== program)
      }));
    }
  };

  const handleCountryChange = (country, checked) => {
    if (checked) {
      setProfile(prev => ({
        ...prev,
        preferredCountries: [...prev.preferredCountries, country]
      }));
    } else {
      setProfile(prev => ({
        ...prev,
        preferredCountries: prev.preferredCountries.filter(c => c !== country)
      }));
    }
  };

  const handleCVDataExtracted = (extractedData) => {
    setProfile(prev => ({
      ...prev,
      ...extractedData
    }));
    setIsProfilePrefilled(true);
    setShowCVUpload(false);
  };

  // Academic Background handlers
  const addAcademicQualification = () => {
    const newQualification = {
      id: Date.now().toString(),
      level: '',
      course: '',
      institution: '',
      yearOfCompletion: '',
      gpa: undefined
    };
    setProfile(prev => ({
      ...prev,
      academicBackground: [...prev.academicBackground, newQualification]
    }));
  };

  const updateAcademicQualification = (id, field, value) => {
    setProfile(prev => ({
      ...prev,
      academicBackground: prev.academicBackground.map(qual =>
        qual.id === id ? { ...qual, [field]: value } : qual
      )
    }));
  };

  const removeAcademicQualification = (id) => {
    setProfile(prev => ({
      ...prev,
      academicBackground: prev.academicBackground.filter(qual => qual.id !== id)
    }));
  };

  // Work Experience handlers
  const addWorkExperience = () => {
    const newExperience = {
      id: Date.now().toString(),
      jobTitle: '',
      company: '',
      startDate: '',
      endDate: '',
      currentlyWorking: false,
      description: ''
    };
    setProfile(prev => ({
      ...prev,
      workExperience: [...prev.workExperience, newExperience]
    }));
  };

  const updateWorkExperience = (id, field, value) => {
    setProfile(prev => ({
      ...prev,
      workExperience: prev.workExperience.map(exp =>
        exp.id === id ? { ...exp, [field]: value } : exp
      )
    }));
  };

  const removeWorkExperience = (id) => {
    setProfile(prev => ({
      ...prev,
      workExperience: prev.workExperience.filter(exp => exp.id !== id)
    }));
  };

  // Test Score handlers
  const handleExamToggle = (examId, checked) => {
    if (checked) {
      setSelectedExams(prev => [...prev, examId]);
      // Add test score with default value
      const exam = availableExams.find(e => e.id === examId);
      if (exam) {
        const newTestScore = {
          examName: exam.name,
          score: exam.defaultScore,
          testDate: ''
        };
        setProfile(prev => ({
          ...prev,
          testScores: [...prev.testScores, newTestScore]
        }));
      }
    } else {
      setSelectedExams(prev => prev.filter(id => id !== examId));
      // Remove test score
      const exam = availableExams.find(e => e.id === examId);
      if (exam) {
        setProfile(prev => ({
          ...prev,
          testScores: prev.testScores.filter(ts => ts.examName !== exam.name)
        }));
      }
    }
  };

  const updateTestScore = (examName, score) => {
    setProfile(prev => ({
      ...prev,
      testScores: prev.testScores.map(ts =>
        ts.examName === examName ? { ...ts, score } : ts
      )
    }));
  };

  const updateTestDate = (examName, testDate) => {
    setProfile(prev => ({
      ...prev,
      testScores: prev.testScores.map(ts =>
        ts.examName === examName ? { ...ts, testDate } : ts
      )
    }));
  };

  const getTestScore = (examName) => {
    return profile.testScores.find(ts => ts.examName === examName);
  };

  const selectedCurrency = currencies.find(c => c.code === profile.budgetCurrency) || currencies[0];

  return (
    <>
    <Header />

    <section id="find-universities" className="py-20 bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">Create Your Academic Profile</h2>
          <p className="text-xl text-gray-600 mb-6">
            Tell us about yourself to get personalized university recommendations
          </p>
          
          {/* CV Upload Option */}
          <div className="max-w-md mx-auto">
            <Dialog open={showCVUpload} onOpenChange={setShowCVUpload}>
              <DialogTrigger asChild>
                <Button variant="outline" size="lg" className="w-full">
                  <Upload className="h-5 w-5 mr-2" />
                  Upload CV for Smart Fill
                  <Sparkles className="h-4 w-4 ml-2 text-yellow-500" />
                </Button>
              </DialogTrigger>
              <DialogContent className="max-w-2xl">
                <CVUploadsSimple 
                  onDataExtracted={handleCVDataExtracted}
                  onClose={() => setShowCVUpload(false)}
                />
              </DialogContent>
            </Dialog>
            <p className="text-sm text-gray-500 mt-2">
              Save time by uploading your CV - our AI will extract your information automatically
            </p>
            
            {!isProfilePrefilled && (
              <details className="mt-4 text-left">
                <summary className="text-sm font-medium text-gray-700 cursor-pointer hover:text-primary">
                  What information can be extracted from my CV?
                </summary>
                <div className="mt-2 p-3 bg-gray-50 rounded-lg text-sm text-gray-600">
                  <p className="font-medium mb-2">Our AI can automatically detect and fill:</p>
                  <ul className="list-disc list-inside space-y-1">
                    <li>Academic level and degree information</li>
                    <li>GPA and academic performance</li>
                    <li>Test scores (IELTS, TOEFL, SAT, GMAT, GRE)</li>
                    <li>Technical skills and programming languages</li>
                    <li>Field of study preferences based on your background</li>
                    <li>Work experience and projects</li>
                  </ul>
                  <p className="mt-2 text-xs text-gray-500">
                    Supports PDF, DOC, and DOCX files. You can always review and modify the extracted information.
                  </p>
                </div>
              </details>
            )}
          </div>

          {isProfilePrefilled && (
            <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded-lg max-w-md mx-auto">
              <div className="flex items-center space-x-2">
                <Sparkles className="h-4 w-4 text-green-600" />
                <span className="text-sm font-medium text-green-800">
                  Profile pre-filled from your CV! Please review and adjust as needed.
                </span>
              </div>
            </div>
          )}
        </div>

        <form onSubmit={handleSubmit} className="space-y-8">
          {/* Academic Background */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <GraduationCap className="h-5 w-5" />
                Academic Background
              </CardTitle>
              <CardDescription>
                Add your academic qualifications (degrees, diplomas, certifications)
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {profile.academicBackground.length === 0 ? (
                <div className="text-center py-8 border-2 border-dashed border-gray-300 rounded-lg">
                  <GraduationCap className="h-12 w-12 mx-auto text-gray-400 mb-3" />
                  <p className="text-gray-500 mb-4">No academic qualifications added yet</p>
                  <Button type="button" onClick={addAcademicQualification} variant="outline">
                    <Plus className="h-4 w-4 mr-2" />
                    Add Academic Qualification
                  </Button>
                </div>
              ) : (
                <>
                  {profile.academicBackground.map((qual, index) => (
                    <div key={qual.id} className="p-4 border rounded-lg bg-gray-50 space-y-4">
                      <div className="flex justify-between items-center mb-2">
                        <h4 className="font-medium">Qualification #{index + 1}</h4>
                        <Button
                          type="button"
                          variant="ghost"
                          size="sm"
                          onClick={() => removeAcademicQualification(qual.id)}
                          className="text-red-600 hover:text-red-700 hover:bg-red-50"
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>

                      <div className="grid md:grid-cols-2 gap-4">
                        <div className="space-y-2">
                          <Label>Academic Level</Label>
                          <Select 
                            value={qual.level} 
                            onValueChange={(value) => updateAcademicQualification(qual.id, 'level', value)}
                          >
                            <SelectTrigger>
                              <SelectValue placeholder="Select level" />
                            </SelectTrigger>
                            <SelectContent>
                              {academicLevels.map(level => (
                                <SelectItem key={level.value} value={level.value}>
                                  {level.label}
                                </SelectItem>
                              ))}
                            </SelectContent>
                          </Select>
                        </div>

                        <div className="space-y-2">
                          <Label>Course/Field of Study</Label>
                          <Input
                            value={qual.course}
                            onChange={(e) => updateAcademicQualification(qual.id, 'course', e.target.value)}
                            placeholder="e.g., Computer Science"
                          />
                        </div>

                        <div className="space-y-2">
                          <Label>Institution Name</Label>
                          <Input
                            value={qual.institution}
                            onChange={(e) => updateAcademicQualification(qual.id, 'institution', e.target.value)}
                            placeholder="e.g., University of California"
                          />
                        </div>

                        <div className="space-y-2">
                          <Label>Year of Completion</Label>
                          <Input
                            value={qual.yearOfCompletion}
                            onChange={(e) => updateAcademicQualification(qual.id, 'yearOfCompletion', e.target.value)}
                            placeholder="e.g., 2024 or Expected 2025"
                          />
                        </div>

                        <div className="space-y-2">
                          <Label>GPA (Optional)</Label>
                          <Input
                            type="number"
                            step="0.01"
                            min="0"
                            max="4.0"
                            value={qual.gpa || ''}
                            onChange={(e) => updateAcademicQualification(qual.id, 'gpa', e.target.value ? parseFloat(e.target.value) : undefined)}
                            placeholder="e.g., 3.8"
                          />
                        </div>
                      </div>
                    </div>
                  ))}

                  <Button type="button" onClick={addAcademicQualification} variant="outline" className="w-full">
                    <Plus className="h-4 w-4 mr-2" />
                    Add Another Qualification
                  </Button>
                </>
              )}
            </CardContent>
          </Card>

          {/* Work Experience */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Briefcase className="h-5 w-5" />
                Work Experience
              </CardTitle>
              <CardDescription>
                Add your professional work experience (optional but recommended)
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {profile.workExperience.length === 0 ? (
                <div className="text-center py-8 border-2 border-dashed border-gray-300 rounded-lg">
                  <Briefcase className="h-12 w-12 mx-auto text-gray-400 mb-3" />
                  <p className="text-gray-500 mb-4">No work experience added yet</p>
                  <Button type="button" onClick={addWorkExperience} variant="outline">
                    <Plus className="h-4 w-4 mr-2" />
                    Add Work Experience
                  </Button>
                </div>
              ) : (
                <>
                  {profile.workExperience.map((exp, index) => (
                    <div key={exp.id} className="p-4 border rounded-lg bg-gray-50 space-y-4">
                      <div className="flex justify-between items-center mb-2">
                        <h4 className="font-medium">Experience #{index + 1}</h4>
                        <Button
                          type="button"
                          variant="ghost"
                          size="sm"
                          onClick={() => removeWorkExperience(exp.id)}
                          className="text-red-600 hover:text-red-700 hover:bg-red-50"
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>

                      <div className="grid md:grid-cols-2 gap-4">
                        <div className="space-y-2">
                          <Label>Job Title</Label>
                          <Input
                            value={exp.jobTitle}
                            onChange={(e) => updateWorkExperience(exp.id, 'jobTitle', e.target.value)}
                            placeholder="e.g., Software Engineer"
                          />
                        </div>

                        <div className="space-y-2">
                          <Label>Company</Label>
                          <Input
                            value={exp.company}
                            onChange={(e) => updateWorkExperience(exp.id, 'company', e.target.value)}
                            placeholder="e.g., Google"
                          />
                        </div>

                        <div className="space-y-2">
                          <Label>Start Date</Label>
                          <Input
                            type="month"
                            value={exp.startDate}
                            onChange={(e) => updateWorkExperience(exp.id, 'startDate', e.target.value)}
                          />
                        </div>

                        <div className="space-y-2">
                          <Label>End Date</Label>
                          <Input
                            type="month"
                            value={exp.endDate}
                            onChange={(e) => updateWorkExperience(exp.id, 'endDate', e.target.value)}
                            disabled={exp.currentlyWorking}
                            placeholder={exp.currentlyWorking ? 'Currently working' : ''}
                          />
                        </div>

                        <div className="md:col-span-2 flex items-center space-x-2">
                          <Checkbox
                            id={`currently-working-${exp.id}`}
                            checked={exp.currentlyWorking}
                            onCheckedChange={(checked) => {
                              updateWorkExperience(exp.id, 'currentlyWorking', !!checked);
                              if (checked) {
                                updateWorkExperience(exp.id, 'endDate', '');
                              }
                            }}
                          />
                          <Label htmlFor={`currently-working-${exp.id}`} className="text-sm font-normal">
                            I currently work here
                          </Label>
                        </div>

                        <div className="md:col-span-2 space-y-2">
                          <Label>Description</Label>
                          <Textarea
                            value={exp.description}
                            onChange={(e) => updateWorkExperience(exp.id, 'description', e.target.value)}
                            placeholder="Describe your role, responsibilities, and achievements..."
                            rows={3}
                          />
                        </div>
                      </div>
                    </div>
                  ))}

                  <Button type="button" onClick={addWorkExperience} variant="outline" className="w-full">
                    <Plus className="h-4 w-4 mr-2" />
                    Add Another Experience
                  </Button>
                </>
              )}
            </CardContent>
          </Card>

          {/* Test Scores */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Award className="h-5 w-5" />
                Test Scores & Examinations
              </CardTitle>
              <CardDescription>
                Select the exams you've taken and provide your scores. Only add exams relevant to your target universities.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Exam Selection */}
              <div>
                <Label className="mb-3 block">Select Exams You've Taken</Label>
                <div className="grid md:grid-cols-2 gap-3">
                  {availableExams.map((exam) => (
                    <div key={exam.id} className="flex items-start space-x-3 p-3 border rounded-lg hover:bg-gray-50">
                      <Checkbox
                        id={exam.id}
                        checked={selectedExams.includes(exam.id)}
                        onCheckedChange={(checked) => handleExamToggle(exam.id, !!checked)}
                      />
                      <div className="flex-1">
                        <Label htmlFor={exam.id} className="cursor-pointer font-medium">
                          {exam.name}
                        </Label>
                        <p className="text-xs text-gray-500 mt-0.5">{exam.description}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Score Inputs for Selected Exams */}
              {selectedExams.length > 0 && (
                <div className="space-y-6 pt-4 border-t">
                  <h4 className="font-medium">Enter Your Scores</h4>
                  {selectedExams.map((examId) => {
                    const exam = availableExams.find(e => e.id === examId);
                    if (!exam) return null;
                    
                    const testScore = getTestScore(exam.name);
                    const score = typeof testScore?.score === 'number' ? testScore.score : exam.defaultScore;
                    
                    return (
                      <div key={examId} className="p-4 bg-blue-50 border border-blue-200 rounded-lg space-y-4">
                        <div className="flex items-center justify-between">
                          <h5 className="font-medium text-blue-900">{exam.name}</h5>
                          <span className="text-sm text-blue-700">Score: {score}</span>
                        </div>
                        
                        <div className="grid md:grid-cols-3 gap-4">
                          <div className="md:col-span-2 space-y-2">
                            <Label>Score ({exam.min} - {exam.max})</Label>
                            <Slider
                              value={[score]}
                              onValueChange={(value) => updateTestScore(exam.name, value[0])}
                              min={exam.min}
                              max={exam.max}
                              step={exam.step}
                              className="w-full"
                            />
                          </div>
                          
                          <div className="space-y-2">
                            <Label>Test Date (Optional)</Label>
                            <Input
                              type="month"
                              value={testScore?.testDate || ''}
                              onChange={(e) => updateTestDate(exam.name, e.target.value)}
                            />
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}

              {selectedExams.length === 0 && (
                <div className="text-center py-6 text-gray-500">
                  <Award className="h-12 w-12 mx-auto text-gray-400 mb-3" />
                  <p>Select the exams you've taken to enter your scores</p>
                  <p className="text-sm mt-2">Different countries and universities require different exams</p>
                </div>
              )}

              {/* Overall GPA */}
              <div className="pt-4 border-t">
                <div className="space-y-2">
                  <Label htmlFor="gpa" className="flex items-center gap-2">
                    Overall GPA: {profile.gpa.toFixed(2)}
                    {isProfilePrefilled && profile.gpa !== 3.0 && (
                      <Sparkles className="h-3 w-3 text-green-600" title="Auto-filled from CV" />
                    )}
                  </Label>
                  <Slider
                    value={[profile.gpa]}
                    onValueChange={(value) => setProfile(prev => ({ ...prev, gpa: value[0] }))}
                    max={4.0}
                    min={0.0}
                    step={0.01}
                    className="w-full"
                  />
                  <p className="text-xs text-gray-500">Your cumulative grade point average (on a 4.0 scale)</p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Program Preferences */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Target className="h-5 w-5" />
                Program Preferences
              </CardTitle>
              <CardDescription>
                Select the programs you're interested in studying
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                {programs.map((program) => (
                  <div key={program} className="flex items-center space-x-2">
                    <Checkbox
                      id={program}
                      checked={profile.preferredPrograms.includes(program)}
                      onCheckedChange={(checked) => handleProgramChange(program, !!checked)}
                    />
                    <Label htmlFor={program} className="text-sm font-normal">
                      {program}
                    </Label>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Location Preferences */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <MapPin className="h-5 w-5" />
                Location Preferences
              </CardTitle>
              <CardDescription>
                Choose countries where you'd like to study
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                {countries.map((country) => (
                  <div key={country} className="flex items-center space-x-2">
                    <Checkbox
                      id={country}
                      checked={profile.preferredCountries.includes(country)}
                      onCheckedChange={(checked) => handleCountryChange(country, !!checked)}
                    />
                    <Label htmlFor={country} className="text-sm font-normal">
                      {country}
                    </Label>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Budget */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <DollarSign className="h-5 w-5" />
                Budget Preferences
              </CardTitle>
              <CardDescription>
                Set your maximum annual tuition budget
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-2">
                <Label htmlFor="currency">Currency</Label>
                <Select 
                  value={profile.budgetCurrency} 
                  onValueChange={(value) => setProfile(prev => ({ ...prev, budgetCurrency: value }))}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select currency" />
                  </SelectTrigger>
                  <SelectContent>
                    {currencies.map(currency => (
                      <SelectItem key={currency.code} value={currency.code}>
                        {currency.symbol} {currency.code} - {currency.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="budget">
                  Maximum Annual Tuition: {selectedCurrency.symbol}{profile.maxTuition.toLocaleString()}
                </Label>
                <Slider
                  value={[profile.maxTuition]}
                  onValueChange={(value) => setProfile(prev => ({ ...prev, maxTuition: value[0] }))}
                  max={100000}
                  min={10000}
                  step={5000}
                  className="w-full"
                />
              </div>
            </CardContent>
          </Card>

          {/* Submit Button */}
          <div className="text-center">
            <Button type="submit" size="lg" className="px-12 py-4">
              Find My Universities
            </Button>
          </div>
        </form>
      </div>
    </section>
    </>
  );
}

