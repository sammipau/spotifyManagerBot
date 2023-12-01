import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime, timedelta, date

class SpotifyManager:
    playlistPerms: str = 'playlist-modify-public playlist-modify-private user-library-read'
    playlistID: str = '4YCCVRarApNjFf8MIXpGjw' # hard coded to circlin
    sp: spotipy.Spotify
    url: str = 'https://accounts.spotify.com/api/token'
    token: str
    fail: bool = False

    def __init__(self):
        try:
            self.sp = spotipy.Spotify(auth_manager = SpotifyOAuth(scope = self.playlistPerms))
        except:
            fail = True
    
    def get_recently_added_tracks(self):
        # issue: limits by 20 but specifying limit breaks it
        allTracks = self.sp.current_user_saved_tracks()
        # improvement - user can specify time delta
        timeFrame: date = date.today() - timedelta(days = 30)
        tracks = []
        for item in allTracks['items']:
            added: date = datetime.strptime(item['added_at'], '%Y-%m-%dT%H:%M:%SZ').date()
            if added >= timeFrame:
                tracks.append(item['track']['uri'])

        return tracks

    def add_recent(self):
        likedTracks = self.get_recently_added_tracks()
        playlistRaw= self.sp.playlist_tracks(self.playlistID)
        playlistTracks = self.to_uris(playlistRaw)
        tracks = list(set(likedTracks) - set(playlistTracks))
        self.sp.playlist_add_items(self.playlistID, tracks)
        return len(tracks)
    
    def remove_old(self):
        tracks = []
        self.sp.playlist_remove_all_occurrences_of_items(self.playlistID, tracks)
        return 1
    
    def to_uris(self, tracks):
        ret = []
        for item in tracks['items']:
            ret.append(item['track']['uri'])
        return ret