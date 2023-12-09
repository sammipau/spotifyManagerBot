import spotipy
from spotipy import SpotifyException
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime, timedelta, date

class SpotifyManager:
    playlistPerms: str = 'playlist-modify-public playlist-modify-private user-library-read'
    playlistID: str = '' # hard coded to circlin
    sp: spotipy.Spotify
    url: str = 'https://accounts.spotify.com/api/token'
    token: str
    fail: bool = False

    def __init__(self):
        try:
            self.sp = spotipy.Spotify(auth_manager = SpotifyOAuth(scope = self.playlistPerms))
        except:
            fail = True
    
    def add_recent(self, playlistName):
        self.get_playlist_id(playlistName)
        if (self.playlistID != ''):
            likedTracks = self.get_recently_added_tracks()
            playlistRaw= self.sp.playlist_tracks(self.playlistID)
            playlistTracks = self.to_uris(playlistRaw)
            tracks = list(set(likedTracks) - set(playlistTracks))
            if (len(tracks) != 0):
                self.sp.playlist_add_items(self.playlistID, tracks)
            return len(tracks)
        return 'PNF'
    
    def remove_old(self, playlistName):
        self.get_playlist_id(playlistName)
        if (self.playlistID != ''):
            try:
                if (self.playlistID != ''):
                    tracks = self.get_old_tracks()
                if (len(tracks) != 0):
                    self.sp.playlist_remove_all_occurrences_of_items(self.playlistID, tracks)
                    return len(tracks)
                if (len(tracks) == 0):
                    return 0
            except SpotifyException as e:
                print("error block")
                return "Error"
            else:
                return "Error"
        return 'PNF'
        
    # Helper functions below
    def get_playlist_id(self, name):
        id = ''
        search = self.sp.search(q = name, type = 'playlist')
        for playlist in search['playlists']['items']:
            if (playlist['name'] == name):
                id = playlist['uri']
        self.playlistID = id
    
    def get_recently_added_tracks(self):
        allTracks1 = self.sp.current_user_saved_tracks(limit = 50)
        allTracks2 = self.sp.current_user_saved_tracks(limit = 50, offset = 50)
        # improvement - user can specify time delta
        timeFrame: date = date.today() - timedelta(days = 30)
        tracks = []
        for item in allTracks1['items']:
            added: date = datetime.strptime(item['added_at'], '%Y-%m-%dT%H:%M:%SZ').date()
            if added >= timeFrame:
                tracks.append(item['track']['uri'])
        for item in allTracks2['items']:
            added: date = datetime.strptime(item['added_at'], '%Y-%m-%dT%H:%M:%SZ').date()
            if added >= timeFrame:
                tracks.append(item['track']['uri'])
        return tracks
    
    def to_uris(self, tracks):
        ret = []
        for item in tracks['items']:
            ret.append(item['track']['uri'])
        return ret
    
    def get_old_tracks(self):
        allTracks = self.sp.playlist_tracks(self.playlistID)
        timeFrame: date = date.today() - timedelta(days = 30)
        tracks = []
        for item in allTracks['items']:
            added: date = datetime.strptime(item['added_at'], '%Y-%m-%dT%H:%M:%SZ').date()
            if added < timeFrame:
                tracks.append(item['track']['uri'])
        return tracks
