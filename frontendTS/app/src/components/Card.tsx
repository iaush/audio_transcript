import React, { useState } from "react";
import "./Card.css";
import api from "../services/api";
import config from "../config";

interface CardProps {
  header: string;
  subtitle: string;
  upload_path: string;
  text: string;
  searchTerm: string;
  setReload: any
}

interface HighlightProps {
  text: string;
  searchTerm: string;
}

let backend = config.backendURL;

const Card = ({
  header,
  subtitle,
  upload_path,
  text,
  searchTerm,
  setReload
}: CardProps) => {
  
  const [open, setOpen] = useState(false);
  const [error, setError] = useState("");

  // const TextHighlighter = ({ text, searchTerm }: HighlightProps) => {
  //   const highlightedText = text
  //     .split(new RegExp(`(${searchTerm})`, "gi"))
  //     .map((part, index) =>
  //       part.toLowerCase() === searchTerm.toLowerCase() ? (
  //         <span key={index} className="highlight">
  //           {part}
  //         </span>
  //       ) : (
  //         part
  //       )
  //     );

  //   return (
  //     <div>
  //       <p>{highlightedText}</p>
  //     </div>
  //   );
  // };

  const handleDelete = async (upload_path: string) => {
    api.delete(`/transcription`, {params: { upload_path }})
    .then((response) => {
      setReload((prev:boolean)=>!prev)
    })
    .catch((error) => setError(error.message));
  }

  return (
    <div className="card-container">
      <div className="card">
        <div className="card-content">
          <div className="card-header">{header}</div>
          <div className="card-body">{`Upload Date: ${new Date(subtitle).toLocaleString()})`}</div>
        </div>
        <div>
          <button className="card-button" onClick={() => setOpen(!open)}>
            {open ? `Close` : `View Details`}
          </button>
          <button className="card-button" style={{backgroundColor : 'red'}} onClick={()=>handleDelete(upload_path)}>Delete</button>
        </div>
      </div>

      {open && (
        <div style={{ display: "flex" }}>
          <div className="audio-container">
            <h3>Audio</h3>
            <audio controls src={`${backend}/${upload_path}`} />
          </div>
          <div className="audio-container" style={{ width: "70%" }}>
            <h3>Transcription</h3>
            <div className="scroll-box">
              {/* <TextHighlighter text={text} searchTerm={searchTerm} /> */}
              <p>{text}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Card;
