import { Box, Heading, Text, Stack, Button } from '@chakra-ui/react';
import { useNavigate } from 'react-router-dom';

const Home = () => {
  const navigate = useNavigate();

  return (
    <Box p={8} textAlign="center">
      <Heading mb={4}>AI Document Research & Conversion</Heading>
      <Text fontSize="lg" mb={8}>
        Upload, analyze, convert and extract insights from your documents using AI.
      </Text>
      <Stack direction="row" justify="center" spacing={6}>
        <Button colorScheme="teal" onClick={() => navigate('/ai-research')}>
          AI Research
        </Button>
        <Button colorScheme="blue" onClick={() => navigate('/convert')}>
          Convert Document
        </Button>
        <Button colorScheme="purple" onClick={() => navigate('/upload-ocr')}>
          Upload & Extract Text
        </Button>
      </Stack>
    </Box>
  );
};

export default Home;