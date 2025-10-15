import os
import json
import logging
import duckdb
import polars as pl
from pathlib import Path
from typing import Dict, List, Any, Optional
from django.conf import settings

logger = logging.getLogger(__name__)


class DatasetService:
    """Service for accessing file-backed university dataset."""
    
    def __init__(self):
        self.base_path = Path(getattr(settings, 'DATASET_BASE_PATH', '/data'))
        self.current_version = self._get_current_version()
        self._connection = None
    
    def _get_current_version(self) -> str:
        """Get the current active dataset version."""
        current_file = self.base_path / 'current'
        
        if current_file.is_file():
            try:
                with open(current_file, 'r') as f:
                    return f.read().strip()
            except Exception as e:
                logger.warning(f"Error reading current version file: {e}")
        
        # Fallback to environment variable
        return getattr(settings, 'DATASET_CURRENT_VERSION', '2025.09')
    
    @property
    def connection(self):
        """Get or create DuckDB connection."""
        if self._connection is None:
            try:
                self._connection = duckdb.connect(":memory:")
                # Configure DuckDB settings
                memory_limit = getattr(settings, 'DUCKDB_MEMORY_LIMIT', '2GB')
                threads = getattr(settings, 'DUCKDB_THREADS', 4)
                
                self._connection.execute(f"SET memory_limit='{memory_limit}'")
                self._connection.execute(f"SET threads={threads}")
                
            except Exception as e:
                logger.error(f"Error creating DuckDB connection: {e}")
                raise
        
        return self._connection
    
    def get_dataset_path(self, filename: str) -> Path:
        """Get path to a dataset file."""
        return self.base_path / 'curated' / self.current_version / filename
    
    def _load_institutions_table(self):
        """Load institutions parquet file into DuckDB."""
        institutions_path = self.get_dataset_path('institutions.parquet')
        
        if not institutions_path.exists():
            raise FileNotFoundError(f"Institutions dataset not found: {institutions_path}")
        
        try:
            self.connection.execute(f"""
                CREATE OR REPLACE TABLE institutions AS 
                SELECT * FROM read_parquet('{institutions_path}')
            """)
            logger.info(f"Loaded institutions table from {institutions_path}")
        except Exception as e:
            logger.error(f"Error loading institutions table: {e}")
            raise
    
    def search_universities(
        self,
        filters: Dict[str, Any] = None,
        limit: int = 20,
        offset: int = 0,
        ordering: str = 'display_name'
    ) -> List[Dict[str, Any]]:
        """
        Search universities with filters.
        
        Args:
            filters: Dictionary of filters to apply
            limit: Maximum number of results
            offset: Offset for pagination
            ordering: Field to order by
            
        Returns:
            List of university dictionaries
        """
        try:
            self._load_institutions_table()
            
            # Build WHERE clause from filters
            where_conditions = []
            params = {}
            
            if filters:
                if 'q' in filters and filters['q']:
                    where_conditions.append("display_name ILIKE ?")
                    params['q'] = f"%{filters['q']}%"
                
                if 'country' in filters and filters['country']:
                    where_conditions.append("country_code = ?")
                    params['country'] = filters['country'].upper()
                
                if 'has_rank' in filters and filters['has_rank']:
                    where_conditions.append("webometrics_rank IS NOT NULL")
            
            where_clause = ""
            if where_conditions:
                where_clause = "WHERE " + " AND ".join(where_conditions)
            
            # Build ORDER BY clause
            valid_orderings = {
                'display_name': 'display_name ASC',
                'country': 'country_code ASC',
                'rank': 'webometrics_rank ASC NULLS LAST',
                'works_count': 'works_count DESC NULLS LAST'
            }
            
            order_clause = valid_orderings.get(ordering, 'display_name ASC')
            
            query = f"""
                SELECT 
                    id,
                    display_name,
                    canonical_name,
                    country_code,
                    homepage_url,
                    webometrics_rank,
                    works_count,
                    cited_by_count,
                    geo_latitude,
                    geo_longitude
                FROM institutions
                {where_clause}
                ORDER BY {order_clause}
                LIMIT ? OFFSET ?
            """
            
            # Add limit and offset parameters
            params['limit'] = limit
            params['offset'] = offset
            
            result = self.connection.execute(query, list(params.values())).fetchall()
            
            # Convert to list of dictionaries
            columns = [desc[0] for desc in self.connection.description]
            universities = []
            
            for row in result:
                university = dict(zip(columns, row))
                # Add computed fields
                university['has_rank'] = university['webometrics_rank'] is not None
                universities.append(university)
            
            return universities
            
        except Exception as e:
            logger.error(f"Error searching universities: {e}")
            raise
    
    def get_university(self, university_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific university by ID.
        
        Args:
            university_id: OpenAlex ID or canonical identifier
            
        Returns:
            University dictionary or None if not found
        """
        try:
            self._load_institutions_table()
            
            query = """
                SELECT *
                FROM institutions
                WHERE id = ?
                LIMIT 1
            """
            
            result = self.connection.execute(query, [university_id]).fetchone()
            
            if result:
                columns = [desc[0] for desc in self.connection.description]
                university = dict(zip(columns, result))
                university['has_rank'] = university['webometrics_rank'] is not None
                return university
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting university {university_id}: {e}")
            raise
    
    def recommend(
        self,
        filters: Dict[str, Any] = None,
        weights: Dict[str, float] = None,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Generate university recommendations based on filters and weights.
        
        Args:
            filters: Filters to apply
            weights: Weights for different scoring factors
            limit: Maximum number of recommendations
            
        Returns:
            List of recommendation dictionaries with scores
        """
        try:
            self._load_institutions_table()
            
            # Default weights
            default_weights = {
                'academics': 0.3,
                'interests': 0.2,
                'career': 0.2,
                'location': 0.1,
                'budget': 0.1,
                'ranking': 0.05,
                'research_activity': 0.05
            }
            
            if weights:
                default_weights.update(weights)
            
            # Build scoring query
            score_components = []
            
            # Research activity score (normalized works_count)
            if default_weights['research_activity'] > 0:
                score_components.append(f"""
                    {default_weights['research_activity']} * 
                    COALESCE(
                        LEAST(works_count / 100000.0, 1.0), 
                        0.0
                    )
                """)
            
            # Ranking score (inverse normalized webometrics_rank)
            if default_weights['ranking'] > 0:
                score_components.append(f"""
                    {default_weights['ranking']} * 
                    COALESCE(
                        1.0 - (webometrics_rank / 10000.0),
                        0.0
                    )
                """)
            
            # Default academic score (placeholder)
            if default_weights['academics'] > 0:
                score_components.append(f"{default_weights['academics']} * 0.7")
            
            # Base location score (can be enhanced with user preferences)
            if default_weights['location'] > 0:
                score_components.append(f"{default_weights['location']} * 0.5")
            
            if not score_components:
                score_components = ["0.5"]  # Default score
            
            score_expression = " + ".join(score_components)
            
            # Build WHERE clause from filters
            where_conditions = []
            params = {}
            
            if filters:
                if 'country' in filters and filters['country']:
                    where_conditions.append("country_code = ?")
                    params['country'] = filters['country'].upper()
                
                if 'min_rank' in filters and filters['min_rank']:
                    where_conditions.append("webometrics_rank <= ?")
                    params['min_rank'] = filters['min_rank']
                
                if 'has_research' in filters and filters['has_research']:
                    where_conditions.append("works_count > 1000")
            
            where_clause = ""
            if where_conditions:
                where_clause = "WHERE " + " AND ".join(where_conditions)
            
            query = f"""
                SELECT 
                    id,
                    display_name,
                    canonical_name,
                    country_code,
                    homepage_url,
                    webometrics_rank,
                    works_count,
                    cited_by_count,
                    ({score_expression}) as score
                FROM institutions
                {where_clause}
                ORDER BY score DESC
                LIMIT ?
            """
            
            params['limit'] = limit
            result = self.connection.execute(query, list(params.values())).fetchall()
            
            # Convert to list of dictionaries
            columns = [desc[0] for desc in self.connection.description]
            recommendations = []
            
            for row in result:
                rec = dict(zip(columns, row))
                # Normalize score to [0, 1] range
                rec['score'] = min(1.0, max(0.0, rec['score']))
                rec['name'] = rec['display_name']  # Alias for compatibility
                recommendations.append(rec)
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            raise
    
    def get_matching_universities(
        self,
        filters: Dict[str, Any] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Get universities matching basic filters (no complex scoring).
        LLM will handle the intelligent ranking.
        
        Args:
            filters: Basic filters to apply
            limit: Maximum number of universities to return
            
        Returns:
            List of university dictionaries
        """
        try:
            self._load_institutions_table()
            
            # Build basic filter query
            where_conditions = []
            
            if filters:
                # Country filter
                if 'countries' in filters and filters['countries']:
                    country_list = "', '".join(filters['countries'])
                    where_conditions.append(f"country_code IN ('{country_list}')")
                
                # Search term filter
                if 'search' in filters and filters['search']:
                    search_term = filters['search'].replace("'", "''")  # Escape quotes
                    where_conditions.append(f"""
                        (LOWER(display_name) LIKE LOWER('%{search_term}%') 
                         OR LOWER(canonical_name) LIKE LOWER('%{search_term}%'))
                    """)
                
                # Minimum ranking filter
                if 'max_rank' in filters and filters['max_rank']:
                    where_conditions.append(f"webometrics_rank <= {filters['max_rank']}")
            
            # Build complete query
            where_clause = "WHERE " + " AND ".join(where_conditions) if where_conditions else ""
            
            query = f"""
                SELECT 
                    id,
                    display_name,
                    canonical_name,
                    country_code,
                    homepage_url,
                    webometrics_rank,
                    works_count,
                    cited_by_count,
                    geo_latitude,
                    geo_longitude
                FROM institutions 
                {where_clause}
                ORDER BY 
                    COALESCE(webometrics_rank, 99999),
                    works_count DESC
                LIMIT {limit}
            """
            
            # Execute query and return results
            results = self.conn.execute(query).fetchall()
            
            universities = []
            for row in results:
                universities.append({
                    'id': row[0],
                    'display_name': row[1],
                    'canonical_name': row[2],
                    'country_code': row[3],
                    'homepage_url': row[4],
                    'webometrics_rank': row[5],
                    'works_count': row[6],
                    'cited_by_count': row[7],
                    'geo_latitude': row[8],
                    'geo_longitude': row[9],
                    'score': 0.5  # Placeholder - LLM will provide real scoring
                })
            
            logger.info(f"Retrieved {len(universities)} matching universities")
            return universities
            
        except Exception as e:
            logger.error(f"Error getting matching universities: {e}")
            return []
    
    def validate_dataset(self) -> Dict[str, Any]:
        """
        Validate the current dataset.
        
        Returns:
            Dictionary with validation results
        """
        try:
            institutions_path = self.get_dataset_path('institutions.parquet')
            
            if not institutions_path.exists():
                return {
                    'valid': False,
                    'error': f"Institutions dataset not found: {institutions_path}",
                    'stats': {}
                }
            
            # Load and validate
            self._load_institutions_table()
            
            # Get basic stats
            stats_query = """
                SELECT 
                    COUNT(*) as total_institutions,
                    COUNT(DISTINCT country_code) as countries,
                    COUNT(webometrics_rank) as ranked_institutions,
                    SUM(works_count) as total_works,
                    MIN(webometrics_rank) as best_rank,
                    MAX(webometrics_rank) as worst_rank
                FROM institutions
            """
            
            result = self.connection.execute(stats_query).fetchone()
            columns = [desc[0] for desc in self.connection.description]
            stats = dict(zip(columns, result))
            
            return {
                'valid': True,
                'version': self.current_version,
                'dataset_path': str(institutions_path),
                'stats': stats
            }
            
        except Exception as e:
            logger.error(f"Error validating dataset: {e}")
            return {
                'valid': False,
                'error': str(e),
                'stats': {}
            }
    
    def close(self):
        """Close DuckDB connection."""
        if self._connection:
            self._connection.close()
            self._connection = None
