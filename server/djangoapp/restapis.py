import requests
import json
# import related models here
from .models import CarDealer, DealerReview 
from requests.auth import HTTPBasicAuth

from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions, SentimentOptions

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs): 
    print('the kwargs are: ')
    print(kwargs)
    print("GET from {} ".format(url))
    if "api_key" in kwargs:
        try:
            print('calling nlu api')
            #response = requests.get(url, params=params, features=Features(
            #entities=EntitiesOptions(emotion=True, sentiment=True, limit=2),
            #keywords=KeywordsOptions(emotion=True, sentiment=True,
                            #     limit=2)), headers={'Content-Type': 'application/json'},
                             #                   auth=HTTPBasicAuth('apikey', api_key))
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            print(params)
            response = requests.get(url, 
                                    text=kwargs["text"],
                                    version=kwargs["version"],
                                    features=kwargs["features"],
                                    return_analyzed_text= kwargs["return_analyzed_text"],
                                    headers={'Content-Type': 'application/json'},
                                    api_key=kwargs['api_key']
                                    )
        except:
            print("Network exception occurred")
    else:
        try:
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                        params=kwargs)
        except:
            # If any error occurs
            print("Network exception occurred")
    status_code = response.status_code
    
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

def get_dealers_by_state(url, dealerState, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url,state=dealerState)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealer_id, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url,id=dealer_id)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["data"] 
        dealers = dealers['docs']
        # For each dealer object
        for dealer_doc in dealers:
            # Get its content in `doc` object
            print("calling analyze_review_sentiments")
            sentiment = analyze_review_sentiments(dealer_doc['review'])
            print('')
            if dealer_doc['purchase']:
                # Create a CarDealer object with values in `doc` object
               
                dealer_obj = DealerReview(dealership=dealer_doc["dealership"], purchase=dealer_doc["purchase"], name=dealer_doc["name"],
                                    id=dealer_doc["id"], review=dealer_doc["review"], purchase_date=dealer_doc["purchase_date"],
                                    car_make=dealer_doc["car_make"],
                                    car_model=dealer_doc["car_model"], car_year=dealer_doc["car_year"], sentiment=sentiment)
                results.append(dealer_obj)
            else:
                dealer_obj = DealerReview(dealership=dealer_doc["dealership"], purchase=dealer_doc["purchase"], name=dealer_doc["name"],
                                    id=dealer_doc["id"], review=dealer_doc["review"], purchase_date=None,
                                    car_make=None,
                                    car_model=None, car_year=None, sentiment=sentiment)
                results.append(dealer_obj)

    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealerreview, **kwargs):
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/6c7755c8-7545-42ce-8512-a05f25de7841"
    api_key = "unMzdImt89TuzDVVCtZiqg9F23_-7IxNyZIQwF-xRd0-" 
    #Features(
     #   entities=EntitiesOptions(emotion=True, sentiment=True, limit=2),
      #  keywords=KeywordsOptions(emotion=True, sentiment=True,
       #                          limit=2))
    version = '2020-08-01'
    features = "sentiment"
    return_analyzed_text = True
    text = dealerreview
    print("calling get_request for nlu")

 

    #json_result = get_request(url,
                            #api_key=api_key,
                           # text=dealerreview, 
                           # features=features,
                           # version=version,
                          #  return_analyzed_text=return_analyzed_text
                            #)

    authenticator = IAMAuthenticator(api_key) 
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator) 
    natural_language_understanding.set_service_url(url) 

    response = natural_language_understanding.analyze( text=text, features=Features(sentiment=SentimentOptions(targets=[text]))).get_result() 
    label=json.dumps(response, indent=2)
    label = response['sentiment']['document']['label']
    print("label")
    print(label)

    return(label)
    #return json_result

