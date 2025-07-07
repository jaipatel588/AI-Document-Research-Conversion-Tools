import { Box, Container, Heading, Divider } from '@chakra-ui/react';
import ResearchUpload from '../features/AIResearch/ResearchUpload';
import SearchQuery from '../features/AIResearch/SearchQuery';
import AISummary from '../features/AIResearch/AISummary';
import { useState } from 'react';

const AIResearchPage = () => {
  const [summary, setSummary] = useState('');
  const [matches, setMatches] = useState([]);

  return (
    <Container maxW="6xl" py={8}>
      <Heading mb={6} fontFamily="Poppins, sans-serif">📚 AI Document Research</Heading>

      <Box mb={10}>
        <ResearchUpload />
      </Box>

      <Divider mb={8} />

      <Box mb={10}>
        <SearchQuery
          onResult={(answer, matchList) => {
            setSummary(answer);
            setMatches(matchList);
          }}
        />
      </Box>

      <AISummary summary={summary} />
    </Container>
  );
};

export default AIResearchPage;