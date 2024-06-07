const urls= {
    refresh_token: 'http://localhost:8888/refresh_token',
    history: 'http://localhost:8888/history',
    classify: 'http://localhost:8888/classify',
    journal: 'http://localhost:8888/journal'
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

const fetchCellsFromAPI= async (token, userInfo) => {

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

export { fetchNewTokenFromAPI, fetchJournalHistoryFromAPI, fetchSubmitSongFromAPI, fetchCellsFromAPI };
