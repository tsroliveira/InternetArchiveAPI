import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Container, Typography, Box, Button, CircularProgress, FormControl, InputLabel, Select, MenuItem, Grid } from '@mui/material';
import HomeIcon from '@mui/icons-material/Home';
import Gallery from '../components/Gallery';
import VideoModal from '../components/VideoModal';
import { getCollectionVideos, getVideoDetails } from '../services/api';

const Collection = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [videos, setVideos] = useState([]);
  const [selectedVideo, setSelectedVideo] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [collectionTitle, setCollectionTitle] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(1);
  const [filters, setFilters] = useState({
    sort: 'date desc'
  });

  // Memoize the loading function to avoid recreation
  const loadCollectionVideos = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      setVideos([]); // Clear videos to avoid flash of old content
      
      console.log(`Loading videos for collection: ${id}, page=${page}, sort=${filters.sort}`);
      const data = await getCollectionVideos(id, page, filters.sort);
      console.log('Data received:', data);
      
      if (data) {
        if (data.films && data.films.length > 0) {
          setVideos(data.films);
          setCollectionTitle(data.title || 'Collection');
        } else {
          // If there are no films, try to use docs
          if (data.docs && data.docs.length > 0) {
            setVideos(data.docs);
            setCollectionTitle(data.title || 'Collection');
          } else {
            setError('No videos found in this collection');
          }
        }
      } else {
        setError('Invalid data format');
      }
    } catch (error) {
      console.error('Error loading videos:', error);
      setError('Error loading videos. Please try again later.');
    } finally {
      setLoading(false);
    }
  }, [id, page, filters.sort]);

  // Single useEffect with correct dependencies
  useEffect(() => {
    if (id) {
      loadCollectionVideos();
    }
  }, [loadCollectionVideos, id]);

  const handleVideoClick = async (video) => {
    try {
      console.log('Clicked on video:', video.identifier); // Debug log
      const videoDetails = await getVideoDetails(video.identifier);
      setSelectedVideo(videoDetails);
      setIsModalOpen(true);
    } catch (error) {
      console.error('Error loading video details:', error);
    }
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
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <Button
            startIcon={<HomeIcon />}
            onClick={() => navigate('/')}
            sx={{ mr: 2 }}
          >
            Home
          </Button>
          <Typography variant="h4" component="h1">
            {collectionTitle}
          </Typography>
        </Box>

        <Grid container spacing={2} sx={{ mb: 3 }}>
          <Grid item xs={12} sm={6}>
            <FormControl fullWidth size="small" disabled>
              <InputLabel id="collection-label">Collection</InputLabel>
              <Select
                labelId="collection-label"
                id="collection"
                name="collection"
                value={id}
                label="Collection"
              >
                <MenuItem value={id}>{id}</MenuItem>
              </Select>
            </FormControl>
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
                <MenuItem value="date desc">Date (Newest)</MenuItem>
                <MenuItem value="date asc">Date (Oldest)</MenuItem>
                <MenuItem value="title asc">Title (A-Z)</MenuItem>
                <MenuItem value="title desc">Title (Z-A)</MenuItem>
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
            items={videos}
            onItemClick={handleVideoClick}
            page={page}
            totalPages={1}
            onPageChange={handlePageChange}
            itemType="video"
          />
        )}

        <VideoModal
          open={isModalOpen}
          onClose={() => setIsModalOpen(false)}
          video={selectedVideo}
        />
      </Box>
    </Container>
  );
};

export default Collection; 