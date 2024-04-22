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

# convert date to simple date format
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

# Function to greet the user
def greet_user():
    return "Hello! Welcome to InnSight, your personal hotel recommender system. Please choose a state to get started."  

#Function to get the unique states
def get_state(dt):
    return dt['province'].unique()

# Function to make list of cities in a state
def get_cities(dt, state):
    return dt[dt['province'] == state]['city'].unique()
        
# Function to recommend top hotels
def recommend_top_hotels(dt,city, top_n=5):
    city_hotels = filter_hotels_by_city(dt,city)
    top_hotels = city_hotels.groupby('name')['reviews.rating'].mean().sort_values(ascending=False).head(top_n)
    return top_hotels

# Function for sentiment analysis
def analyze_sentiment(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0.5:
        return 'Better'
    elif analysis.sentiment.polarity > 0:
        return 'Good'
    else:
        return 'Neutral or Negative'


# Function to categorize reviews of a hotel
def categorize_reviews(dt,hotel_name):
    hotel_reviews = dt[dt['name'].str.contains(hotel_name, case=False, na=False)]['reviews.text']
    sentiment_analysis = hotel_reviews.apply(analyze_sentiment)
    return sentiment_analysis.value_counts()

# Function to get the average rating of a hotel
def get_average_rating(dt,hotel_name):
    return dt[dt['name'].str.contains(hotel_name, case=False, na=False)]['reviews.rating'].mean()
    
# Function to check if a hotel is in the top 5
def is_hotel_in_top5(city, hotel_name):
    top_hotels = recommend_top_hotels(city)
    return hotel_name in top_hotels.index


#Function to check duplicate cities in the dataset
def check_duplicate_cities(dt):
    return dt['city'].duplicated().sum()
 
#Function to check duplicate hotel names in cities and states
def check_duplicate_hotels(dt):
    return dt['name'].duplicated().sum()

# Function to filter hotels by city
def filter_hotels_by_city(dt,city):
    return dt[dt['city'].str.lower() == city.lower()]

# Function for sentiment analysis
def analyze_sentiment(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0.5:
        return 'Better'
    elif analysis.sentiment.polarity > 0:
        return 'Good'
    else:
        return 'Neutral or Negative'


