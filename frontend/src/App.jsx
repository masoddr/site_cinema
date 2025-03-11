import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import SeancesViewer from './components/SeancesViewer';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/seances" element={<SeancesViewer seances={seances} />} />
      </Routes>
    </Router>
  );
};

export default App; 