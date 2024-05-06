import React from 'react';
import PieChartLatestJournal from './PieChartLatestJournal';
import RadarChartAllJournals from './RadarChartAllJournals';
const UserStatistics = () => {
    return (
        <div className="user-statistics">
            <PieChartLatestJournal />
            <RadarChartAllJournals />
        </div>
    );
};
export default UserStatistics;