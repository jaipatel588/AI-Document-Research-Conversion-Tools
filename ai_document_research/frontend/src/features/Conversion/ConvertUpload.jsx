import {
  Box,
  Button,
  VStack,
  Text,
  Select,
  Progress,
  Tag,
  Icon,
  useToast
} from '@chakra-ui/react';
import { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { CheckCircleIcon } from '@chakra-ui/icons';
import axios from 'axios';

const formatOptions = {
  jpg: ['pdf', 'txt'],
  jpeg: ['pdf', 'txt'],
  png: ['pdf', 'txt'],
  pdf: ['jpg', 'txt', 'docx'],
  docx: ['pdf'],
  txt: ['pdf']
};

const ConvertUpload = () => {
  const [file, setFile] = useState(null);
  const [availableFormats, setAvailableFormats] = useState([]);
  const [targetFormat, setTargetFormat] = useState('');
  const [progress, setProgress] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [convertedFileUrl, setConvertedFileUrl] = useState('');
  const toast = useToast();

  const onDrop = (acceptedFiles) => {
    const uploaded = acceptedFiles[0];
    const ext = uploaded.name.split('.').pop().toLowerCase();
    const formats = formatOptions[ext];

    if (!formats) {
      toast({ title: 'Unsupported file type', status: 'error', isClosable: true });
      return;
    }

    setFile(uploaded);
    setAvailableFormats(formats);
    setTargetFormat('');
    setConvertedFileUrl('');
  };

  const { getRootProps, getInputProps } = useDropzone({ onDrop });

  const handleConvert = async () => {
    if (!file || !targetFormat) {
      toast({ title: 'Select file and target format', status: 'warning', isClosable: true });
      return;
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('target_format', targetFormat);

    setIsLoading(true);
    setProgress(10);

    try {
      const res = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/api/convert/convert`, formData, {
        responseType: 'blob',
        onDownloadProgress: (progressEvent) => {
          const percent = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          setProgress(percent);
        }
      });

      const blob = new Blob([res.data]);
      const url = window.URL.createObjectURL(blob);
      setConvertedFileUrl(url);
      toast({ title: 'Conversion Successful ✅', status: 'success', isClosable: true });
    } catch (err) {
      toast({ title: 'Conversion Failed ❌', status: 'error', isClosable: true });
    } finally {
      setIsLoading(false);
      setProgress(100);
    }
  };

  const handleReset = () => {
    setFile(null);
    setAvailableFormats([]);
    setTargetFormat('');
    setConvertedFileUrl('');
    setProgress(0);
  };

  return (
    <Box my={4} p={4} borderWidth={1} borderRadius="lg" fontFamily="'Poppins', sans-serif">
      <VStack spacing={4}>
        <Text fontSize="xl" fontWeight="bold">Document Conversion</Text>

        {convertedFileUrl ? (
          <Box my={6} p={6} borderWidth={1} borderRadius="lg" boxShadow="md">
            <VStack spacing={4}>
              <Icon as={CheckCircleIcon} w={10} h={10} color="green.500" />
              <Text fontSize="xl" fontWeight="bold">Conversion Complete 🎉</Text>
              <Text>
                File: <strong>{file?.name?.split('.')[0] || `converted_file.${targetFormat}`}</strong>
              </Text>
              {targetFormat && (
                <Tag colorScheme="blue" fontSize="md">
                  Converted to: {targetFormat.toUpperCase()}
                </Tag>
              )}
              <Button
                as="a"
                href={convertedFileUrl}
                download={`${file?.name?.split('.')[0] || 'converted_file'}.${targetFormat}`}
                colorScheme="green"
              >
                Download Converted File
              </Button>
              <Button onClick={handleReset} variant="outline" colorScheme="blue">
                Convert Another File
              </Button>
            </VStack>
          </Box>
        ) : (
          <>
            <Text fontSize="md">Upload your document to convert</Text>

            <Box
              {...getRootProps()}
              border="2px dashed gray"
              p={6}
              w="100%"
              textAlign="center"
              cursor="pointer"
            >
              <input {...getInputProps()} />
              <Text>{file ? file.name : 'Drag & drop or click to upload'}</Text>
            </Box>

            {availableFormats.length > 0 && (
              <Select
                placeholder="Select target format"
                onChange={(e) => setTargetFormat(e.target.value)}
              >
                {availableFormats.map((fmt) => (
                  <option key={fmt} value={fmt}>{fmt.toUpperCase()}</option>
                ))}
              </Select>
            )}

            <Button
              colorScheme="blue"
              isLoading={isLoading}
              onClick={handleConvert}
              isDisabled={!file || !targetFormat}
            >
              Convert
            </Button>

            {isLoading && <Progress hasStripe isAnimated value={progress} w="100%" />}
          </>
        )}
      </VStack>
    </Box>
  );
};

export default ConvertUpload;