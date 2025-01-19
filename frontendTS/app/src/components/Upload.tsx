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

  // handle the file upload for multiples files or single, filename taken as input (FILENAME) if multiple files are uploaded
  const handleSubmit = async () => {
    const files = (document.getElementById("file") as HTMLInputElement).files;

    const name = (document.getElementById("name") as HTMLInputElement).value;

    if (!files) {
      setError("Please select a file to upload");
      return;
    }

    const formData = new FormData();
    if (files.length > 1) {
      for (let i = 0; i < files.length; i++) {
        formData.append("files", files[i]);
        formData.append("file_names", `${name} (${files[i].name})`);
      }
    } else {
      formData.append("files", files[0]);
      formData.append("file_names", name);
    }

    setError(""); 
    setLoading(true); 

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
        setLoading(false); 
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
