import React from "react";
import TagFacesIcon from '@mui/icons-material/TagFaces';
import SentimentDissatisfiedIcon from '@mui/icons-material/SentimentDissatisfied';
import QuestionMarkIcon from '@mui/icons-material/QuestionMark';
import OfflineBoltIcon from '@mui/icons-material/OfflineBolt';
import SelfImprovementIcon from '@mui/icons-material/SelfImprovement';


const JournalHistoryItem = ({ journal, onClick }) => {
    const getDate = (timestamp) => {
        // Convert timestamp to milliseconds if it's not already in milliseconds
        const timestampMs = timestamp * 1000; // Convert seconds to milliseconds
        const date = new Date(timestampMs);
        const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
        const formattedDate = new Intl.DateTimeFormat('en-US', options).format(date);
        return formattedDate;
    };
    return (
        <div className="journal-table-history" onClick={onClick}>
            {/* convert timestamp of journal['date] to actual date */}
            <div className="journal-banner">
                {journal.emotion === 'Happy' && <TagFacesIcon className="emotions-icon" />}
                {journal.emotion === 'Sad' && <SentimentDissatisfiedIcon className="emotions-icon" />}
                {journal.emotion === 'Energetic' && <OfflineBoltIcon className="emotions-icon" />}
                {journal.emotion === 'Calm' && <SelfImprovementIcon className="emotions-icon" />}
                {journal.emotion === 'not set' && <QuestionMarkIcon className="emotions-icon" />}
            </div>
            <div className="journal-date">{getDate(journal['date'])}</div>
            <img src={journal['questions'][0]['img']} alt="journal image"></img>
        </div>
    );
};

export default JournalHistoryItem;
