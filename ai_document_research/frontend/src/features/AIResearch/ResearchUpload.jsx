import { useState, useCallback } from "react";
import {
  Box,
  Button,
  Text,
  useToast,
  List,
  ListItem,
  Heading,
} from "@chakra-ui/react";
import { useDropzone } from "react-dropzone";

const API_BASE = import.meta.env.VITE_API_BASE_URL;

const ResearchUpload = () => {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const toast = useToast();

  // 🔁 Drag-n-Drop handler
  const onDrop = useCallback((acceptedFiles) => {
    setSelectedFiles((prev) => [...prev, ...acceptedFiles]);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "application/pdf": [".pdf"],
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [".docx"],
      "text/plain": [".txt"],
    },
    multiple: true,
  });

  // 🧠 Upload to backend
  const handleUpload = async () => {
    if (selectedFiles.length === 0) {
      toast({
        title: "No files selected.",
        status: "warning",
        duration: 3000,
        isClosable: true,
      });
      return;
    }

    const formData = new FormData();
    selectedFiles.forEach((file) => formData.append("files", file));
    selectedFiles.forEach((file, idx) =>
      formData.append("metadata", file.name || `Document ${idx + 1}`)
    );

    try {
      const response = await fetch(`${API_BASE}/api/ai/index-files`, {
        method: "POST",
        body: formData,
      });

      const result = await response.json();

      if (response.ok) {
        toast({
          title: "✅ Files uploaded!",
          description: result.message || "Upload completed successfully.",
          status: "success",
          duration: 3000,
          isClosable: true,
        });
        setSelectedFiles([]); // reset
      } else {
        toast({
          title: "❌ Upload failed",
          description: result.detail || "Backend error.",
          status: "error",
          duration: 3000,
          isClosable: true,
        });
      }
    } catch (err) {
      toast({
        title: "❌ Upload error",
        description: err.message || "Unexpected error occurred.",
        status: "error",
        duration: 3000,
        isClosable: true,
      });
    }
  };

  return (
    <Box
      borderWidth={1}
      borderRadius="xl"
      boxShadow="lg"
      p={6}
      bg="white"
      fontFamily="Poppins, sans-serif"
    >
      <Heading size="md" mb={4}>
        📤 Upload Documents for AI Research
      </Heading>

      <Box
        {...getRootProps()}
        border="2px dashed"
        borderColor={isDragActive ? "blue.400" : "gray.300"}
        borderRadius="md"
        p={6}
        textAlign="center"
        cursor="pointer"
        bg={isDragActive ? "blue.50" : "gray.50"}
      >
        <input {...getInputProps()} />
        {isDragActive ? (
          <Text color="blue.500">Drop the files here...</Text>
        ) : (
          <Text>Drag and drop files here, or click to select (.pdf, .docx, .txt)</Text>
        )}
      </Box>

      {selectedFiles.length > 0 && (
        <Box mt={4}>
          <Text fontWeight="medium" mb={2}>
            Selected Files ({selectedFiles.length}):
          </Text>
          <List spacing={1} fontSize="sm">
            {selectedFiles.map((file, index) => (
              <ListItem key={index}>📄 {file.name}</ListItem>
            ))}
          </List>
        </Box>
      )}

      <Button
        onClick={handleUpload}
        mt={6}
        colorScheme="blue"
        isDisabled={selectedFiles.length === 0}
      >
        Upload to AI Index
      </Button>
    </Box>
  );
};

export default ResearchUpload;