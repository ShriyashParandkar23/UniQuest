export const universities = [
  {
    id: '1',
    name: 'Stanford University',
    location: 'Palo Alto, California',
    country: 'United States',
    ranking: 3,
    tuitionFee: 56169,
    acceptanceRate: 4,
    programs: ['Computer Science', 'Engineering', 'Business', 'Medicine', 'Law'],
    requirements: {
      gpa: 3.9,
      ielts: 7.0,
      toefl: 100,
      sat: 1520
    },
    features: ['Silicon Valley Location', 'Top Research', 'Alumni Network', 'Innovation Hub'],
    description: 'Stanford University is a prestigious private research university known for its academic excellence and innovation in technology.',
    image: 'https://images.unsplash.com/photo-1515255697730-f5d4ecefeb38?w=500',
    scholarships: true,
    campusType: 'Suburban',
    size: 'Large'
  },
  {
    id: '2',
    name: 'University of Oxford',
    location: 'Oxford',
    country: 'United Kingdom',
    ranking: 2,
    tuitionFee: 47000,
    acceptanceRate: 17,
    programs: ['Liberal Arts', 'Sciences', 'Engineering', 'Medicine', 'Philosophy'],
    requirements: {
      gpa: 3.8,
      ielts: 7.5,
      toefl: 110
    },
    features: ['Historic Institution', 'Tutorial System', 'World-Class Faculty', 'Research Excellence'],
    description: 'The University of Oxford is one of the oldest universities in the world, renowned for its academic tradition and excellence.',
    image: 'https://images.unsplash.com/photo-1562813733-b31f71025d54?w=500',
    scholarships: true,
    campusType: 'Urban',
    size: 'Large'
  },
  {
    id: '3',
    name: 'University of Toronto',
    location: 'Toronto, Ontario',
    country: 'Canada',
    ranking: 25,
    tuitionFee: 35000,
    acceptanceRate: 43,
    programs: ['Engineering', 'Medicine', 'Business', 'Computer Science', 'Arts'],
    requirements: {
      gpa: 3.5,
      ielts: 6.5,
      toefl: 89
    },
    features: ['Diverse Community', 'Research Opportunities', 'City Campus', 'Strong Alumni'],
    description: 'The University of Toronto is a public research university and one of the most prestigious universities in Canada.',
    image: 'https://images.unsplash.com/photo-1568515045052-f9a854d70bfd?w=500',
    scholarships: true,
    campusType: 'Urban',
    size: 'Large'
  },
  {
    id: '4',
    name: 'University of Melbourne',
    location: 'Melbourne, Victoria',
    country: 'Australia',
    ranking: 33,
    tuitionFee: 32000,
    acceptanceRate: 70,
    programs: ['Business', 'Engineering', 'Medicine', 'Arts', 'Science'],
    requirements: {
      gpa: 3.3,
      ielts: 6.5,
      toefl: 79
    },
    features: ['Vibrant City', 'Research Excellence', 'International Community', 'Industry Connections'],
    description: 'The University of Melbourne is a public research university located in Melbourne, Australia, known for its strong academic programs.',
    image: 'https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=500',
    scholarships: true,
    campusType: 'Urban',
    size: 'Large'
  },
  {
    id: '5',
    name: 'ETH Zurich',
    location: 'Zurich',
    country: 'Switzerland',
    ranking: 7,
    tuitionFee: 1500,
    acceptanceRate: 8,
    programs: ['Engineering', 'Computer Science', 'Natural Sciences', 'Mathematics', 'Architecture'],
    requirements: {
      gpa: 3.7,
      ielts: 7.0,
      toefl: 100
    },
    features: ['Low Tuition', 'Research Excellence', 'Innovation Focus', 'Mountain Setting'],
    description: 'ETH Zurich is a public research university specializing in science, technology, engineering and mathematics.',
    image: 'https://images.unsplash.com/photo-1539650116574-75c0c6d73a3e?w=500',
    scholarships: false,
    campusType: 'Urban',
    size: 'Medium'
  },
  {
    id: '6',
    name: 'National University of Singapore',
    location: 'Singapore',
    country: 'Singapore',
    ranking: 11,
    tuitionFee: 38000,
    acceptanceRate: 5,
    programs: ['Engineering', 'Business', 'Computer Science', 'Medicine', 'Law'],
    requirements: {
      gpa: 3.6,
      ielts: 6.5,
      toefl: 85
    },
    features: ['Global Hub', 'Research Excellence', 'Modern Facilities', 'Career Opportunities'],
    description: 'NUS is the flagship university of Singapore, known for its strong programs in engineering and business.',
    image: 'https://images.unsplash.com/photo-1590579491624-f98f36d4c763?w=500',
    scholarships: true,
    campusType: 'Urban',
    size: 'Large'
  }
];

export function getUniversityById(id) {
  return universities.find(uni => uni.id === id);
}

export function filterUniversities(criteria) {
  return universities.filter(uni => {
    if (criteria.maxTuition && uni.tuitionFee > criteria.maxTuition) return false;
    if (criteria.minAcceptanceRate && uni.acceptanceRate < criteria.minAcceptanceRate) return false;
    if (criteria.countries && criteria.countries.length > 0 && !criteria.countries.includes(uni.country)) return false;
    if (criteria.programs && criteria.programs.length > 0 && !criteria.programs.some(program => uni.programs.includes(program))) return false;
    if (criteria.gpa && uni.requirements.gpa > criteria.gpa + 0.3) return false;
    return true;
  });
}