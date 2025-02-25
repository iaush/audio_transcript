import React, { useState } from "react";
import { Debounce } from "../services/ultils";

interface SearchBarProps {
  onSearch: (value: string) => void;
}

interface HandleSearchEvent {
  target: {
    value: string;
  };
}
const SearchBar: React.FC<SearchBarProps> = ({ onSearch }) => {
  const [searchTerm, setSearchTerm] = useState("");
  
  // send the search term back to the parent component
  const handleSearch = (event: HandleSearchEvent) => {
    setSearchTerm(event.target.value);
    onSearch(event.target.value);
  };

  return (
    <input
      style={{
        minWidth: "50%",
        maxWidth: "70%",
        padding: "20px 20px",
        fontSize: "25px",
        margin: "0 20px",
        borderRadius: "25px",
        fontFamily: "Arial",
      }}
      type="text"
      placeholder="Search for file name"
      value={searchTerm}
      onChange={handleSearch}
    />
  );
};

export default SearchBar;
