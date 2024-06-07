const BASE_URL='http://localhost:8888';
const urls = {
    refresh_token: `${BASE_URL}/refresh_token`,
    history: `${BASE_URL}/history`,
    classify: `${BASE_URL}/classify`,
    journal: `${BASE_URL}/journal`,
    report: `${BASE_URL}/report`,
    all_report: `${BASE_URL}/all_report`,
    songs: `${BASE_URL}/songs`,
    user: `${BASE_URL}/user`
}

const fetchNewTokenFromAPI = async (token, refreshToken) => {
    const response = await fetch(urls['refresh_token'], {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `${token}`
        },
        body: JSON.stringify({
            refresh_token: refreshToken
        }),
    });

    if (!response.ok) {
        throw new Error('Failed to fetch data');
    }
    return await response.json();

}

const fetchJournalHistoryFromAPI = async (token, userInfo) => {
    const history = await fetch(urls['history'], {
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

    if (!history.ok) {
        throw new Error('Failed to fetch data');
    }

    return await history.json();
}
const fetchSubmitSongFromAPI = async (token, userInfo, selectedCell) => {
    const newCells = await fetch(urls['classify'], {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `${token}`
        },
        body: JSON.stringify({
            email: userInfo.email,
            spotify_id: userInfo.id,
            question: selectedCell,
            index: selectedCell.index,
            img: selectedCell.image,
        })
    });
    return newCells.json();

};

const fetchCellsFromAPI = async (token, userInfo) => {

    const journal = await fetch(urls['journal'], {
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
    return await journal.json();

}

const fetchPieChartReportFromAPI = async (token, userInfo) => {
    const data = await fetch(urls['report'], {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `${token}`
        },
        body: JSON.stringify({
            email: userInfo.email,
            spotify_id: userInfo.id
        })
    });
    return await data.json();
};
const fetchRadarChartReportFromAPI = async (token, userInfo) => {
    const data = await fetch(urls['all_report'], {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `${token}`
        },
        body: JSON.stringify({
            email: userInfo.email,
            spotify_id: userInfo.id
        })
    });
    return await data.json();
};

const fetchSongsFromAPI = async (token, startingName) => {
    const encodedName = encodeURIComponent(startingName);
    return await fetch(`${urls['songs']}?searchName=${encodedName}`, {
        headers: {
            'Authorization': `${token}`
        }
    });

}

const fetchUser = async(token) => {
    return await fetch(urls['user'], {
                headers: {
                    'Authorization': `${token}`
                }
            });

};

export {fetchUser, fetchSongsFromAPI, fetchRadarChartReportFromAPI, fetchPieChartReportFromAPI, fetchNewTokenFromAPI, fetchJournalHistoryFromAPI, fetchSubmitSongFromAPI, fetchCellsFromAPI };
