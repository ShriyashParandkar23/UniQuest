import { useState, useRef } from 'react';
import { Button } from '../src/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../src/components/ui/card';
import { Alert, AlertDescription } from '../src/components/ui/alert';
import { Upload, FileText, CheckCircle, AlertCircle, X, Sparkles } from 'lucide-react';

export function CVUploadSimple({ onDataExtracted, onClose }) {
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
    <Card className="w-full max-w-2xl">
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

      <CardContent className="space-y-6">
        {/* File Upload Area */}
        {!file && (
          <div
            className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-primary transition-colors cursor-pointer"
            onClick={() => fileInputRef.current?.click()}
          >
            <Upload className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Drop your CV here or click to browse
            </h3>
            <p className="text-sm text-gray-500 mb-4">
              Supports PDF, DOC, and DOCX files up to 10MB
            </p>
            <Button variant="outline">
              Choose File
            </Button>
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
            <div className="flex items-center justify-between p-4 border rounded-lg">
              <div className="flex items-center space-x-3">
                <FileText className="h-8 w-8 text-primary" />
                <div>
                  <p className="font-medium">{file.name}</p>
                  <p className="text-sm text-gray-500">
                    {(file.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                </div>
              </div>
              <Button variant="ghost" size="sm" onClick={removeFile}>
                <X className="h-4 w-4" />
              </Button>
            </div>

            {isProcessing ? (
              <div className="text-center py-4">
                <div className="inline-flex items-center space-x-2">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-primary"></div>
                  <span>Processing your CV...</span>
                </div>
              </div>
            ) : (
              <Button onClick={processCV} className="w-full">
                <Sparkles className="h-4 w-4 mr-2" />
                Extract Information
              </Button>
            )}
          </div>
        )}

        {/* Error Alert */}
        {error && (
          <Alert variant="destructive">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {isProcessing && (
          <Alert>
            <Sparkles className="h-4 w-4" />
            <AlertDescription>
              Processing your CV and extracting academic information...
            </AlertDescription>
          </Alert>
        )}

        {!isProcessing && (
          <Alert>
            <CheckCircle className="h-4 w-4" />
            <AlertDescription>
              <strong>Demo Mode:</strong> This will auto-fill your profile with sample data from a Computer Science student's CV.
            </AlertDescription>
          </Alert>
        )}
      </CardContent>
    </Card>
  );
}