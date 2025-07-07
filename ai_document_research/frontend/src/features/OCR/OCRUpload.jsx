import { Box, Button, Textarea, VStack, Text } from '@chakra-ui/react';
import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import toast from 'react-hot-toast';

const OCRUpload = () => {
  const [file, setFile] = useState(null);
  const [ocrText, setOcrText] = useState('');

  const onDrop = useCallback((acceptedFiles) => {
    setFile(acceptedFiles[0]);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    multiple: false
  });

  const handleOCR = async () => {
    if (!file) return toast.error('Please upload a file');
    const formData = new FormData();
    formData.append('file', file);
    try {
      const res = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/ocr`, formData);
      setOcrText(res.data.text);
      toast.success('OCR extraction complete');
    } catch (err) {
      toast.error('OCR extraction failed');
    }
  };

  return (
    <Box my={4} p={4} borderWidth={1} borderRadius="lg">
      <VStack spacing={4}>
        <Box
          {...getRootProps()}
          border="2px dashed purple"
          borderRadius="md"
          p={6}
          w="100%"
          textAlign="center"
          bg={isDragActive ? 'purple.100' : 'gray.50'}
          cursor="pointer"
        >
          <input {...getInputProps()} />
          {isDragActive ? (
            <Text>Drop the image or PDF here...</Text>
          ) : (
            <Text>Drag & drop image or PDF for OCR, or click to select</Text>
          )}
        </Box>
        <Button colorScheme="purple" onClick={handleOCR}>Extract Text</Button>
        <Textarea value={ocrText} placeholder="Extracted text will appear here..." rows={10} readOnly />
      </VStack>
    </Box>
  );
};

export default OCRUpload;