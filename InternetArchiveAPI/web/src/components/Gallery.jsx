import React from 'react';
import { Grid, Card, CardMedia, CardContent, Typography, Box, Pagination } from '@mui/material';

const Gallery = ({ items, onItemClick, page, totalPages, onPageChange, itemType }) => {
  console.log('Gallery items:', items); // Debug log

  if (!items || items.length === 0) {
    return (
      <Box sx={{ p: 3, textAlign: 'center' }}>
        <Typography variant="h6">No items found</Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Grid container spacing={3}>
        {items.map((item) => (
          <Grid item xs={12} sm={6} md={4} lg={3} key={item.identifier}>
            <Card 
              onClick={() => onItemClick(item)}
              sx={{ 
                cursor: 'pointer',
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                '&:hover': { transform: 'scale(1.02)', transition: 'transform 0.2s' }
              }}
            >
              <CardMedia
                component="img"
                height="200"
                image={item.thumbnail_url || 'https://via.placeholder.com/300x200'}
                alt={item.title}
                sx={{ objectFit: 'cover' }}
              />
              <CardContent sx={{ flexGrow: 1 }}>
                <Typography noWrap variant="subtitle1" gutterBottom>
                  {item.title || 'Untitled'}
                </Typography>
                {item.description && (
                  <Typography 
                    variant="body2" 
                    color="text.secondary"
                    sx={{
                      display: '-webkit-box',
                      WebkitLineClamp: 2,
                      WebkitBoxOrient: 'vertical',
                      overflow: 'hidden',
                      textOverflow: 'ellipsis'
                    }}
                  >
                    {item.description}
                  </Typography>
                )}
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
      
      {totalPages > 1 && (
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
          <Pagination 
            count={totalPages} 
            page={page} 
            onChange={(e, value) => onPageChange(value)}
            color="primary"
          />
        </Box>
      )}
    </Box>
  );
};

export default Gallery; 