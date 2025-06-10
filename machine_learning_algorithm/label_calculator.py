class LabelCalculator:
    """Represents the label calculator.
    """
    def __init__(self):
        """Represents the constructor.
        """
        self.__set_danceability_mapping_dictionary()
        self.__set_mood_mapping_dictionary()
        self.__set_instrumentalness_mapping_dictionary()
        self.__set_energy_mapping_dictionary()
        
    def calculate_label(self, danceability: str, instrumentalness: str, mood: str, energy: str) -> str:
        """Calculates the label based on the given danceability category, instrumentalness category, valence category and energy category.
        Args:
            danceability (str): The danceability category (very undanceable, undanceable, danceable, very danceable).
            instrumentalness (str): The instrumentalness category (very low, low, high, very high).
            mood (str): The valence category (negative, positive).
            energy (str): The energy category (very low, low, high, very high).
        Raises:
            TypeError: Is thrown if danceability is not a str.
            TypeError: Is thrown if instrumentalness is not a str.
            TypeError: Is thrown if mood is not a str.
            TypeError: Is thrown if energy is not a str.
            e: Error message.
        Returns:
            str: The calculated label.
        """
        if type(danceability) != str:
            raise TypeError("danceability must be a str!")
        if type(instrumentalness) != str:
            raise TypeError("instrumentalness must be a str!")
        if type(mood) != str:
            raise TypeError("mood must be a str!")
        if type(energy) != str:
            raise TypeError("energy must be a str!")
        
        try:
            danceability_digit = self.__get_danceability_mapping_digit(danceability)
            instrumentalness_digit = self.__get_instrumentalness_mapping_digit(instrumentalness)
            mood_digit = self.__get_mood_mapping_digit(mood)
            energy_digit = self.__get_energy_mapping_digit(energy)
            result = f"{danceability_digit},{instrumentalness_digit},{mood_digit},{energy_digit}"
            return result
        except Exception as e:
            raise e
        
    def decompose_label(self, label: str) -> dict:
        """Decomposes a label into its categories.
        Args:
            label (str): The label to decompose.
        Raises:
            TypeError: Is thrown if label is not a str.
            ValueError: Is thrown if label cannot be decomposed into 4 categories.
            e: Error message.
        Returns:
            dict: The result dictionary containing the values for the specific categories.
        """
        if type(label) != str:
            raise TypeError("label must be a str!")
        
        try:
            splitted = label.split(",")
            
            if len(splitted) != 4:
                raise ValueError("Invalid label format detected!")
            
            danceability = self.__get_danceability(int(splitted[0]))
            instrumentalness = self.__get_instrumentalness(int(splitted[1]))
            mood = self.__get_mood(int(splitted[2]))
            energy = self.__get_energy(int(splitted[3]))
            return {"danceability": danceability, "instrumentalness": instrumentalness, "mood": mood, "energy":  energy}
        except Exception as e:
            raise e
        
    def __set_mood_mapping_dictionary(self):
        """Sets the valence category mapping dictionary (to a digit).
        """
        self.__mood_dictionary = dict()
        self.__mood_dictionary['very negative'] = 0
        self.__mood_dictionary['negative'] = 1
        self.__mood_dictionary['positive'] = 2
        self.__mood_dictionary['very positive'] = 3
        
    def __set_instrumentalness_mapping_dictionary(self):
        """Sets the instrumentalness category mapping dictionary (to a digit).
        """
        self.__instrumentalness_dictionary = dict()
        self.__instrumentalness_dictionary['very low'] = 0
        self.__instrumentalness_dictionary['low'] = 1
        self.__instrumentalness_dictionary['high'] = 2
        self.__instrumentalness_dictionary['very high'] = 3
        
    def __set_danceability_mapping_dictionary(self):
        """Sets the danceability category mapping dictionary (to a digit).
        """
        self.__danceability_mapping_dictionary = dict()
        self.__danceability_mapping_dictionary['very undanceable'] = 0
        self.__danceability_mapping_dictionary['undanceable'] = 1
        self.__danceability_mapping_dictionary['danceable'] = 2
        self.__danceability_mapping_dictionary['very danceable'] = 3    
        
    def __set_energy_mapping_dictionary(self):
        """Sets the energy category mapping dictionary (to a digit).
        """
        self.__energy_mapping_dictionary = dict()
        self.__energy_mapping_dictionary['very low'] = 0
        self.__energy_mapping_dictionary['low'] = 1
        self.__energy_mapping_dictionary['high'] = 2
        self.__energy_mapping_dictionary['very high'] = 3
        
    def __get_mood_mapping_digit(self, mood: str) -> int:
        """Returns the mapping digit for the given valence category.
        Args:
            mood (str): The valence category.
        Raises:
            TypeError: Is thrown if mood is not a str.
            e: Error message.
        Returns:
            int: The mapping digit.
        """
        if type(mood) != str:
            raise TypeError("mood must be str!")
        
        try:
            return self.__mood_dictionary[mood]
        except Exception as e:
            raise e
        
    def __get_mood(self, digit: int) -> str:
        """Returns the valence category based on the digit.
        Args:
            digit (int): The mapping digit.
        Raises:
            TypeError: Is thrown if digit is not an int.
            ValueError: Is thrown if an invalid digit is detected.
            e: Error message.
        Returns:
            str: The valence category.
        """
        if type(digit) != int:
            raise TypeError("digit must be an int!")
        
        try:
            for k, v in self.__mood_dictionary.items():
                if v == digit:
                    return k
                
            raise ValueError("Invalid digit detected!")
        except Exception as e:
            raise e
        
    def __get_instrumentalness_mapping_digit(self, instrumentalness: str) -> int:
        """Returns the mapping digit for the given instrumentalness category.
        Args:
            instrumentalness (str): The instrumentalness category.
        Raises:
            TypeError: Is thrown if instrumentalness is not a str.
            e: Error message.
        Returns:
            int: The mapping digit.
        """
        if type(instrumentalness) != str:
            raise TypeError("instrumentalness must be str!")
        
        try:
            return self.__instrumentalness_dictionary[instrumentalness]
        except Exception as e:
            raise e
        
    def __get_instrumentalness(self, digit: int) -> str:
        """Returns the instrumentalness category based on the digit.
        Args:
            digit (int): The mapping digit.
        Raises:
            TypeError: Is thrown if digit is not an int.
            ValueError: Is thrown if an invalid digit is detected.
            e: Error message.
        Returns:
            str: The instrumentalness category.
        """
        if type(digit) != int:
            raise TypeError("digit must be an int!")
        
        try:
            for k, v in self.__instrumentalness_dictionary.items():
                if v == digit:
                    return k
                
            raise ValueError("Invalid digit detected!")
        except Exception as e:
            raise e
        
    def __get_danceability_mapping_digit(self, danceability: str) -> int:
        """Returns the mapping digit for the given danceability category.
        Args:
            danceability (str): The danceability category.
        Raises:
            TypeError: Is thrown if danceability is not a str.
            e: Error message.
        Returns:
            int: The mapping digit.
        """
        if type(danceability) != str:
            raise TypeError("Danceability must be str!")
        
        try:
            return self.__danceability_mapping_dictionary[danceability]
        except Exception as e:
            raise e
        
    def __get_danceability(self, digit: int) -> str:
        """Returns the danceability category based on the digit.
        Args:
            digit (int): The mapping digit.
        Raises:
            TypeError: Is thrown if digit is not an int.
            ValueError: Is thrown if an invalid digit is detected.
            e: Error message.
        Returns:
            str: The danceability category.
        """
        if type(digit) != int:
            raise TypeError("digit must be an int!")
        
        try:
            for k, v in self.__danceability_mapping_dictionary.items():
                if v == digit:
                    return k
                
            raise ValueError("Invalid digit detected!")
        except Exception as e:
            raise e
        
    def __get_energy_mapping_digit(self, energy: str) -> int:
        """Returns the mapping digit for the given energy category.
        Args:
            energy (str): The energy category.
        Raises:
            TypeError: Is thrown if energy is not a str.
            e: Error message.
        Returns:
            int: The mapping digit.
        """
        if type(energy) != str:
            raise TypeError("energy must be str!")
        
        try:
            return self.__energy_mapping_dictionary[energy]
        except Exception as e:
            raise e
        
    def __get_energy(self, digit: int) -> str:
        """Returns the energy category based on the digit.
        Args:
            digit (int): The mapping digit.
        Raises:
            TypeError: Is thrown if digit is not an int.
            ValueError: Is thrown if an invalid digit is detected.
            e: Error message.
        Returns:
            str: The energy category.
        """
        if type(digit) != int:
            raise TypeError("digit must be an int!")
        
        try:
            for k, v in self.__energy_mapping_dictionary.items():
                if v == digit:
                    return k
                
            raise ValueError("Invalid digit detected!")
        except Exception as e:
            raise e