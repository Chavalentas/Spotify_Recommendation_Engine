class ValenceCategorizer:
    """Represents the valence categorizer.
    """
    def categorize(self, valence_value: float):
        """Categorizes the valence value (a value between 0 and 1).
        Args:
            valence_value (float): The danceability value (a value between 0 and 1).
        Raises:
            TypeError: Is thrown if valence_value is not a float.
            ValueError: Is thrown if valence_value is less than 0.
            ValueError: Is thrown if valence_value is greater than 1.
            ValueError: Is thrown if valence_value is out of range.
        Returns:
            str: The category of the valence (very negative, negative, positive, very positive).
        """
        if type(valence_value) != float:
            raise TypeError("valence_value must be a float!")
        if valence_value < 0:
            raise ValueError("valence_value cannot be negative!")
        if valence_value > 1:
            raise ValueError("valence_value cannot be greater than 1!")
        
        if valence_value < 0.25:
            return 'very negative'
        
        if valence_value >= 0.25 and valence_value < 0.5:
            return 'negative'
        
        if valence_value >= 0.5 and valence_value < 0.75:
            return 'positive'
        
        if valence_value >= 0.75 and valence_value <= 1:
            return 'very positive'
        
        raise ValueError("valence_value must be within valid range!")
    
    def get_min_inclusive(self, category_name: str) -> float:
        """Gets the minimum value for a given category (inclusive).
        Args:
            category_name (str): The name of the category (very negative, negative, positive, very positive).
        Raises:
            TypeError: Is thrown if category_name is not a str.
            ValueError: Is thrown if invalid category_name is passed.
            ValueError: Is thrown if invalid category_name is passed.
        Returns:
            float: The minimal limit of the range.
        """
        if type(category_name) != str:
            raise TypeError("category_name must be a str!")
        if not(category_name in ['very negative', 'negative', 'positive', 'very positive']):
            raise ValueError("category_name was invalid option!")
        
        if category_name == 'very negative':
            return 0.0
        
        if category_name == 'negative':
            return 0.25
        
        if category_name == 'positive':
            return 0.5
       
        if category_name == 'very positive':
            return 0.75
        
        raise ValueError("Invalid category_name!")
     
    def get_max_exclusive(self, category_name: str) -> float:
        """Gets the maximum value for a given category (exclusive).
        Args:
            category_name (str): The name of the category (very negative, negative, positive, very positive).
        Raises:
            TypeError: Is thrown if category_name is not a str.
            ValueError: Is thrown if invalid category_name is passed.
            ValueError: Is thrown if invalid category_name is passed.
        Returns:
            float: The maximal limit of the range.
        """
        if type(category_name) != str:
            raise TypeError("category_name must be a str!")
        if not(category_name in ['very negative', 'negative', 'positive', 'very positive']):
            raise ValueError("category_name was invalid option!")
        
        if category_name == 'very negative':
            return 0.25
        
        if category_name == 'negative':
            return 0.5
        
        if category_name == 'positive':
            return 0.75
       
        if category_name == 'very positive':
            return 1.01
        
        raise ValueError("Invalid category_name!")