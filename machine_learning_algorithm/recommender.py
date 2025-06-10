import pandas as pd
from danceability_categorizer import DanceabilityCategorizer
from energy_categorizer import EnergyCategorizer
from instrumentalness_categorizer import InstrumentalnessCategorizer
from valence_categorizer import ValenceCategorizer

class Recommender:
    """Represents the recommender.
    """
    def __init__(self):
        """Represents the constructor.
        """
        self.__danceability_categorizer = DanceabilityCategorizer()
        self.__energy_categorizer = EnergyCategorizer()
        self.__instrumentalness_categorizer = InstrumentalnessCategorizer()
        self.__valence_categorizer = ValenceCategorizer()
        
    def recommend(self, danceability_category: str, mood: str, energy_category: str, instrumentalness_category: str, input_frame: pd.DataFrame) -> pd.DataFrame:
        """ Recommends tracks from the given frame based on the passed categories.
        Args:
            danceability_category (str): The danceability category (very undanceable, undanceable, danceable, very danceable).
            mood (str): The valence category (very negative, negative, positive, very positive).
            energy_category (str): The energy category (very low, low, high, very high).
            instrumentalness_category (str): The instrumentalness category (very low, low, high, very high).
            input_frame (pd.DataFrame): The input data frame.
        Raises:
            TypeError: Is thrown if danceability_category is not a str.
            TypeError: Is thrown if mood is not a str.
            TypeError: Is thrown if energy_category is not a str.
            TypeError: Is thrown if instrumentalness_category is not a str.
            TypeError: Is thrown if input_frame is not a pd.DataFrame.
            e: Error message.
        Returns:
            pd.DataFrame: A data frame consisting of recommended tracks.
        """
        if type(danceability_category) != str:
            raise TypeError("danceability_category is not a str!")
        if type(mood) != str:
            raise TypeError("mood is not a str!")
        if type(energy_category) != str:
            raise TypeError("energy_category is not a str!")
        if type(instrumentalness_category) != str:
            raise TypeError("instrumentalness_category is not a str!")
        if type(input_frame) != pd.DataFrame:
            raise TypeError("input_frame must is not a pd.DataFrame!")
        
        try:
            danceability_min_incl = self.__danceability_categorizer.get_min_inclusive(danceability_category)
            danceability_max_excl = self.__danceability_categorizer.get_max_exclusive(danceability_category)
            energy_min_incl = self.__energy_categorizer.get_min_inclusive(energy_category)
            energy_max_excl = self.__energy_categorizer.get_max_exclusive(energy_category)  
            instrumentalness_min_incl = self.__instrumentalness_categorizer.get_min_inclusive(instrumentalness_category)
            instrumentalness_max_excl = self.__instrumentalness_categorizer.get_max_exclusive(instrumentalness_category)  
            valence_min_incl = self.__valence_categorizer.get_min_inclusive(mood)
            valence_max_excl = self.__valence_categorizer.get_max_exclusive(mood)
            danceability_condition = ((input_frame['danceability'] >= danceability_min_incl) & (input_frame['danceability'] < danceability_max_excl))
            energy_condition = ((input_frame['energy'] >= energy_min_incl) & (input_frame['energy'] < energy_max_excl))
            instrumentalness_condition = ((input_frame['instrumentalness'] >= instrumentalness_min_incl) & (input_frame['instrumentalness'] < instrumentalness_max_excl))
            valence_condition = ((input_frame['valence'] >= valence_min_incl) & (input_frame['valence'] < valence_max_excl))
            result = input_frame[danceability_condition & energy_condition & instrumentalness_condition & valence_condition]
            return result
        except Exception as e:
            raise e
        
        
        
        