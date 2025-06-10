import pandas as pd

class FrameFilter:
    """Represents the frame filter.
    """
    @staticmethod
    def apply_range_filter(frame: pd.DataFrame, criterion_min_max_tuples: list) -> pd.DataFrame:
        """Applies the range filter (>=, <=).
        Args:
            frame (pd.DataFrame): The input data frame.
            criterion_min_max_tuples (list): List of the range filter tuples (e.g. [("danceability", (0, 0.5)) ,...]).
        Raises:
            TypeError: Is thrown if frame is not a pd.DataFrame.
            TypeError: Is thrown if criterion_min_max_tuples is not a list.
            TypeError: Is thrown if criterion_min_max_tuples does not consist of tuples.
            TypeError: Is thrown if criterion_min_max_tuples does not consist of tuples of length 2.
            TypeError: Is thrown if the tuple format is incorrect (correct format, e.g. ("danceability", (0, 0.5)) => danceability between 0 and 0.5).
            TypeError: Is thrown if the tuple format is incorrect (correct format, e.g. ("danceability", (0, 0.5)) => danceability between 0 and 0.5).
            TypeError: Is thrown if the tuple format is incorrect (correct format, e.g. ("danceability", (0, 0.5)) => danceability between 0 and 0.5).
            TypeError: Is thrown if the tuple format is incorrect (correct format, e.g. ("danceability", (0, 0.5)) => danceability between 0 and 0.5).
            e: Error message.
        Returns:
            pd.DataFrame: The filtered frame.
        """
        if type(frame) != pd.DataFrame:
            raise TypeError("frame must be a pandas DataFrame!")
        if type(criterion_min_max_tuples) != list:
            raise TypeError("criterion_min_max_tuples must be a list!")
        if len(criterion_min_max_tuples) == 0:
            return frame
        if not(all([type(el) == tuple for el in criterion_min_max_tuples])):
            raise TypeError("criterion_min_max_tuples must consist of tuples!")
        
        for t in criterion_min_max_tuples:
            if len(t) != 2:
                raise TypeError("criterion_min_max_tuples must be of length 2!")
            if type(t[0]) != str:
                raise TypeError("The first element of all tuples must be string!")
            if type(t[1]) != tuple and len(t[1]) != 2:
                raise TypeError("The second element of all tuples must be (min,max)!")
            if not(type(t[1][0]) == int or type(t[1][0]) == float):
                raise TypeError("Min value must be either int or float!")
            if not(type(t[1][1]) == int or type(t[1][1]) == float):
                raise TypeError("Max value must be either int or float!")       
        
        try:
            result = pd.DataFrame(frame)
            
            for t in criterion_min_max_tuples:
                criterion_name = t[0]
                criterion_min_val = t[1][0]
                criterion_max_val = t[1][1]
                result = result[(result[criterion_name] >= criterion_min_val) & (result[criterion_name] <= criterion_max_val)]
            return result
        except Exception as e:
            raise e
        
    @staticmethod
    def apply_equality_filter(frame: pd.DataFrame, criterion_value_tuples: list) -> pd.DataFrame:
        """Applies the equality filter (==).
        Args:
            frame (pd.DataFrame): The input data frame.
            criterion_value_tuples (list): List of the equality filter tuples (e.g. [("danceability", 0.2) ,...]).
        Raises:
            TypeError: Is thrown if frame is not a pd.DataFrame.
            TypeError: Is thrown if criterion_value_tuples is not a list.
            TypeError: Is thrown if criterion_value_tuples does not consist of tuples.
            TypeError: Is thrown if criterion_value_tuples does not consist of tuples of length 2.
            TypeError: Is thrown if first element of criterion_value_tuples tuples is not a str.
            e: Error message.
        Returns:
            pd.DataFrame: The filtered frame.
        """
        if type(frame) != pd.DataFrame:
            raise TypeError("frame must be a pandas DataFrame!")
        if type(criterion_value_tuples) != list:
            raise TypeError("criterion_value_tuples must be a list!")
        if len(criterion_value_tuples) == 0:
            return frame
        if not(all([type(el) == tuple for el in criterion_value_tuples])):
            raise TypeError("criterion_value_tuples must consist of tuples!")
        
        for t in criterion_value_tuples:
            if len(t) != 2:
                raise TypeError("criterion_min_max_tuples must be of length 2!")
            if type(t[0]) != str:
                raise TypeError("The first element of all tuples must be string!")   
        
        try:
            result = pd.DataFrame(frame)
            
            for t in criterion_value_tuples:
                criterion_name = t[0]
                equal_value = t[1]
                result = result[result[criterion_name] == equal_value]
            return result
        except Exception as e:
            raise e
        
        
        