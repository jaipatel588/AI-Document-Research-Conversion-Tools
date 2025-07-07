const BASE_URL = "http://localhost:8000/api/v1"; // Update if deployed

// Upload & extract text from file
export const uploadDocument = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${BASE_URL}/upload-document`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) throw new Error("Failed to upload document.");
  return await res.json();
};

// Convert file format
export const convertDocument = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${BASE_URL}/convert-document`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) throw new Error("Failed to convert document.");
  return await res.json();
};