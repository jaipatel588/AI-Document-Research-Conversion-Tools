import { Box, Text } from '@chakra-ui/react';

const Footer = () => {
  return (
    <Box bg="gray.200" textAlign="center" py={4} mt={8}>
      <Text>&copy; {new Date().getFullYear()} AI Document Research & Conversion Tool</Text>
    </Box>
  );
};

export default Footer;