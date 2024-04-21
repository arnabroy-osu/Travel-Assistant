import os
import pandas as pd
from datetime import datetime

# get the list of data files from resource dir
data_file_path = "../Resources/Reviews/cleaned"
data_files = os.listdir(data_file_path)
data_files

def get_hotel_reviews():
    '''

    '''
    # Hotel Reviews
    hotel_files = [file for file in data_files if file.startswith('hotel') and file.endswith('.csv')]
    h_dfs = []

    #print(hotel_files)
    
    for each_file in hotel_files: 
        h_dfs.append(pd.read_csv(data_file_path+ "/" + each_file))

    hotel_reviews_df = pd.concat(h_dfs).reset_index(drop=True)

    return hotel_reviews_df

def get_airbnb_reviews():
    '''

    '''
    # Hotel Reviews
    airbnb_files = [file for file in data_files if file.startswith('airbnb') and file.endswith('.csv')]
    a_dfs = []

    for each_file in airbnb_files: 
        a_dfs.append(pd.read_csv(data_file_path + "/" + each_file))

    airbnb_reviews_df = pd.concat(a_dfs).reset_index(drop=True)

    # drop the duplicate rows 
    airbnb_reviews_df.drop_duplicates(keep='first', inplace=True)
    airbnb_reviews_df.reset_index(drop=True, inplace=True)

    return airbnb_reviews_df

def replace_string_in_column(df, column, string_to_replace, replacement_string):
    """
    Replace a string with another string in a specified column of a pandas DataFrame.

    Parameters:
        df (pandas.DataFrame): The pandas DataFrame.
        column (str): The name of the column in which the replacement will be made.
        string_to_replace (str): The string to be replaced.
        replacement_string (str): The string to replace occurrences of `string_to_replace`.
    
    Returns:
        pandas.DataFrame: The modified DataFrame with the replacements.
    """
    df[column] = df[column].apply(lambda x: x.replace(string_to_replace, replacement_string))
    
    return df

def convert_date_format(df, date_column):
    """
    Convert date values in a specified column of a pandas DataFrame to a simpler date format.

    Parameters:
        df (pandas.DataFrame): The pandas DataFrame.
        date_column (str): The name of the column containing date values to be converted.

    Returns:
        pandas.DataFrame: The modified DataFrame with the date values converted to a simpler format.
    """
    df[date_column] = df[date_column].apply(lambda x: pd.to_datetime(x).strftime('%Y-%m-%d'))
    return df