import {
  Box,
  Input,
  Button,
  VStack,
  Textarea,
  Text,
  List,
  ListItem,
  Divider,
  Badge,
} from "@chakra-ui/react";
import { useState } from "react";
import axios from "axios";
import toast from "react-hot-toast";

const SearchQuery = ({ onResult }) => {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState("");
  const [matches, setMatches] = useState([]);

  const handleSearch = async () => {
    if (!query.trim()) return toast.error("❌ Please enter a valid query.");

    try {
      const res = await axios.post(
        `${import.meta.env.VITE_API_BASE_URL}/api/ai/search-body`,
        {
          query,
          top_k: 5,
        }
      );

      const { answer, matches } = res.data || {};

      if (!answer) {
        toast.error("⚠️ No results from AI.");
        return;
      }

      setResult(answer);
      setMatches(matches);

      if (onResult) onResult(answer, matches); // 🔁 Inform parent if needed

      toast.success("✅ AI Search Completed");
    } catch (err) {
      console.error("❌ Search Error:", err);
      toast.error("❌ Search failed. See console for details.");
    }
  };

  return (
    <Box
      my={6}
      p={6}
      borderWidth={1}
      borderRadius="xl"
      boxShadow="md"
      bg="white"
      fontFamily="Poppins, sans-serif"
    >
      <VStack spacing={4} align="stretch">
        <Text fontSize="xl" fontWeight="semibold">
          🔍 Ask a Question About Your Documents
        </Text>

        <Input
          placeholder="Type your research query here..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          size="md"
          borderRadius="md"
        />

        <Button colorScheme="blue" onClick={handleSearch}>
          Search
        </Button>

        <Button
          variant="outline"
          colorScheme="green"
          onClick={() => {
            setQuery("Summarize this document");
            handleSearch();
          }}
        >
          🧠 Summarize Document
        </Button>

        <Textarea
          value={result}
          placeholder="🧠 AI Answer will appear here..."
          rows={6}
          readOnly
          borderRadius="md"
        />

        {matches.length > 0 && (
          <Box mt={6}>
            <Text fontWeight="bold" fontSize="lg" mb={2}>
              📚 Matched Documents:
            </Text>
            <List spacing={4}>
              {matches.map((doc, i) => (
                <ListItem
                  key={i}
                  border="1px solid #E2E8F0"
                  borderRadius="md"
                  p={3}
                  bg="gray.50"
                >
                  <Text fontWeight="medium">📄 {doc.metadata}</Text>
                  <Text fontSize="sm" color="gray.600" mt={1}>
                    {doc.text.slice(0, 200)}...
                  </Text>
                  <Badge mt={2} colorScheme="purple">
                    Rank #{doc.rank} | Score: {doc.score.toFixed(2)}
                  </Badge>
                </ListItem>
              ))}
            </List>
            <Divider my={4} />
          </Box>
        )}
      </VStack>
    </Box>
  );
};

export default SearchQuery;