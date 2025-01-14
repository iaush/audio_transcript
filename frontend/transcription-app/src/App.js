import './App.css';
import SearchBar from './components/SearchBar';
import Button from '@mui/material/Button';


function App() {
  return (
    <div className="App">

        <div className='App-body'>

          <div className='App-header'>
            <SearchBar 
              onSearch={(searchTerm) => {
              console.log(searchTerm);
              }}
            />
            <Button 
            sx={{
              width: '150px',
              padding: '20px 20px',
              fontSize: '16px',
            }}
            
            variant="contained">Upload</Button>
          </div>
          
        </div>
        
    
    </div>
  );
}

export default App;
