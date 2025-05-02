import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { Container, Typography, Box, CircularProgress, Button, TextField, FormControl, InputLabel, Select, MenuItem, Grid } from '@mui/material';
import Gallery from '../components/Gallery';
import { getCollections } from '../services/api';
import HomeIcon from '@mui/icons-material/Home';
import VideoLibrary from '@mui/icons-material/VideoLibrary';

const Home = () => {
  const [collections, setCollections] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    collection: '*',
    sort: 'stars desc'
  });
  const navigate = useNavigate();

  // Memoize the loading function to avoid recreation
  const loadCollections = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      setCollections([]); // Clear collections to avoid flash of old content
      
      console.log(`Fetching collections: page=${page}, collection=${filters.collection}, sort=${filters.sort}`);
      const data = await getCollections(page, filters.collection, filters.sort);
      
      if (data && data.docs) {
        setCollections(data.docs);
        setTotalPages(Math.ceil(data.numFound / 12));
        if (data.docs.length === 0) {
          setError('No items found for this search');
        }
      } else {
        setError('Invalid data format');
      }
    } catch (error) {
      console.error('Error loading collections:', error);
      setError('Error loading collections. Please try again later.');
    } finally {
      setLoading(false);
    }
  }, [page, filters.collection, filters.sort]);

  // Single useEffect with correct dependencies
  useEffect(() => {
    loadCollections();
  }, [loadCollections]);
  
  const handleCollectionClick = (collection) => {
    navigate(`/collection/${collection.identifier}`);
  };

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    // When filters change, reset to page 1 and update the filter
    setPage(1);
    setFilters(prev => ({ ...prev, [name]: value }));
  };

  const handlePageChange = (newPage) => {
    setPage(newPage);
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>        
        <Button
          startIcon={<HomeIcon />}
          onClick={() => navigate('/')}
          sx={{ mr: 2, mb: 3 }}
        >
          Explore All Collections
        </Button>

        <Button
          startIcon={<VideoLibrary />}
          onClick={() => navigate('/collection/TV-FOXNEWSW')}
          sx={{ mr: 2, mb: 3 }}
        >
          Video: Fox News West
        </Button>

        <Grid container spacing={2} sx={{ mb: 3 }}>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Collection"
              name="collection"
              value={filters.collection}
              onChange={handleFilterChange}
              size="small"
              helperText="Use * for all collections"
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <FormControl fullWidth size="small">
              <InputLabel id="sort-label">Sort by</InputLabel>
              <Select
                labelId="sort-label"
                id="sort"
                name="sort"
                value={filters.sort}
                label="Sort by"
                onChange={handleFilterChange}
              >
                <MenuItem value="stars desc">Stars Desc</MenuItem>
                <MenuItem value="stars asc">Starts Asc</MenuItem>
                <MenuItem value="num_reviews desc">Num Reviews Desc</MenuItem>
                <MenuItem value="num_reviews asc">Num Reviews Asc</MenuItem>
                <MenuItem value="files_count desc">Files Count Desc</MenuItem>
                <MenuItem value="files_count asc">Files Count Asc</MenuItem>
              </Select>
            </FormControl>
          </Grid>
        </Grid>

        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
            <CircularProgress />
          </Box>
        ) : error ? (
          <Box sx={{ textAlign: 'center', my: 4 }}>
            <Typography color="error">{error}</Typography>
          </Box>
        ) : (
          <Gallery
            items={collections}
            onItemClick={handleCollectionClick}
            page={page}
            totalPages={totalPages}
            onPageChange={handlePageChange}
            itemType="collection"
          />
        )}
      </Box>
    </Container>
  );
};

export default Home; 