import TextField from "@mui/material/TextField";
import Autocomplete from "@mui/material/Autocomplete";

import React, { useState } from 'react';
import { useAuth } from '../../providers/AuthProvider';

const SearchBar = ({ setCurrentSelectedSong }) => { 
    const [songs, setSongs] = useState([]);
    let timeoutId;
    const { token } = useAuth();

    const fetchSongs = async (startingName) => {
        try {
            const encodedName = encodeURIComponent(startingName);
            const response = await fetch(`http://localhost:8888/songs?searchName=${encodedName}`, {
                headers: {
                    'Authorization': `${token}`
                }
            });
            const data = await response.json();
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
        clearTimeout(timeoutId); // Clear previous timeout

        // Set new timeout to call fetchSongs after 500 milliseconds of user inactivity
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
                        label="Search Box"
                        style={{ color: 'white', borderRadius: 5 }}
                        onChange={handleInputChange}
                    />
                )}
            />

        </>
    );
};
export default SearchBar;
