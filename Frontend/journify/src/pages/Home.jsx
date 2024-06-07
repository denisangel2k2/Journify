import React, { useState, useEffect } from 'react';
import '../styles/components/home.scss';
import JournalCell from "../components/home-components/JournalCell";
import { Modal } from 'react-bootstrap';
import UserContainer from '../components/home-components/UserContainer';
import TableHistory from '../components/home-components/TableHistory';
import SearchBar from '../components/home-components/SearchBar';
import { useAuth, useLocalStorage } from '../providers/AuthProvider';
import HistoryJournalSongs from '../components/home-components/HistoryJournalSongs';
import { fetchCellsFromAPI, fetchSubmitSongFromAPI, fetchJournalHistoryFromAPI, fetchNewTokenFromAPI } from '../providers/API';

export const Home = () => {
  const [cells, setCells] = useLocalStorage('cells', []);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [isHistoryModalVisible, setIsHistoryModalVisible] = useState(false);
  const [selectedCell, setSelectedCell] = useState({});
  const [currentSelectedSong, setCurrentSelectedSong] = useState(null);
  const { token, userInfo } = useAuth();
  const [history, setHistory] = useLocalStorage('history', []);
  const [currentSelectedJournal, setCurrentSelectedJournal] = useState({});

  const {setToken, refreshToken, setExpiresAt,expiresAt} = useAuth();


  const fetchCells = async () => {
    try {
      
      const data = await fetchCellsFromAPI(token, userInfo);
      setCells(data);
    } catch (error) {
      console.log('Error fetching cells:', error);
    }
  };
  // const fetchSubmitSong = async () => {
  //   const newCells = await fetch('http://localhost:8888/classify', {
  //     method: 'POST',
  //     headers: {
  //       'Content-Type': 'application/json',
  //       'Authorization': `${token}`
  //     },
  //     body: JSON.stringify({
  //       email: userInfo.email,
  //       spotify_id: userInfo.id,
  //       question: selectedCell,
  //       index: selectedCell.index,
  //       img: selectedCell.image,
  //     })
  //   });
  //   return newCells.json();

  // };
  const fetchJournalHistory = async () => {
    try {
     
      const data = await fetchJournalHistoryFromAPI(token, userInfo);
      setHistory(data);
    }
    catch (error) {
      console.log('Error fetching history:', error);
    }

  };
  const fetchNewToken = async () => {
    try {
      
      const data = await fetchNewTokenFromAPI(token, refreshToken);
      setToken(data.access_token);
      setExpiresAt(data.expires_at);
    }
    catch (error) { 
      console.log('Error fetching new token:', error);
    }
  }

  useEffect(() => {
    const currentTimeStamp = Date.now() / 1000;
    console.log(currentTimeStamp-expiresAt)
    if (currentTimeStamp >= expiresAt) 
    {
      fetchNewToken();
    }
  
  },[refreshToken]);

  useEffect(() => {
    fetchCells();
    fetchJournalHistory();
  }, [token, userInfo]);

 
  const saveModalChanges = () => {
    setIsModalVisible(false);

    const copySelectedCell = selectedCell;
    copySelectedCell.answer = currentSelectedSong.song + " - " + currentSelectedSong.artist;
    copySelectedCell.img = currentSelectedSong.image;

    setSelectedCell(copySelectedCell);
    fetchSubmitSongFromAPI(token,userInfo,selectedCell).then((newCells) => {
      setCells(newCells);
    });
  }

  const handleClickOnCell = (item) => {
    setIsModalVisible(true);
    setSelectedCell(item);
  }

  return (
    <>
      <Modal show={isModalVisible} id="modal-song">
        <Modal.Header>
          <Modal.Title>Quote #{selectedCell.index + 1}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <div className="container">
            <p>{selectedCell.question}</p>
            {selectedCell.answer !== 'not set' && <p>Answer: {selectedCell.answer}</p>}
            {selectedCell.emotion !== 'not set' && <p>Emotion: {selectedCell.emotion}</p>}
          </div>

          <SearchBar setCurrentSelectedSong={setCurrentSelectedSong}></SearchBar>
        </Modal.Body>
        <Modal.Footer>
          <button onClick={() => { saveModalChanges() }}>Submit</button>
          <button onClick={() => { setIsModalVisible(false) }}>Close</button>
        </Modal.Footer>
      </Modal>

      <Modal show={isHistoryModalVisible} id="modal-history" style={{ maxWidth: '100%', maxHeight: '100%' }}>

        <Modal.Body>
          <HistoryJournalSongs journal={currentSelectedJournal} />
        </Modal.Body>
        <Modal.Footer>
          <button onClick={() => { setIsHistoryModalVisible(false) }}>Close</button>
        </Modal.Footer>
      </Modal>

      <div class="home-background">
        <div className="upper-container">
          <UserContainer />
          <div className="main-container">
            <h1>Your Journify for today</h1>

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
        <TableHistory setIsHistoryModalVisible={setIsHistoryModalVisible} history={history} setCurrentSelectedJournal={setCurrentSelectedJournal} />
      </div>
    </>

  );
}

export default Home;
