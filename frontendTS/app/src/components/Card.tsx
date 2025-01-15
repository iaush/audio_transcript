import React, { useState } from "react";
import "./Card.css";

interface CardProps {
  header: string;
  subtitle: string;
  upload_path: string;
  text: string;
  searchTerm: string;
}

interface HighlightProps {
  text: string;
  searchTerm: string;
}

let backend = "http://localhost:8000";

const Card = ({
  header,
  subtitle,
  upload_path,
  text,
  searchTerm,
}: CardProps) => {
  let [date, timing] = subtitle.split("T");
  const [open, setOpen] = useState(false);

  const TextHighlighter = ({ text, searchTerm }: HighlightProps) => {
    const highlightedText = text
      .split(new RegExp(`(${searchTerm})`, "gi"))
      .map((part, index) =>
        part.toLowerCase() === searchTerm.toLowerCase() ? (
          <span key={index} className="highlight">
            {part}
          </span>
        ) : (
          part
        )
      );

    return (
      <div className="scroll-box">
        <p>{highlightedText}</p>
      </div>
    );
  };

  return (
    <div className="card-container">
      <div className="card">
        <div className="card-content">
          <div className="card-header">{header}</div>
          <div className="card-body">{`Upload Date: ${date} (${
            timing.split(".")[0]
          })`}</div>
        </div>
        {/* <div>
          <audio controls src={`${backend}/${upload_path}`} />
        </div> */}
        <div>
          <button className="card-button" onClick={() => setOpen(!open)}>
            {open ? `Close` : `View Details`}
          </button>
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
              <TextHighlighter text={text} searchTerm={searchTerm} />
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Card;
