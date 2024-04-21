import os
import pandas as pd

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


