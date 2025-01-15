import React, { useEffect, useState, useCallback } from "react";
import "./App.css";
import SearchBar from "./components/SearchBar";
import Card from "./components/Card";
import api from "./services/api";
import { Button } from "@mui/material";
import { Debounce } from "./services/ultils";

interface Item {
  file_name: string;
  created: string;
  upload_path: string;
  transcription: string;
}
function App() {
  const [items, setItems] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");

  useEffect(() => {
    if (searchTerm == "") {
      api.get("/transcriptions").then((response) => setItems(response.data));
    }
  }, [searchTerm]);

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

  console.log(items);

  let cardItems = items.map((item: Item) => {
    return (
      <Card
        header={item.file_name}
        subtitle={item.created}
        upload_path={item.upload_path}
        text={item.transcription}
        searchTerm={searchTerm}
      />
    );
  });
  return (
    <div className="App">
      <div className="App-body">
        <div className="App-header">
          <SearchBar onSearch={setSearchTerm} />
          <button
            style={{
              width: "150px",
              padding: "20px 20px",
              fontSize: "16px",
              backgroundColor: "#61dafb",
              borderRadius: "25px",
            }}
          >
            Upload
          </button>
        </div>

        <div className="App-content">{cardItems}</div>
      </div>
    </div>
  );
}

export default App;
