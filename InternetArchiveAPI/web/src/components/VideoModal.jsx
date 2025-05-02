import React, { useState } from 'react';
import {
  Dialog,
  DialogContent,
  DialogTitle,
  Button,
  Typography,
  Box,
  IconButton,
  Chip
} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';

const VideoModal = ({ open, onClose, video }) => {
  const [isPlaying, setIsPlaying] = useState(false);

  if (!video) return null;

  const getVideoUrl = () => {
    if (video.playback_urls && video.playback_urls.length > 0) {
      return video.playback_urls[0].url;
    }
    return null;
  };

  return (
    <Dialog
      open={open}
      onClose={onClose}
      maxWidth="md"
      fullWidth
    >
      <DialogTitle>
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Typography variant="h6">{video.title}</Typography>
          <IconButton onClick={onClose}>
            <CloseIcon />
          </IconButton>
        </Box>
      </DialogTitle>
      <DialogContent>
        <Box sx={{ mb: 2 }}>
          {isPlaying ? (
            <Box sx={{ position: 'relative', paddingTop: '56.25%' }}>
              <iframe
                style={{
                  position: 'absolute',
                  top: 0,
                  left: 0,
                  width: '100%',
                  height: '100%',
                }}
                src={getVideoUrl()}
                title={video.title}
                frameBorder="0"
                allowFullScreen
              />
            </Box>
          ) : (
            <Box
              component="img"
              src={video.thumbnail_url}
              alt={video.title}
              sx={{ width: '100%', maxHeight: 400, objectFit: 'cover' }}
            />
          )}
        </Box>

        {!isPlaying && getVideoUrl() && (
          <Box sx={{ mb: 2 }}>
            <Button
              variant="contained"
              color="primary"
              onClick={() => setIsPlaying(true)}
            >
              Start watching
            </Button>
          </Box>
        )}

        {video.description && (
          <Typography variant="body1" sx={{ mb: 1 }}>
            {video.description}
          </Typography>
        )}

        {video.date && (
          <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
            Data: {new Date(video.date).toLocaleDateString()}
          </Typography>
        )}

        {video.subject && video.subject.length > 0 && (
          <Box sx={{ mt: 2 }}>
            <Typography variant="subtitle2" gutterBottom>
              Tags:
            </Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
              {video.subject.map((tag, index) => (
                <Chip key={index} label={tag} size="small" />
              ))}
            </Box>
          </Box>
        )}
      </DialogContent>
    </Dialog>
  );
};

export default VideoModal; 