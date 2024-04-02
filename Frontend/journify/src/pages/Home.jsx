import React, { useState, useEffect } from 'react';
import '../styles/components/home.scss';
import JournalCell from "../components/home-components/JournalCell";
import { Modal } from 'react-bootstrap';
import UserContainer from '../components/home-components/UserContainer';
import TableHistory from '../components/home-components/TableHistory';
import SearchBar from '../components/home-components/SearchBar';
import { useLocalStorage } from '../providers/AuthProvider';

export const Home = () => {
  const [cells, setCells] = useLocalStorage('cells', []);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [selectedCell, setSelectedCell] = useState({});
  const [currentSelectedSong, setCurrentSelectedSong] = useState(null);


  const fetchCells = () => {
    return [
      { id: 1, img: "https://letsenhance.io/static/8f5e523ee6b2479e26ecc91b9c25261e/1015f/MainAfter.jpg", "song": "" },
      { id: 2, img: "", "song": "" },
      { id: 3, img: "", "song": "" },
      { id: 3, img: "", "song": "" },
      { id: 3, img: "", "song": "" },
      { id: 3, img: "", "song": "" },
      { id: 3, img: "", "song": "" },
      { id: 3, img: "", "song": "" },
      { id: 3, img: "", "song": "" },
      { id: 3, img: "", "song": "" },
      { id: 3, img: "", "song": "" },
      { id: 3, img: "", "song": "" },
    ];
  };

  useEffect(() => {
    const fetchedCells = fetchCells();
    setCells(fetchedCells);
  }, []);

  const saveModalChanges = () => {

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
          <Modal.Title>{selectedCell.id}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <p>Modal body text goes here.</p>
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
              {cells.map(cell => (
                <JournalCell
                  key={cell.id}
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
