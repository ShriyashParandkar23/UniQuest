import { useState, useRef } from 'react';
import { Button } from '../src/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../src/components/ui/card';
import { Alert, AlertDescription } from '../src/components/ui/alert';
import { DialogTitle,DialogContent } from '../src/components/ui/dialog';
import { Upload, FileText, CheckCircle, AlertCircle, X, Sparkles } from 'lucide-react';

export default function CVUploadsSimple({ onDataExtracted, onClose }) {
  const [file, setFile] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);

  const handleFileSelect = (selectedFile) => {
    // Validate file type
    const allowedTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    if (!allowedTypes.includes(selectedFile.type)) {
      setError('Please upload a PDF or Word document');
      return;
    }

    // Validate file size (max 10MB)
    if (selectedFile.size > 10 * 1024 * 1024) {
      setError('File size must be less than 10MB');
      return;
    }

    setFile(selectedFile);
    setError(null);
  };

  const processCV = async () => {
    if (!file) return;

    setIsProcessing(true);
    setError(null);

    try {
      // Simulate processing delay
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      const mockData = {
        academicLevel: 'undergraduate',
        gpa: 3.8,
        ieltsScore: 7.5,
        toeflScore: 105,
        satScore: 1450,
        gmatScore: 720,
        preferredPrograms: ['Computer Science', 'Engineering']
      };

      onDataExtracted(mockData);
      setIsProcessing(false);
      
      // Close the dialog after a brief delay to show success
      setTimeout(() => {
        onClose();
      }, 500);
      
    } catch (err) {
      setError('Failed to process CV. Please try again.');
      setIsProcessing(false);
    }
  };

  const removeFile = () => {
    setFile(null);
    setError(null);
  };

  return (
    <Card className="w-full max-w-2xl bg-white">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="flex items-center gap-2">
              <Upload className="h-5 w-5" />
              Upload Your CV
            </CardTitle>
            <CardDescription>
              Let our AI extract your academic information automatically
            </CardDescription>
          </div>
          <Button variant="ghost" size="sm" onClick={onClose}>
            <X className="h-4 w-4" />
          </Button>
        </div>
      </CardHeader>

     <CardContent className="space-y-6 bg-gradient-to-br from-gray-50 to-white p-6">
        {/* File Upload Area */}
        {!file && (
          <div
            className="relative border-2 border-dashed border-gray-300 rounded-xl p-12 text-center hover:border-primary hover:bg-primary/5 transition-all duration-300 cursor-pointer group bg-white shadow-sm"
            onClick={() => fileInputRef.current?.click()}
          >
            <div className="absolute inset-0 bg-gradient-to-br from-primary/5 to-transparent rounded-xl opacity-0 group-hover:opacity-100 transition-opacity" />
            <div className="relative">
              <div className="bg-primary/10 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform">
                <Upload className="h-10 w-10 text-primary" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Drop your CV here or click to browse
              </h3>
              <p className="text-sm text-gray-600 mb-6 max-w-md mx-auto">
                Supports PDF, DOC, and DOCX files up to 10MB
              </p>
              <Button variant="outline" className="shadow-sm hover:shadow-md transition-shadow">
                <FileText className="h-4 w-4 mr-2" />
                Choose File
              </Button>
            </div>
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf,.doc,.docx"
              onChange={(e) => e.target.files?.[0] && handleFileSelect(e.target.files[0])}
              className="hidden"
            />
          </div>
        )}

        {/* File Selected */}
        {file && (
          <div className="space-y-4">
            <div className="flex items-center justify-between p-5 border border-gray-200 rounded-xl bg-white shadow-sm hover:shadow-md transition-shadow">
              <div className="flex items-center space-x-4">
                <div className="bg-primary/10 p-3 rounded-lg">
                  <FileText className="h-8 w-8 text-primary" />
                </div>
                <div>
                  <p className="font-semibold text-gray-900">{file.name}</p>
                  <p className="text-sm text-gray-500">
                    {(file.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                </div>
              </div>
              <Button 
                variant="ghost" 
                size="sm" 
                onClick={removeFile}
                className="hover:bg-red-50 hover:text-red-600 transition-colors"
              >
                <X className="h-5 w-5" />
              </Button>
            </div>

            {isProcessing ? (
              <div className="text-center py-6 bg-white rounded-xl border border-gray-200 shadow-sm">
                <div className="inline-flex items-center space-x-3">
                  <div className="relative">
                    <div className="animate-spin rounded-full h-6 w-6 border-2 border-primary border-t-transparent"></div>
                    <div className="absolute inset-0 rounded-full bg-primary/20 blur-sm"></div>
                  </div>
                  <span className="text-gray-700 font-medium">Processing your CV...</span>
                </div>
              </div>
            ) : (
              <Button 
                onClick={processCV} 
                className="w-full h-12 text-base font-medium shadow-md hover:shadow-lg transition-all"
              >
                <Sparkles className="h-5 w-5 mr-2" />
                Extract Information
              </Button>
            )}
          </div>
        )}

        {/* Error Alert */}
        {error && (
          <Alert variant="destructive" className="border-red-200 bg-red-50 shadow-sm">
            <AlertCircle className="h-5 w-5" />
            <AlertDescription className="text-red-800 font-medium">
              {error}
            </AlertDescription>
          </Alert>
        )}

        {isProcessing && (
          <Alert className="border-blue-200 bg-blue-50 shadow-sm">
            <Sparkles className="h-5 w-5 text-blue-600" />
            <AlertDescription className="text-blue-800">
              Processing your CV and extracting academic information...
            </AlertDescription>
          </Alert>
        )}

        {!isProcessing && !error && (
          <Alert className="border-green-200 bg-green-50 shadow-sm">
            <CheckCircle className="h-5 w-5 text-green-600" />
            <AlertDescription className="text-green-800">
              <strong className="font-semibold">Demo Mode:</strong> This will auto-fill your profile with sample data from a Computer Science student's CV.
            </AlertDescription>
          </Alert>
        )}
      </CardContent>
    </Card>
  );
}