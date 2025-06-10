#--------------------------------------------Code--------------------------------------------
import sys
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.express as px
import pickle
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'machine_learning_algorithm'))
from machine_learning_algorithm.danceability_categorizer import DanceabilityCategorizer
from machine_learning_algorithm.recommender import Recommender
from machine_learning_algorithm.label_calculator import LabelCalculator
from config import Config
sys.path.append("..")
from model.frame_filter import FrameFilter
from model.track import Track
from sklearn.neighbors import KNeighborsClassifier
config = Config()

def create_state_key_if_not_exists(state_key, init_value):
    """Creates a state key it it does not exist.
    Args:
        state_key (_type_): The state key.
        init_value (_type_): The initial value that is set at the beginning.
    """
    if state_key not in st.session_state:
        st.session_state[state_key] = init_value
        
def on_get_recommendations_click(*args):
    """Is executed when the "Get recommendations" button is clicked.
    """
    track_id = args[0]
    st.session_state["search_bar_value"] = ""
    st.session_state["recommendations_search_enabled"] = True
    st.session_state["searching_mode_value"] = "Recommendations"
    recommendations = get_recommendations(track_id, 'id', st.session_state["data_frame"],
                                          st.session_state["model"], recommender, label_calculator)
    st.session_state["recommendations_frame"] = recommendations
    reload_data()

def on_turn_off_recommendations_request():
    """Is executed when the "Turn off recommendations" button is clicked.
    """
    st.session_state["recommendations_search_enabled"] = False
    st.session_state["searching_mode_value"] = "Main (recommendations deactivated)"
    reload_data()
    
def reload_data():
    """Reloads data.
    """
    st.session_state["page_count"] = 0
    st.session_state["paginator_left_value"] = 0
    st.session_state["paginator_right_value"] = 10
    refilter_data()
    
def refilter_data():
    """Refilters data.
    """
    df = st.session_state["data_frame"]
    result = apply_criteria(df, st.session_state["criteria_values"])
    genrey_key = get_genre(st.session_state["selected_genre"])
    result = apply_genre(result, "track_genre", genrey_key)
    result = apply_search_bar_value(result, st.session_state["search_bar_value"],
                                               "artists_name", "name")
    
    if st.session_state["recommendations_search_enabled"]:
        recommended_values = st.session_state["recommendations_frame"]
        result = result[result["id"].isin(recommended_values["id"])]
        
    st.session_state["currently_displayed_frame"] = result
    
def apply_criteria(input_frame: pd.DataFrame, criteria_values_dict: dict) -> pd.DataFrame:
    """Applies criteria to the input frame.
    Args:
        input_frame (pd.DataFrame): The input frame.
        criteria_values_dict (dict): The dictionary containing criteria value ranges (the format can be seen in get_range_selection_criterion_values_dictionary()).
    Raises:
        TypeError: Is thrown if input_frame is not a pd.DataFrame.
        TypeError: Is thrown if criteria_values_dict is not a dict.
    Returns:
        pd.DataFrame: The filtered data frame.
    """
    if type(input_frame) != pd.DataFrame:
        raise TypeError("input_frame must be a pd.DataFrame!")
    if type(criteria_values_dict) != dict:
        raise TypeError("criteria_values_dict must be a dict!") 
    
    df = pd.DataFrame(input_frame)
    filter_list = [(key, st.session_state[key]) for key in criteria_values_dict.keys()]
    result = FrameFilter.apply_range_filter(df, filter_list)
    return result

def apply_genre(input_frame: pd.DataFrame, frame_genre_attribute: str, genre_key: str) -> pd.DataFrame:
    """Applies the genre filter.
    Args:
        input_frame (pd.DataFrame): The input data frame.
        frame_genre_attribute (str): The name of the genre attribute.
        genre_key (str): The genre value.
    Raises:
        TypeError: Is thrown if input_frame is not a pd.DataFrame.
        TypeError: Is thrown if frame_genre_attribute is not a str.
        TypeError: Is thrown if genre_key is not a str.
    Returns:
        pd.DataFrame: The filtered data frame.
    """
    if type(input_frame) != pd.DataFrame:
        raise TypeError("input_frame must be a pd.DataFrame!")
    if type(frame_genre_attribute) != str:
        raise TypeError("frame_genre_attribute must be a str!")
    if type(genre_key) != str:
        raise TypeError("genre_key must be a str!")
    
    if genre_key == "all":
        return input_frame

    result = FrameFilter.apply_equality_filter(input_frame, [(frame_genre_attribute, genre_key)])
    return result

