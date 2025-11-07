export const mockScholarships = [
  {
    id: '1',
    name: 'Global Excellence Scholarship',
    provider: 'Stanford University',
    amount: 50000,
    deadline: '2025-01-15',
    eligibility: ['GPA 3.8+', 'International Student', 'STEM Field'],
    description: 'Full tuition scholarship for outstanding international students in STEM fields.',
    countries: ['Global'],
    fields: ['Computer Science', 'Engineering', 'Mathematics'],
    type: 'Merit'
  },
  {
    id: '2',
    name: 'Commonwealth Scholarship',
    provider: 'UK Government',
    amount: 30000,
    deadline: '2025-02-01',
    eligibility: ['Commonwealth Country', 'Masters/PhD', 'GPA 3.5+'],
    description: 'Scholarships for students from Commonwealth countries to study in the UK.',
    countries: ['United Kingdom'],
    fields: ['All Fields'],
    type: 'Country-specific'
  },
  {
    id: '3',
    name: 'Fulbright Program',
    provider: 'US State Department',
    amount: 45000,
    deadline: '2025-03-01',
    eligibility: ['Graduate Student', 'Research Focus', 'Academic Excellence'],
    description: 'Prestigious scholarship program for international educational exchange.',
    countries: ['United States'],
    fields: ['All Fields'],
    type: 'Merit'
  }
];

export const mockNotifications = [
  {
    id: '1',
    title: 'Application Deadline Approaching',
    message: 'Stanford University application deadline is in 15 days',
    type: 'deadline',
    date: '2024-12-20',
    read: false,
    urgent: true
  },
  {
    id: '2',
    title: 'New Scholarship Available',
    message: 'Global Excellence Scholarship now open for applications',
    type: 'scholarship',
    date: '2024-12-19',
    read: false,
    urgent: false
  },
  {
    id: '3',
    title: 'Document Upload Complete',
    message: 'Your transcripts have been successfully uploaded',
    type: 'application',
    date: '2024-12-18',
    read: true,
    urgent: false
  }
];

export const mockApplications = [
  {
    universityId: '1',
    universityName: 'Stanford University',
    program: 'MS Computer Science',
    status: 'In Progress',
    applicationDeadline: '2025-01-15',
    documentsSubmitted: 6,
    totalDocuments: 8,
    lastUpdated: '2024-12-20'
  },
  {
    universityId: '2',
    universityName: 'University of Oxford',
    program: 'MSc Engineering Science',
    status: 'Submitted',
    applicationDeadline: '2025-01-10',
    documentsSubmitted: 8,
    totalDocuments: 8,
    lastUpdated: '2024-12-15'
  }
];

export const mockVisaSteps = [
  {
    id: '1',
    title: 'Receive Acceptance Letter',
    description: 'Get your official acceptance letter from the university',
    completed: true,
    documents: ['Acceptance Letter', 'I-20 Form (US)', 'CAS Letter (UK)'],
    tips: ['Keep multiple copies', 'Ensure all details are correct']
  },
  {
    id: '2',
    title: 'Prepare Financial Documents',
    description: 'Gather all required financial documentation',
    completed: false,
    documents: ['Bank Statements', 'Scholarship Letters', 'Sponsorship Documents'],
    tips: ['Documents should be recent (within 6 months)', 'Get official translations if needed']
  },
  {
    id: '3',
    title: 'Complete Visa Application',
    description: 'Fill out the visa application form online',
    completed: false,
    documents: ['Passport', 'Photos', 'Application Form'],
    tips: ['Double-check all information', 'Pay application fees online']
  }
];