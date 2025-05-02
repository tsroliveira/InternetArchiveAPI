import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
});

export const getCollections = async (page = 1, collection = '*', sort = 'files_count desc') => {
  try {
    const response = await api.get('/explore', {
      params: {
        collection,
        page,
        rows: 12,
        sort
      }
    });
    return response.data;
  } catch (error) {
    console.error('API call error:', error);
    throw error;
  }
};

export const getCollectionVideos = async (identifier, page = 1, sort = 'date desc') => {
  try {
    console.log('Buscando vídeos da coleção:', identifier); // Debug log
    const response = await api.get(`/collections/${identifier}`, {
      params: {
        film_rows: 5,
        page,
        sort
      }
    });
    console.log('Resposta da API:', response.data); // Debug log
    return response.data;
  } catch (error) {
    console.error('Error fetching collection videos:', error);
    throw error;
  }
};

export const getVideoDetails = async (identifier) => {
  try {
    const response = await api.get(`/videos/${identifier}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching video details:', error);
    throw error;
  }
};

export default api; 