def apply_search_bar_value(input_frame: pd.DataFrame, search_value: str, artists_name_attribute: str, track_name_attribute: str) -> pd.DataFrame:
    """Applies the search bar value filter to the input frame.
    Args:
        input_frame (pd.DataFrame): The input frame.
        search_value (str): The search bar value.
        artists_name_attribute (str): The name of the artists name attribute.
        track_name_attribute (str): The name of the track name attribute.
    Raises:
        TypeError: Is thrown if input_frame is not a pd.DataFrame.
        TypeError: Is thrown if search_value is not a str.
        TypeError: Is thrown if artist_name_attribute is not a str.
        TypeError: Is thrown if track_name_attribute is not a str.
    Returns:
        pd.DataFrame: The result data frame.
    """
    if type(input_frame) != pd.DataFrame:
        raise TypeError("input_frame must be a pd.DataFrame!")
    if type(search_value) != str:
        raise TypeError("search_value must be a str!")
    if type(artists_name_attribute) != str:
        raise TypeError("artists_name_attribute must be a str!")
    if type(track_name_attribute) != str:
        raise TypeError("track_name_attribute must be a str!")
    if search_value == "" or search_value == None:
        return input_frame
    
    df_artists = get_data_frame_by_artist(input_frame, search_value, artists_name_attribute)
    df_tracks = get_data_frame_by_track_name(input_frame, search_value, track_name_attribute)
    result = pd.concat([df_artists, df_tracks])
    return result.drop_duplicates(subset=["id"])

def get_recommendations(track_id: str, id_attribute: str, input_frame: pd.DataFrame, knn_classifier: KNeighborsClassifier,
                        recommender: Recommender, label_calculator: LabelCalculator) -> pd.DataFrame:
    """Retrieves recommendations based on the input parameters.
    Args:
        track_id (str): The input track ID.
        id_attribute (str): The name of the track id attribute.
        input_frame (pd.DataFrame): The input frame.
        knn_classifier (KNeighborsClassifier): The KNN classifier.
        recommender (Recommender): The recommender.
        label_calculator (LabelCalculator): The label calculator.

    Raises:
        TypeError: Is thrown if track_id is not a str.
        TypeError: Is thrown if id_attribute is not a str.
        TypeError: Is thrown if input_frame is not a pd.DataFrame.
        TypeError: Is thrown if knn_classifier is not a KNeighborsClassifier.
        TypeError: Is thrown if recommender is not a Recommender.
        TypeError: Is thrown if label_calculator is not a LabelCalculator.
    Returns:
        pd.DataFrame: The recommendations data frame.
    """
    if type(track_id) != str:
        raise TypeError("track_id must be a str!")
    if type(id_attribute) != str:
        raise TypeError("id_attribute must be a str!")
    if type(input_frame) != pd.DataFrame:
        raise TypeError("input_frame must be a pd.DataFrame!")
    if type(knn_classifier) != KNeighborsClassifier:
        raise TypeError("knn_classifier must be a KNeighborsClassifier!")
    if type(recommender) != Recommender:
        raise TypeError("recommender must be of type Recommender!")
    if type(label_calculator) != LabelCalculator:
        raise TypeError("label_calculator must be of type LabelCalculator!")
    
    frame = pd.DataFrame(input_frame)
    correct_row = frame[frame[id_attribute] == track_id].iloc[0][['danceability', 'valence', 'instrumentalness', 'energy']]
    input_array = np.array(correct_row)
    label = knn_classifier.predict([input_array])
    label_decomposed = label_calculator.decompose_label(label[0])
    recommended = recommender.recommend(label_decomposed["danceability"], label_decomposed["mood"],
                                        label_decomposed["energy"], 
                                        label_decomposed["instrumentalness"],
                                        input_frame)
    return recommended
    
    
def get_data_frame_by_artist(input_frame: pd.DataFrame, search_str: str, artists_name_attribute: str) -> pd.DataFrame:
    """Filters data frame by looking for artists containing the search_str.
    Args:
        input_frame (pd.DataFrame): The input data frame.
        search_str (str): The search string.
        artists_name_attribute (str): The name of the artists attribute.
    Raises:
        TypeError: Is thrown if input_frame is not a pd.DataFrame:
        TypeError: Is thrown if search_str is not a str.
        TypeError: Is thrown if artists_name_attribute is not a str.
    Returns:
        pd.DataFrame: The filtered data frame.
    """
    if type(input_frame) != pd.DataFrame:
        raise TypeError("input_frame must be a pd.DataFrame!")
    if type(search_str) != str:
        raise TypeError("search_str must be a str!")
    if type(artists_name_attribute) != str:
        raise TypeError("artists_name_attribute must be a str!")
    
    frame = pd.DataFrame(input_frame)
    subframe = frame[frame[artists_name_attribute].apply(lambda artists_list: any([search_str.lower().replace(" ", "") in str(el).lower().replace(" ", "") for el in artists_list]))]
    return subframe

