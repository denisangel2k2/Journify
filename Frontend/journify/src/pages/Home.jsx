import React, { useState, useEffect } from 'react';
import '../styles/components/home.scss';
import JournalCell from "../components/home-components/JournalCell";
import { Modal } from 'react-bootstrap';
import UserContainer from '../components/home-components/UserContainer';
import TableHistory from '../components/home-components/TableHistory';
import SearchBar from '../components/home-components/SearchBar';
import { useAuth, useLocalStorage } from '../providers/AuthProvider';

export const Home = () => {
  const [cells, setCells] = useLocalStorage('cells', []);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [selectedCell, setSelectedCell] = useState({});
  const [currentSelectedSong, setCurrentSelectedSong] = useState(null);
  const { token, userInfo } = useAuth();

  const fetchCells = async () => {
    try {
      const journal = await fetch('http://localhost:8888/journal', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `${token}`
        },
        body: JSON.stringify({
          email: userInfo.email,
          spotify_id: userInfo.id
        })
      });

      if (!journal.ok) {
        throw new Error('Failed to fetch data');
      }
      const data = await journal.json();
      setCells(data);
    } catch (error) {
      console.log('Error fetching cells:', error);
    }
  };
  useEffect(() => {
    console.log('HEREEEE' + !cells)
    fetchCells();
  }, [token, userInfo]);

  const saveModalChanges = () => {
    setIsModalVisible(false);
    const newCells = cells;
    newCells.questions[selectedCell.index].song = currentSelectedSong;
    //fetch info from the server regarding the classification of the song and update the cell with the image and classification
    

    setCells(newCells);
  }

  const handleClickOnCell = (item) => {
    setIsModalVisible(true);
    setSelectedCell(item);
  }
  useEffect(() => {
    console.log(currentSelectedSong);
  }, [currentSelectedSong]);

  return (
    <>
      <Modal show={isModalVisible}>
        <Modal.Header>
          <Modal.Title>{selectedCell.index + 1}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <p>{selectedCell.question}</p>
          <SearchBar setCurrentSelectedSong={setCurrentSelectedSong}></SearchBar>
        </Modal.Body>
        <Modal.Footer>
          <button onClick={() => { setIsModalVisible(false) }}>Close</button>
        </Modal.Footer>
      </Modal>
      <div class="home-background">
        <div className="upper-container">
          <UserContainer />
          <div className="main-container">
            <div className="table-container">
              {cells?.questions && cells.questions.map(cell => (
                <JournalCell
                  key={cell.index}
                  item={cell}
                  onClick={() => handleClickOnCell(cell)}
                />
              ))}
            </div>

          </div>
        </div>
        <TableHistory />
      </div>
    </>

  );
}

export default Home;
