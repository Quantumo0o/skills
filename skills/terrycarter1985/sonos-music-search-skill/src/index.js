const { BraveSearch } = require('@brave/search-api');
const Sonos = require('sonos');

if (!process.env.BRAVE_API_KEY) {
  throw new Error('BRAVE_API_KEY environment variable is required');
}

const braveSearch = new BraveSearch(process.env.BRAVE_API_KEY);

async function searchAndPlay(speakerName, query) {
  // Search for music using Brave Search
  const searchResults = await braveSearch.web(`${query} site:spotify.com/track`, {
    count: 5,
    safesearch: 'off'
  });

  if (!searchResults.web || searchResults.web.results.length === 0) {
    throw new Error(`No results found for query: ${query}`);
  }

  // Extract Spotify URI from first result
  const firstResult = searchResults.web.results[0];
  const spotifyUri = firstResult.url.replace('https://open.spotify.com/track/', 'spotify:track:');

  // Find Sonos speaker
  const devices = await Sonos.DeviceDiscovery();
  const speaker = devices.find(d => d.name === speakerName);
  
  if (!speaker) {
    throw new Error(`Speaker not found: ${speakerName}`);
  }

  // Play the track
  await speaker.play(spotifyUri);
  
  return {
    success: true,
    track: firstResult.title,
    speaker: speakerName,
    uri: spotifyUri
  };
}

async function getCurrentTrack(speakerName) {
  const devices = await Sonos.DeviceDiscovery();
  const speaker = devices.find(d => d.name === speakerName);
  
  if (!speaker) {
    throw new Error(`Speaker not found: ${speakerName}`);
  }

  const currentTrack = await speaker.currentTrack();
  return currentTrack;
}

// CLI usage
if (require.main === module) {
  const [,, command, speakerName, ...queryParts] = process.argv;
  const query = queryParts.join(' ');

  (async () => {
    try {
      if (command === 'play') {
        const result = await searchAndPlay(speakerName, query);
        console.log(`Playing "${result.track}" on ${result.speaker}`);
      } else if (command === 'current') {
        const track = await getCurrentTrack(speakerName);
        console.log(`Currently playing: ${track.title} by ${track.artist}`);
      } else {
        console.log('Usage: node index.js play <speaker-name> <search-query>');
        console.log('       node index.js current <speaker-name>');
        process.exit(1);
      }
    } catch (error) {
      console.error('Error:', error.message);
      process.exit(1);
    }
  })();
}

module.exports = { searchAndPlay, getCurrentTrack };
