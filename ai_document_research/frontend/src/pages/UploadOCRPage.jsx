import { Box, Heading } from '@chakra-ui/react';
import OCRUpload from '../features/OCR/OCRUpload';

const UploadOCRPage = () => {
  return (
    <Box p={8}>
      <Heading mb={4}>Upload Document for OCR</Heading>
      <OCRUpload />
    </Box>
  );
};

export default UploadOCRPage;