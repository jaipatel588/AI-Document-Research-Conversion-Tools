import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import AIResearchPage from './pages/AIResearchPage';
import ConversionPage from './pages/ConversionPage';
import UploadOCRPage from './pages/UploadOCRPage';
import Navbar from './components/Navbar';
import Footer from './components/Footer';

const App = () => {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/ai-research" element={<AIResearchPage />} />
        <Route path="/convert" element={<ConversionPage />} />
        <Route path="/upload-ocr" element={<UploadOCRPage />} />
      </Routes>
      <Footer />
    </>
  );
};

export default App;