import React from "react";

const JournalHistoryItem = ({journal, onClick}) => {
    return (
        <div className="journal-table-history" onClick={onClick}>
            <img src={journal['questions'][0]['img']} alt="journal image"></img>
        </div>
    );
};

export default JournalHistoryItem;
