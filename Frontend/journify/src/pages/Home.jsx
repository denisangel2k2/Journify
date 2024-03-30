import React, {useState,useEffect} from 'react';
import '../styles/components/home.scss';
import JournalCell from "../components/home-components/JournalCell";
import { Modal } from 'react-bootstrap';
import UserContainer from '../components/home-components/UserContainer';
import TableHistory from '../components/home-components/TableHistory';

export const Home = () => {
  const [cells,setCells] = useState([]);
  const [isModalVisible,setIsModalVisible] = useState(false);
  const [selectedCell,setSelectedCell] = useState({});
  const fetchCells = () => {
    return [
      { id: 1, img: "https://letsenhance.io/static/8f5e523ee6b2479e26ecc91b9c25261e/1015f/MainAfter.jpg" },
      { id: 2, img: "https://i.scdn.co/image/ab67616d0000b2734c53f577a646d5fe275ceadb" },
      { id: 3, img: "" },
      { id: 3, img: "" },
      { id: 3, img: "" },
      { id: 3, img: "" },
      { id: 3, img: "" },
      { id: 3, img: "" },
      { id: 3, img: "" },
      { id: 3, img: "" },
      { id: 3, img: "" },
      { id: 3, img: "" },


    ];
  };

  useEffect(()=>{
    const fetchedCells = fetchCells(); 
    setCells(fetchedCells);
  },[]);

  const handleClickOnCell = (item) => {
    setIsModalVisible(true);
    setSelectedCell(item);
  }
  return (
    <>      
      <Modal show={isModalVisible}>
          <Modal.Header>
            <Modal.Title>{selectedCell.id}</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            <p>Modal body text goes here.</p>
          </Modal.Body>
          <Modal.Footer>
            <button onClick={()=>{ setIsModalVisible(false) }}>Close</button>
          </Modal.Footer>
      </Modal>  
      <div class="home-background">
        <div className="upper-container">
          <UserContainer/>
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
        <TableHistory/>
      </div>
      
    </>
    
    );
  }
  
  export default Home;
