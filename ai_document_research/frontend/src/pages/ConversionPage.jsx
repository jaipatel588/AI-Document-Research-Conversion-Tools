import { Box, Heading } from '@chakra-ui/react';
import ConvertUpload from '../features/Conversion/ConvertUpload';

const ConversionPage = () => {
  return (
    <Box p={8}>
      <Heading mb={4}>Document Conversion</Heading>
      <ConvertUpload />
    </Box>
  );
};

export default ConversionPage;