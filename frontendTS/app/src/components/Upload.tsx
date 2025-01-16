import React, { useEffect, useState } from "react";
import "./Upload.css";
import api from "../services/api";

interface UploadProps {
  onClose: () => void;
  setReload: () => void;
}

const Upload = ({ onClose, setReload }: UploadProps) => {
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    const file = (document.getElementById("file") as HTMLInputElement)
      .files?.[0];

    const name = (document.getElementById("name") as HTMLInputElement).value;

    if (!file) {
      setError("Please select a file to upload");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("file_name", name);
    setError(""); // Clear any previous errors
    setLoading(true); // Set loading to true before sending the request

    api
      .post("/transcribe", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      .then((response) => {
        if (response.status == 200) {
          onClose();
          setReload();
        }
      })
      .catch((error) => {
        console.error("Error uploading file:", error);
        setError(error.message);
      })
      .finally(() => {
        setLoading(false); // Set loading to false after the request is complete
      });
  };
  return (
    <div className="upload-modal">
      <div className="upload-modal-content">
        <form className="upload-form">
          <div className="input-divs">
            <label htmlFor="file" className="upload-label">
              Choose a file :
            </label>
            <input
              type="file"
              id="file"
              name="file"
              accept="audio/*"
              className="upload-input"
              required
              multiple
            />
          </div>
          <div className="input-divs">
            <label htmlFor="name" className="upload-label">
              Filename :
            </label>
            <input type="text" id="name" className="upload-input" />
          </div>
        </form>
        <button
          className="close-button"
          style={{ backgroundColor: "#bae86f" }}
          onClick={handleSubmit}
        >
          Submit
        </button>
        <button onClick={onClose} className="close-button">
          Close
        </button>
        {error && <p>{error}</p>}
      </div>
      {loading && (
        <div className="loading">
          <div className="spinner"></div>
        </div>
      )}
    </div>
  );
};

export default Upload;
