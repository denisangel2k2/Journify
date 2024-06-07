import TextField from "@mui/material/TextField";
import Autocomplete from "@mui/material/Autocomplete";

import React, { useState } from 'react';
import { useAuth } from '../../providers/AuthProvider';
import { fetchSongsFromAPI } from "../../providers/API";

const SearchBar = ({ setCurrentSelectedSong }) => { 
    const [songs, setSongs] = useState([]);
    let timeoutId;
    const { token } = useAuth();

    const fetchSongs = async (startingName) => {
        try {
            
            const response = (await fetchSongsFromAPI(token,startingName));
            const data= await response.json();
            setSongs(data);
        } catch (error) {
            console.error('Error fetching songs:', error);
        }
        
    }
    const handleSelectedSong = (event, value) => {
        setCurrentSelectedSong(value);
    }
    const handleInputChange = (event) => {
        const input = event.target.value;
        clearTimeout(timeoutId); 

        timeoutId = setTimeout(() => {
            fetchSongs(input);
        }, 500);
    };
    return (
        <>
            <Autocomplete
                freeSolo
                autoComplete
                autoHighlight
                options={songs}
                getOptionLabel={(option) => `${option.song} - ${option.artist}`}
                getOptionSelected={(option, value) => { return option.song === value.song }}
                onChange={handleSelectedSong}
                renderInput={(params) => (
                    <TextField
                        {...params}
                        variant="outlined"
                        label="Search Song"
                        className="search-bar"
                        style={{ color: 'white', borderRadius: 5 }}
                        onChange={handleInputChange}
                    />
                )}
            />

        </>
    );
};
export default SearchBar;
