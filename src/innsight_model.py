import requests
import dotenv
import os
import json
from langchain.chains import AnalyzeDocumentChain
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain

dotenv.load_dotenv()

def get_latlong(address):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={os.environ.get('GOOGLE_API_KEY')}"
    response = requests.get(url)
    if response.status_code != 200:
        return "Error in fetching place details"
    return response.json()


def search_hotels(location, radius):
    ''' 
        Search hotels using location with specific radius
    '''
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius={radius}&keyword=hotels&key={os.environ.get('GOOGLE_API_KEY')}"
    response = requests.get(url)
    print(response)
    if response.status_code != 200:
        return "Error in fetching places"
    return response.json()

def get_place_details(place_id):
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=name,rating,review&key={os.environ.get('GOOGLE_API_KEY')}"
    response = requests.get(url)
    if response.status_code != 200:
        return "Error in fetching place details"
    return response.json()

def search_places(query, selectedType, minRating): 
    '''
        Search hotels using google places api 
    '''
    #API endpoint
    url = 'https://places.googleapis.com/v1/places:searchText'

    includedTypes = ["extended_stay_hotel", "hotel", "lodging"]

    #headers
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': os.environ.get('GOOGLE_API_KEY'), 
        'X-Goog-FieldMask': 'places.id,places.displayName,places.rating,places.reviews,places.websiteUri,places.types,places.primaryType'
    }

    #data payload for the POST request
    data = {
        'textQuery': selectedType + ' ' + query, 
        'maxResultCount': 5,
        'minRating': minRating,
        'strictTypeFiltering': True,
        'includedType': selectedType
    }

    hotel_details = []

    response = requests.post(url, headers=headers, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        # Process the response
        if (type(json.loads(response.text)) == dict) and len(json.loads(response.text)) != 0:
            for eachPlace in json.loads(response.text)['places']:
                if (eachPlace["primaryType"] == selectedType):
                    details = {
                        'placeId': eachPlace['id'],
                        'name' : eachPlace['displayName']['text'],
                        'types' : eachPlace['types'] if 'types' in eachPlace else None,
                        'primaryType' : eachPlace['primaryType'] if 'primaryType' in eachPlace else None,
                        'website' : eachPlace['websiteUri'] if 'websiteUri' in eachPlace else None,
                        'rating' : eachPlace['rating'] if 'rating' in eachPlace else None,
                        'reviews' : eachPlace['reviews'] if 'reviews' in eachPlace else None        
                    }
                    
                    all_reviews = []
                    if details['reviews'] != None:
                        for eachReview in details['reviews']:
                            review_text = eachReview['text']['text']
                            all_reviews.append(review_text)
                            details['allReviews'] = (' '.join(all_reviews))

                    hotel_details.append(details)
            try:
                sorted_list = sorted(hotel_details, key=lambda x: x['rating'], reverse=True)
                print(f'Hotel Details List: {len(sorted_list)}')
                return sorted_list
            except Exception as ex:
                print(f'Error when sorting: {ex}')

            print(f'Hotel Details List: {len(hotel_details)}')
    else:
        print(f"Error: {response.status_code}, {response.text}")
    return hotel_details

def analyze_reviews(review_data, review_prompt):
    ''' 
        Function to process hotel reviews based on the prompt provided using Langchain, 
        ChatOpenAI and QA chains form langchain. 

        Prompt Examples: 
        Which of the hotels has the best reviews and why do you think that? You must make a choice
        and choose one hotel and provide reasoning behind it. 

        Analyze the reiviews of the hotel, and tell which has the positive sentiment? Based on sentiment 
        analysis recommend top 3 hotels? And provide the sentiment scores for each hotel?

    '''
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    qa_chain = load_qa_chain(llm, chain_type="map_reduce")
    qa_document_chain = AnalyzeDocumentChain(combine_docs_chain=qa_chain)
    ans = qa_document_chain.run(
        input_document=review_data, 
        question=review_prompt)
    return ans

def get_lat_long(city_name):
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": city_name,
        "format": "json"
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    if data:
        lat = data[0]["lat"]
        lon = data[0]["lon"]
        return lat, lon
    else:
        return None, None
    
def get_top_attractions(longitude, latitude, n):
    try:
        # Convert n to an integer
        n = int(n)
        if n <= 0:
            raise ValueError("N must be a positive integer")
        # Make API call
        url = f"https://api.opentripmap.com/0.1/en/places/radius?radius=100000&lon={longitude}&lat={latitude}&kinds=tourist_object&format=json&limit={n}&apikey={os.environ.get('OPEN_TRIP_MAP_KEY')}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad response status
        # Extract top attractions
        attractions = response.json()
        # Extract names of top attractions
        top_attractions = [attraction['name'] for attraction in attractions]
        return top_attractions
    
    except ValueError as ve:
        print(f"Error: {ve}")
    except requests.RequestException as re:
        print(f"Error making API request: {re}")
    except KeyError:
        print("Error: Response format unexpected, please check API documentation.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")