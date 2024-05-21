import React from 'react';
import PieChartLatestJournal from './PieChartLatestJournal';
import RadarChartAllJournals from './RadarChartAllJournals';
const UserStatistics = ({cells}) => {
    return (
        <div className="user-statistics">
            <PieChartLatestJournal cells={cells}/>
            <RadarChartAllJournals cells={cells}/>
        </div>
    );
};
export default UserStatistics;