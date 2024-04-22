import TagFacesIcon from '@mui/icons-material/TagFaces';
import SentimentDissatisfiedIcon from '@mui/icons-material/SentimentDissatisfied';
import QuestionMarkIcon from '@mui/icons-material/QuestionMark';
import OfflineBoltIcon from '@mui/icons-material/OfflineBolt';
import SelfImprovementIcon from '@mui/icons-material/SelfImprovement';

const JournalCell = ({ onClick, item }) => {
    return (
        <div className="journal-cell" onClick={() => { onClick() }}>
            {item.img &&
                <img src={item.img} alt="journal-cell"></img>
                
            }

            <div className='journal-banner'>
                {item.emotion === 'Happy' &&  <TagFacesIcon className="emotions-icon"/> }
                {item.emotion === 'Sad' &&  <SentimentDissatisfiedIcon className="emotions-icon" /> }
                {item.emotion === 'Energetic' &&  <OfflineBoltIcon className="emotions-icon"/> }
                {item.emotion === 'Calm' &&  <SelfImprovementIcon className="emotions-icon"/> }
                {item.emotion === 'not set' && item.answer!=='not set' && <QuestionMarkIcon className="emotions-icon"/> }
            </div>
        </div>
    );
}
export default JournalCell;