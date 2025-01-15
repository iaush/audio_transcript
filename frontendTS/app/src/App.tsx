import React, { useEffect, useState, useCallback } from "react";
import "./App.css";
import SearchBar from "./components/SearchBar";
import Card from "./components/Card";
import api from "./services/api";
import { Button } from "@mui/material";
import { Debounce } from "./services/ultils";
import Upload from "./components/Upload";
import Health from "./components/Health";

interface Item {
  file_name: string;
  created: string;
  upload_path: string;
  transcription: string;
}
function App() {
  const [items, setItems] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [open, setOpen] = useState(false);
  const [reload, setReload] = useState(false);

  useEffect(() => {
    if (searchTerm == "") {
      api.get("/transcriptions").then((response) => setItems(response.data));
    }
  }, [searchTerm, reload]);

  // useEffect(() => {
  //   if (searchTerm !== "") {
  //     api
  //       .get("/search", { params: { search_term: searchTerm } })
  //       .then((response) => setItems(response.data));
  //   }
  // }, [searchTerm]);

  const debouncedSearch = useCallback(
    Debounce((term: string) => {
      api
        .get("/search", { params: { search_term: term } })
        .then((response) => setItems(response.data))
        .catch((error) =>
          console.error("Error fetching search results:", error)
        );
    }, 300),
    []
  );

  useEffect(() => {
    if (searchTerm !== "") {
      debouncedSearch(searchTerm);
    }
  }, [searchTerm]);

  let cardItems = items.map((item: Item) => {
    return (
      <Card
        header={item.file_name}
        subtitle={item.created}
        upload_path={item.upload_path}
        text={item.transcription}
        searchTerm={searchTerm}
        setReload={() => setReload(!reload)}
      />
    );
  });
  return (
    <>
      <div className="App">
        <div className="App-body">
          <Health />
          <div>
            {open && (
              <Upload
                onClose={() => setOpen(false)}
                setReload={() => setReload(!reload)}
              />
            )}
          </div>
          <div className="App-header">
            <SearchBar onSearch={setSearchTerm} />
            <button className="upload-button" onClick={() => setOpen(!open)}>
              Upload
            </button>
          </div>
          <div className="App-content">{cardItems}</div>
        </div>
      </div>
    </>
  );
}

export default App;