def get_data_frame_by_track_name(input_frame: pd.DataFrame, search_str: str, track_name_attribute: str) -> pd.DataFrame:
    """Filters data frame by looking for tracks containing the search_str.
    Args:
        input_frame (pd.DataFrame): The input data frame.
        search_str (str): The search string.
        track_name_attribute (str): The name of the track name attribute.
    Raises:
        TypeError: Is thrown if input_frame is not a pd.DataFrame:
        TypeError: Is thrown if search_str is not a str.
        TypeError: Is thrown if track_name_attribute is not a str.
    Returns:
        pd.DataFrame: The filtered data frame.
    """
    if type(input_frame) != pd.DataFrame:
        raise TypeError("input_frame must be a pd.DataFrame!")
    if type(search_str) != str:
        raise TypeError("search_str must be a str!")
    if type(track_name_attribute) != str:
        raise TypeError("track_name_attribute must be a str!")
    
    frame = pd.DataFrame(input_frame)
    subframe = frame[frame[track_name_attribute].apply(lambda track: search_str.lower().replace(" ", "") in str(track).lower().replace(" ", ""))]
    return subframe
    

def on_paginator_right():
    """Is executed when the right paginator is clicked.
    """
    data_frame = pd.DataFrame(st.session_state["currently_displayed_frame"])
    current_right = st.session_state["paginator_right_value"]
    
    if current_right > len(data_frame):
        return
    
    st.session_state["paginator_left_value"] = current_right
    st.session_state["paginator_right_value"] = current_right + st.session_state["paginator_step"]
    st.session_state["page_count"] += 1
    refilter_data()

def on_paginator_left():
    """Is executed when the left paginator is clicked.
    """
    current_left = st.session_state["paginator_left_value"]
    
    if current_left == 0:
        return
    
    st.session_state["paginator_right_value"] = current_left
    st.session_state["paginator_left_value"] = current_left - st.session_state["paginator_step"]
    st.session_state["page_count"] -= 1
    refilter_data()
    
def get_genre_to_key_mapping_dictionary() -> dict:
    """Gets genre-to-key mapping dictionary.
    Returns:
        dict: The mapping dictionary.
    """
    result_dict = {
        "**All**" : "all",
        "Avant-garde": "avant-garde",
         "Blues": "blues",
         "Country": "country",
         "Easy listening": "easy listening",
         "Electronic": "electronic",
         "Experimental": "experimental",
         "Folk": "folk",
         "Hip Hop": "hip hop",
         "Jazz": "jazz",
         "Metal": "metal",
         "Pop": "pop",
         "Punk": "punk",
         "R&B": "r&b",
         "Rap": "rap",
         "Rock": "rock",
         "Soul": "soul"
    }
    
    return result_dict

def get_range_selection_criterion_limits_dictionary() -> dict:
    """Gets the dictionary that expresses possible value ranges for criteria.
    Returns:
        dict: The mapping dictionary.
    """
    result_dict = {
        "danceability": (0.0, 1.0),
        "instrumentalness": (0.0, 1.0),
        "energy": (0.0, 1.0),
        "valence": (0.0, 1.0)
    }
    
    return result_dict


def get_range_selection_criterion_values_dictionary() -> dict:
    """Gets the dictionary that expresses current limits set in the possible limit range.
    Returns:
        dict: The mapping dictionary.
    """
    result_dict = {
        "danceability": (0.0, 1.0),
        "instrumentalness": (0.0, 1.0),
        "energy": (0.0, 1.0),
        "valence": (0.0, 1.0)
    }
    
    return result_dict

def get_genre(display_str: str):
    """Gets the genre associated with the display string.
    Args:
        display_str (str): The display string.
    Raises:
        TypeError: Is thrown if display_str is not a str.
    Returns:
        _type_: Value behind the key.
    """
    if type(display_str) != str:
        raise TypeError("display_str must be a str!")
    
    dictionary = get_genre_to_key_mapping_dictionary()
    return dictionary[display_str]

