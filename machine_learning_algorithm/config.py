import os
from pathlib import Path
from dataclasses import dataclass

@dataclass
class Config:
    """Represents the configuration dynamically storing all data source paths.
    Attributes:
        project_path (str): The root project path.
        preprocessed_data_path (str): The path leading to the CSV file containing information about the preprocessed data.   
        model_path (str): The path to the model.       
        data_frame_path (str): The path to the data.       
        colors_path (str): The path leading to the CSV file containing the color codes.
    """
    project_path: Path = Path(__file__).resolve().parents[1]
    
    preprocessed_data_path: Path = project_path.joinpath("spotify_data", "preprocessed.csv")
    
    model_path: Path = project_path.joinpath("app", "model", "model.pkl")
    
    data_frame_path: Path = project_path.joinpath("app", "model", "data.pkl")
    
    colors_path: Path = project_path.joinpath("machine_learning_algorithm", "color_codes.csv")

