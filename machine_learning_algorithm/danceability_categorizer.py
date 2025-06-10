class DanceabilityCategorizer:
    """Represents the danceability rule-based classifier.
    """
    def categorize(self, danceability_value: float) -> str:
        """Categorizes the danceability value (a value between 0 and 1).
        Args:
            danceability_value (float): The danceability value (a value between 0 and 1).
        Raises:
            TypeError: Is thrown if danceability_value is not a float.
            ValueError: Is thrown if danceability_value is less than 0.
            ValueError: Is thrown if danceability_value is greater than 1.
            ValueError: Is thrown if danceability_value is out of range.
        Returns:
            str: The category of the danceability (very undanceable, undanceable, danceable, very danceable).
        """
        if type(danceability_value) != float:
            raise TypeError("danceability_value must be a float!")
        if danceability_value < 0:
            raise ValueError("danceability_value cannot be negative!")
        if danceability_value > 1:
            raise ValueError("danceability_value cannot be greater than 1!")
        
        if danceability_value < 0.25:
            return 'very undanceable'
        
        if danceability_value >= 0.25 and danceability_value < 0.5:
            return 'undanceable'
        
        if danceability_value >= 0.5 and danceability_value < 0.75:
            return 'danceable'
        
        if danceability_value >= 0.75 and danceability_value <= 1:
            return 'very danceable'
        
        raise ValueError("danceability_value must be within valid range!")
    
    def get_min_inclusive(self, category_name: str) -> float:
        """Gets the minimum value for a given category (inclusive).
        Args:
            category_name (str): The name of the category (very undanceable, undanceable, danceable or very danceable).
        Raises:
            TypeError: Is thrown if category_name is not a str.
            ValueError: Is thrown if invalid category_name is passed.
            ValueError: Is thrown if invalid category_name is passed.
        Returns:
            float: The minimal limit of the range.
        """
        if type(category_name) != str:
            raise TypeError("category_name must be a str!")
        if not(category_name in ['very undanceable', 'undanceable', 'danceable', 'very danceable']):
            raise ValueError("category_name was invalid option!")
        
        if category_name == 'very undanceable':
            return 0.0
        
        if category_name == 'undanceable':
            return 0.25
        
        if category_name == 'danceable':
            return 0.5
       
        if category_name == 'very danceable':
            return 0.75
        
        raise ValueError("Invalid category_name!")
     
    def get_max_exclusive(self, category_name: str) -> float:
        """Gets the maximum value for a given category (exclusive).
        Args:
            category_name (str): The name of the category (very undanceable, undanceable, danceable or very danceable).
        Raises:
            TypeError: Is thrown if category_name is not a str.
            ValueError: Is thrown if invalid category_name is passed.
            ValueError: Is thrown if invalid category_name is passed.
        Returns:
            float: The maximal limit of the range.
        """
        if type(category_name) != str:
            raise TypeError("category_name must be a str!")
        if not(category_name in ['very undanceable', 'undanceable', 'danceable', 'very danceable']):
            raise ValueError("category_name was invalid option!")
        
        if category_name == 'very undanceable':
            return 0.25
        
        if category_name == 'undanceable':
            return 0.5
        
        if category_name == 'danceable':
            return 0.75
       
        if category_name == 'very danceable':
            return 1.01
        
        raise ValueError("Invalid category_name!")