import os
from pathlib import Path
from dataclasses import dataclass

@dataclass
class Config:
    """Represents the configuration dynamically storing all data source paths.
    Attributes:
        project_path (str): The root project path.
        tracks_path (str):  The path leading to the tracks CSV file.
        artists_path (str): The path leading to the artists CSV file.
        albums_path (str): The path leading to the albums CSV file.
        lyrics_features_path (str): The path leading to the lyrics features CSV file.
        preprocessed_data_path (str): The path leading to the CSV file containing information about the preprocessed data.   
    """
    project_path: Path = Path(__file__).resolve().parents[1]

    tracks_path: Path = project_path.joinpath("spotify_data", "SpotGenTrack", "DataSources", "spotify_tracks.csv")
    
    artists_path: Path = project_path.joinpath("spotify_data", "SpotGenTrack", "DataSources", "spotify_artists.csv")
    
    albums_path: Path = project_path.joinpath("spotify_data", "SpotGenTrack", "DataSources", "spotify_albums.csv")
    
    lyrics_features_path: Path = project_path.joinpath("spotify_data", "SpotGenTrack", "FeaturesExtracted", "lyrics_features.csv")
    
    preprocessed_data_path: Path = project_path.joinpath("spotify_data", "preprocessed.csv")

