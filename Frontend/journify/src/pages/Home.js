export const Home = () => {
    const handleGetPlaylists = () => {
      const token = localStorage.getItem('accessToken');
      const playlists = fetch('http://localhost:8888/playlists', {
        headers: {
          'Authorization': `${token}`
        }
      }
    ).then(response => response.json()).then(data => console.log(data))  
  }
      return (
        <div>
          {<button onClick={handleGetPlaylists}>Get Playlists</button>}
        </div>
      );
}

export default Home;