def get_list_textual_representation(input_list: list, empty_text: str, separator: str) -> str:
    """Returns a textual representation of a list.
    Args:
        input_list (list): The input list.
        empty_text (str): Value to return if input_list is empty.
        separator (str): The separator to use when separating input_list.
    Raises:
        TypeError: Is thrown if input_list is not a list.
        TypeError: Is thrown if empty_text is not a str.
        TypeError: Is thrown if separator is not a str.
    Returns:
        str: The result textual representation.
    """
    if type(input_list) != list:
        raise TypeError("input_list must be a list!")
    if type(empty_text) != str:
        raise TypeError("empty_text must be a str!")
    if type(separator) != str:
        raise TypeError("separator must be a str!")
    
    if len(input_list) == 0:
        return empty_text
    
    return separator.join(input_list)

def get_string_textual_representation(input_str: str, empty_text: str) -> str:
    """Returns a textual representation of a string.
    Args:
        input_str (str): The input string.
        empty_text (str): Value to return if input_str is empty.
    Raises:
        TypeError: Is thrown if input_str is not a string.
        TypeError: Is thrown if empty_text is not a string.
    Returns:
        str: The result textual representation.
    """
    if type(input_str) != str:
        raise TypeError("input_str must be a str!")
    if type(empty_text) != str:
        raise TypeError("empty_text must be a str!")
    
    if len(input_str) == 0:
        return empty_text
    
    return input_str

def get_radar_chart(r_values: list, theta_values: list, width: int, height: int):
    """Returns a radar chart.
    Args:
        r_values (list): Attributes to display.
        theta_values (list): Attribute names.
        width (int): Chart width.
        height (int): Chart height.
    Raises:
        TypeError: Is thrown if r_values is not a list.
        TypeError: Is thrown if theta_values is not a list.
        TypeError: Is thrown if width is not an int.
        TypeError: Is thrown if height is not an int.
        ValueError: Is thrown if height is negative.
        ValueError: Is thrown if widh is negative.
    Returns:
        _type_: The result plot.
    """
    if type(r_values) != list:
        raise TypeError("r_values must be a list!")
    if type(theta_values) != list:
        raise TypeError("theta_values must be a list!")
    if type(width) != int:
        raise TypeError("width must ne an int!")
    if type(height) != int:
        raise TypeError("height must be an int!")
    if height < 0:
        raise ValueError("height cannot be negative!")
    if width < 0:
        raise ValueError("width cannot be negative!")
    
    df = pd.DataFrame(dict(
        r=r_values,
        theta=theta_values
    ))
    
    fig = px.line_polar(df, r='r', theta='theta', line_close=True, width=width, height=height)
    return fig
    
# Helper variables/objects
genres_to_select_to_keys = get_genre_to_key_mapping_dictionary()
criteria_values = get_range_selection_criterion_values_dictionary()
criteria_limits = get_range_selection_criterion_limits_dictionary()
label_calculator = LabelCalculator()
recommender = Recommender()

def create_session():
    """Creates a session.
    """
    create_state_key_if_not_exists("selected_genre", "**All**")
    create_state_key_if_not_exists("genres_to_select", genres_to_select_to_keys.keys())
    create_state_key_if_not_exists("criteria_limits", criteria_limits)
    create_state_key_if_not_exists("criteria_values", criteria_values)
    create_state_key_if_not_exists("data_frame", pd.DataFrame())
    create_state_key_if_not_exists("currently_displayed_frame", pd.DataFrame())
    create_state_key_if_not_exists("model", None)
    create_state_key_if_not_exists("paginator_left_value", 0)
    create_state_key_if_not_exists("paginator_right_value", 10)
    create_state_key_if_not_exists("paginator_step", 10)
    create_state_key_if_not_exists("page_count", 0)
    create_state_key_if_not_exists("searching_mode_value", "Main (recommendations deactivated)")
    create_state_key_if_not_exists("search_bar_value", "")
    create_state_key_if_not_exists("init_load", True)
    create_state_key_if_not_exists("recommendations_search_enabled", False)
    create_state_key_if_not_exists("recommendations_frame", pd.DataFrame())
    
@st.cache_data  
def get_data():
    """Gets the data frame used in the application.
    Returns:
        _type_: The data frame.
    """
    st.session_state["data_frame"] = pickle.load(open(config.data_frame_path, "rb"))
    return st.session_state["data_frame"]

