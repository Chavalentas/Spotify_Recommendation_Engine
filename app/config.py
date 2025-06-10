import os
from pathlib import Path
from dataclasses import dataclass

@dataclass
class Config:
    """Represents the configuration dynamically storing all data source paths.
    Attributes:
        project_path (str): The root project path.
        model_path (str): The path to the model.       
        data_frame_path (str): The path to the data.    
    """
    project_path: Path = Path(__file__).resolve().parents[1]

    model_path: Path = project_path.joinpath("app", "model", "model.pkl")
    
    data_frame_path: Path = project_path.joinpath("app", "model", "data.pkl")