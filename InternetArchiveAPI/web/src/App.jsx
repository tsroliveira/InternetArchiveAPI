import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme, CssBaseline } from '@mui/material';
import Home from './pages/Home';
import Collection from './pages/Collection';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#00bcd4',
    },
    background: {
      default: '#121212',
      paper: '#1e1e1e',
    },
  },
});

const App = () => {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/collection/:id" element={<Collection />} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
};

export default App; 