@st.cache_data  
def get_model():
    """Gets the model used to create the predictions.
    Returns:
        _type_: The model.
    """
    st.session_state["model"] = pickle.load(open(config.model_path, "rb"))
    return st.session_state["model"] 

def get_display_information(input_frame: pd.DataFrame) -> list:
    """Gets a list of track information used to display the data.
    Args:
        input_frame (pd.DataFrame): The input data frame.
    Returns:
        list: List of data to display.
    """
    display_frame = pd.DataFrame(input_frame)
    data_excerpt = display_frame[['id', 'name', 'danceability', 'instrumentalness', 'energy', 'valence', 'artists_name']]
    data_excerpt_list = list(data_excerpt.itertuples(index=False, name=None))
    data_list = [Track(el[0], get_string_textual_representation(el[1], "unknown"), el[2], el[3], el[4], el[5], 
                       get_list_textual_representation(el[6], "unknown", ",")) for el in data_excerpt_list] 
    return data_list

create_session() 

if st.session_state["init_load"]:
    st.session_state["init_load"] = False    
    st.session_state["data_frame"] = get_data()
    st.session_state["model"] = get_model()
    st.session_state["currently_displayed_frame"] = st.session_state["data_frame"]
#--------------------------------------------Code--------------------------------------------  

#--------------------------------------------UI--------------------------------------------
search_mode_value = st.session_state["searching_mode_value"]
st.write(f"Searching in: {search_mode_value}")

with st.container():
    search_row = st.columns(2)     
    with search_row[0].container():
        st.text_input("Search for artists/track: ", key="search_bar_value", placeholder="Enter the name of the track/artist", on_change=reload_data)
    with search_row[1].container():
        disabled = not(st.session_state["recommendations_search_enabled"])
        st.button("Turn off recommendations search", on_click=on_turn_off_recommendations_request, disabled=disabled)

main_songs_selection_layout, _, genre_selection = st.columns(3, gap="large")

with st.sidebar:
    criteria_limits_dict : dict = st.session_state["criteria_limits"]
    criteria_values_dict: dict = st.session_state["criteria_values"]
    
    for criterion in criteria_limits_dict.keys():
        min_val, max_val = criteria_limits_dict[criterion]
        current_val = criteria_values_dict[criterion]
        st.slider(criterion, min_val, max_val, current_val, key=criterion, step=0.1, on_change=reload_data)

with main_songs_selection_layout.container():
    currently_displayed_frame = st.session_state["currently_displayed_frame"]
    left = st.session_state["paginator_left_value"]
    right = st.session_state["paginator_right_value"]
    to_display_to_list: list[Track] = get_display_information(currently_displayed_frame)
    tracks_to_display = to_display_to_list[left:right]
    rows = [st.columns(1, gap="large") for _ in enumerate(tracks_to_display)]
    
    if len(tracks_to_display) == 0:
        st.write("No tracks using the current search criteria were found!")
    else: 
        for i, row in enumerate(rows):
            for col in row:
                with col.container():
                    thick_line = """
                    <hr style="border:2px solid gray">
                    """
                    st.markdown(thick_line, unsafe_allow_html=True)
                    track_to_display = tracks_to_display[i]
                    components.iframe(f"https://open.spotify.com/embed/track/{track_to_display.id}",  width=270, height=380)
                    with st.expander("More details", expanded=False):
                        st.write(f"**Track name:** {track_to_display.name}")
                        st.write(f"**Artists:** {track_to_display.artists}")
                        f = get_radar_chart([track_to_display.danceability, track_to_display.valence, track_to_display.energy, track_to_display.instrumentalness], 
                                        ["danceability", "valence", "energy", "instrumentalness"],
                                        width=450, height=390)
                        st.write(f)
                        
                    st.button("Get recommendations", key=track_to_display.id, on_click=on_get_recommendations_click, args=[track_to_display.id])    
                    
    with st.container():
        paginator_row = st.columns(2)     
        with paginator_row[0].container():
            st.button("<-", on_click=on_paginator_left)
        with paginator_row[1].container():
            st.button("->", on_click=on_paginator_right)
            
    page_count = st.session_state["page_count"]
    st.write(f"Page {page_count}, Entries ({left}-{right})")
            

with genre_selection.container():
    st.radio(
        "Choose the preferred genre",
        st.session_state["genres_to_select"],
        key='selected_genre',
        on_change=reload_data)
#--------------------------------------------UI--------------------------------------------