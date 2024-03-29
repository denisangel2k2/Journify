
const JournalCell = ({onClick,item}) => {
    return (
        <div className="journal-cell" onClick={()=>{onClick()}}>
            {item.img &&
            <img src={item.img} alt="journal-cell"></img>  
            }
        </div>
    );
}
export default JournalCell;