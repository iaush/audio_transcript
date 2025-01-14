import React, { useState } from 'react';

const SearchBar = ({ onSearch }) => {
    const [searchTerm, setSearchTerm] = useState('');
    
    const handleSearch = (event) => {
        setSearchTerm(event.target.value);
        onSearch(event.target.value);
    };
    
    return (
        <input
        style={{ 
            minWidth: '50%',
            maxWidth: '70%',
            padding: '20px 20px',
            fontSize: '25px',
            margin: '0 20px',
            borderRadius: '25px',
            fontFamily: 'Arial',
         }}
        type="text"
        placeholder="Search for keywords to find related transcriptions"
        value={searchTerm}
        onChange={handleSearch}
        />
    );
    }

export default SearchBar;