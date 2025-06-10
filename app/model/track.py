class Track:
    """Represents a track.
    """
    def __init__(self, id: str, name: str, danceability: float, instrumentalness: float, energy: float, valence: float, artists: str):
        """Represents the constructor.
        Args:
            id (str): The track ID.
            name (str): The track name.
            danceability (float): The track danceability (between 0 and 1).
            instrumentalness (float): The track instrumentalness (between 0 and 1).
            energy (float): The track energy (between 0 and 1).
            valence (float): The track valence (between 0 and 1).
            artists (str): The track artists (textual representation).
        """
        self.id = id
        self.name = name
        self.danceability = danceability
        self.instrumentalness = instrumentalness
        self.energy = energy
        self.valence = valence
        self.artists = artists