import { Button } from '../src/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../src/components/ui/card';
import { Badge } from '../src/components/ui/badge';
import { MapPin, DollarSign, TrendingUp, Users, Star, Heart } from 'lucide-react';
import ImageWithFallback from './ImageWithFallback';
import { useState } from 'react';

export default function UniversityCard({ university, onViewDetails, onCompare, isInComparison }) {
  const [isFavorited, setIsFavorited] = useState(false);

  return (
    <Card className="group hover:shadow-lg transition-all duration-300 overflow-hidden">
      <div className="relative">
        <ImageWithFallback
          src={university.image}
          alt={university.name}
          className="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300"
        />
        <div className="absolute top-4 left-4">
          <Badge variant="secondary" className="bg-white/90 text-gray-800">
            #{university.ranking} Globally
          </Badge>
        </div>
        <div className="absolute top-4 right-4 flex gap-2">
          <Button
            size="sm"
            variant="secondary"
            className="bg-white/90 hover:bg-white p-2"
            onClick={(e) => {
              e.stopPropagation();
              setIsFavorited(!isFavorited);
            }}
          >
            <Heart className={`h-4 w-4 ${isFavorited ? 'fill-red-500 text-red-500' : 'text-gray-600'}`} />
          </Button>
        </div>
      </div>

      <CardHeader className="pb-3">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <CardTitle className="text-xl group-hover:text-primary transition-colors line-clamp-1">
              {university.name}
            </CardTitle>
            <CardDescription className="flex items-center mt-1">
              <MapPin className="h-4 w-4 mr-1" />
              {university.location}, {university.country}
            </CardDescription>
          </div>
        </div>
      </CardHeader>

      <CardContent className="space-y-4">
        {/* Key Stats */}
        <div className="grid grid-cols-2 gap-4">
          <div className="flex items-center space-x-2">
            <DollarSign className="h-4 w-4 text-green-600" />
            <div>
              <div className="text-sm text-gray-600">Tuition</div>
              <div className="font-semibold">${university.tuitionFee.toLocaleString()}</div>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <TrendingUp className="h-4 w-4 text-blue-600" />
            <div>
              <div className="text-sm text-gray-600">Acceptance</div>
              <div className="font-semibold">{university.acceptanceRate}%</div>
            </div>
          </div>
        </div>

        {/* Requirements */}
        <div className="space-y-2">
          <div className="text-sm font-medium text-gray-700">Requirements</div>
          <div className="flex flex-wrap gap-2">
            <Badge variant="outline" className="text-xs">
              GPA {university.requirements.gpa}+
            </Badge>
            <Badge variant="outline" className="text-xs">
              IELTS {university.requirements.ielts}+
            </Badge>
            <Badge variant="outline" className="text-xs">
              TOEFL {university.requirements.toefl}+
            </Badge>
          </div>
        </div>

        {/* Top Programs */}
        <div className="space-y-2">
          <div className="text-sm font-medium text-gray-700">Top Programs</div>
          <div className="flex flex-wrap gap-1">
            {university.programs.slice(0, 3).map((program) => (
              <Badge key={program} variant="secondary" className="text-xs">
                {program}
              </Badge>
            ))}
            {university.programs.length > 3 && (
              <Badge variant="outline" className="text-xs">
                +{university.programs.length - 3} more
              </Badge>
            )}
          </div>
        </div>

        {/* Features */}
        <div className="space-y-2">
          <div className="text-sm font-medium text-gray-700">Key Features</div>
          <div className="flex flex-wrap gap-1">
            {university.features.slice(0, 2).map((feature) => (
              <Badge key={feature} variant="outline" className="text-xs">
                {feature}
              </Badge>
            ))}
          </div>
        </div>

        {/* Scholarships */}
        {university.scholarships && (
          <div className="flex items-center space-x-2 text-green-600">
            <Star className="h-4 w-4" />
            <span className="text-sm font-medium">Scholarships Available</span>
          </div>
        )}

        {/* Actions */}
        <div className="flex gap-2 pt-2">
          <Button 
            className="flex-1" 
            onClick={() => onViewDetails(university)}
          >
            View Details
          </Button>
          {onCompare && (
            <Button 
              variant="outline" 
              onClick={() => onCompare(university)}
              disabled={isInComparison}
            >
              {isInComparison ? 'Added' : 'Compare'}
            </Button>
          )}
        </div>
      </CardContent>
    </Card>
  );
}