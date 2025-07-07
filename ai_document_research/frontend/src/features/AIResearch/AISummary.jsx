import { Box, Heading, Text } from '@chakra-ui/react';

const AISummary = ({ summary = "Run a query to get AI-generated summary." }) => {
  return (
    <Box mt={4}>
      <Heading size="md" mb={2}>AI Summary</Heading>
      <Text whiteSpace="pre-wrap">{summary}</Text>
    </Box>
  );
};

export default AISummary;