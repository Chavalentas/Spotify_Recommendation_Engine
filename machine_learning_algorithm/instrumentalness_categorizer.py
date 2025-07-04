class InstrumentalnessCategorizer:
    """Represents the instrumentalness rule-based classifier.
    """
    def categorize(self, instrumentalness_value: float) -> str:
        """Categorizes the instrumentalness value (a value between 0 and 1).
        Args:
            instrumentalness_value (float): The energy value (a value between 0 and 1).
        Raises:
            TypeError: Is thrown if instrumentalness_value is not a float.
            ValueError: Is thrown if instrumentalness_value is less than 0.
            ValueError: Is thrown if instrumentalness_value is greater than 1.
            ValueError: Is thrown if instrumentalness_value is out of range.
        Returns:
            str: The category of the instrumentalness (very low, low, high, very high).
        """
        if type(instrumentalness_value) != float:
            raise TypeError("instrumentalness_value must be a float!")
        if instrumentalness_value < 0:
            raise ValueError("instrumentalness_value cannot be negative!")
        if instrumentalness_value > 1:
            raise ValueError("instrumentalness_value cannot be greater than 1!")
        
        if instrumentalness_value < 0.25:
            return 'very low'
        
        if instrumentalness_value >= 0.25 and instrumentalness_value < 0.5:
            return 'low'
        
        if instrumentalness_value >= 0.5 and instrumentalness_value < 0.75:
            return 'high'
        
        if instrumentalness_value >= 0.75 and instrumentalness_value <= 1:
            return 'very high'
        
        raise ValueError("instrumentalness_value must be within valid range!")
    
    def get_min_inclusive(self, category_name: str) -> float:
        """Gets the minimum value for a given category (inclusive).
        Args:
            category_name (str): The name of the category (very low, low, high or very high).
        Raises:
            TypeError: Is thrown if category_name is not a str.
            ValueError: Is thrown if invalid category_name is passed.
            ValueError: Is thrown if invalid category_name is passed.
        Returns:
            float: The minimal limit of the range.
        """
        if type(category_name) != str:
            raise TypeError("category_name must be a str!")
        if not(category_name in ['very low', 'low', 'high', 'very high']):
            raise ValueError("category_name was invalid option!")
        
        if category_name == 'very low':
            return 0.0
        
        if category_name == 'low':
            return 0.25
        
        if category_name == 'high':
            return 0.5
       
        if category_name == 'very high':
            return 0.75
        
        raise ValueError("Invalid category_name!")
     
    def get_max_exclusive(self, category_name: str) -> float:
        """Gets the maximum value for a given category (exclusive).
        Args:
            category_name (str): The name of the category (very low, low, high or very high).
        Raises:
            TypeError: Is thrown if category_name is not a str.
            ValueError: Is thrown if invalid category_name is passed.
            ValueError: Is thrown if invalid category_name is passed.
        Returns:
            float: The maximal limit of the range.
        """
        if type(category_name) != str:
            raise TypeError("category_name must be a str!")
        if not(category_name in ['very low', 'low', 'high', 'very high']):
            raise ValueError("category_name was invalid option!")
        
        if category_name == 'very low':
            return 0.25
        
        if category_name == 'low':
            return 0.5
        
        if category_name == 'high':
            return 0.75
       
        if category_name == 'very high':
            return 1.01
        
        raise ValueError("Invalid category_name!")