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
  const [items, setItems] = useState<Item[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [open, setOpen] = useState(false);
  const [reload, setReload] = useState(false);
  const [debouncedSearchTerm, setDebouncedSearchTerm] = useState(searchTerm);
  const debounceDelay = 500;

  // debounce the search term to avoid making too many requests
  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedSearchTerm(searchTerm);
    }, debounceDelay);

    return () => {
      clearTimeout(handler);
    };
  }, [searchTerm]);

  useEffect(() => {
    if (debouncedSearchTerm === "") {
      api.get("/transcriptions").then((response) => {
        console.log(response.data);
        setItems(response.data)
      });
    }
  }, [debouncedSearchTerm, reload]);

  // retrieve the transcriptions from the backend and reload the page when the reload state changes
  useEffect(() => {
    if (debouncedSearchTerm !== "") {
      api
        .get("/search", { params: { search_term: debouncedSearchTerm } })
        .then((response) => {
          console.log(response.data);
          setItems(response.data)}).catch((error) =>
            console.error("Error fetching search results:", error)
          );
    }
  }, [debouncedSearchTerm, reload]);

  // useEffect(() => {
  //   if (searchTerm == "") {
  //     api.get("/transcriptions").then((response) => setItems(response.data));
  //   }
  // }, [searchTerm, reload]);

  // useEffect(() => {
  //   if (searchTerm !== "") {
  //     api
  //       .get("/search", { params: { search_term: searchTerm } })
  //       .then((response) => setItems(response.data));
  //   }
  // }, [searchTerm]);

  // const debouncedSearch = useCallback(
  //   Debounce((term: string) => {
  //     api
  //       .get("/search", { params: { search_term: term } })
  //       .then((response) => setItems(response.data))
  //       .catch((error) =>
  //         console.error("Error fetching search results:", error)
  //       );
  //   }, 1000),
  //   []
  // );

  // useEffect(() => {
  //   if (searchTerm !== "") {
  //     debouncedSearch(searchTerm);
  //   }
  // }, [searchTerm]);

  // renders all the transcriptions as cards
  let cardItems = items?.map((item: Item) => {
    return (
      <Card
        header={item.file_name}
        subtitle={item.created}
        upload_path={item.upload_path}
        text={item.transcription}
        searchTerm={searchTerm}
        setReload={setReload}
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
          <div className="App-content">{cardItems.length>0?cardItems:<p>No results found</p>}</div>
        </div>
      </div>
    </>
  );
}

export default App;
