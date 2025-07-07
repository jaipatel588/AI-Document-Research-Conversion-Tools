import { Box, Flex, Link, Text } from '@chakra-ui/react';
import { NavLink } from 'react-router-dom';

const Navbar = () => {
  return (
    <Box bg="teal.500" p={4} color="white">
      <Flex justify="space-between" align="center">
        <Text fontSize="xl" fontWeight="bold">AI Doc Tool</Text>
        <Flex gap={6}>
          <Link as={NavLink} to="/">Home</Link>
          <Link as={NavLink} to="/ai-research">AI Research</Link>
          <Link as={NavLink} to="/convert">Conversion</Link>
          <Link as={NavLink} to="/upload-ocr">OCR Upload</Link>
        </Flex>
      </Flex>
    </Box>
  );
};

export default Navbar;