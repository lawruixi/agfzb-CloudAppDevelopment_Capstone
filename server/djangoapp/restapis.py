import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from .env import nlu_key, nlu_url

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        api_key = kwargs.get('api_key', None)
        if api_key:
            #api_key was provided
            response = requests.get(url, headers={'Content-Type': 'application/json'}, auth=HTTPBasicAuth('apikey', api_key), params=kwargs)
        else:
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred during GET.")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    print(json_payload)
    print(kwargs)
    print("POST to {}".format(url))
    try:
        response = requests.post(url, params=kwargs, json=json_payload)
    except Exception as e:
        print(str(e))
        print("Network exception occured during POST.")
    status_code = response.status_code
    print("With status {}".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    print(json_result)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # For each dealer object
        for dealer_doc in dealers:
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
def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url, dealership=kwargs.get("dealership"))
    if json_result:
        reviews = json_result["response"]
        for review in reviews:
            review_obj = DealerReview(
                dealership = review["dealership"],
                name = review["name"],
                purchase = review["purchase"],
                review = review["review"],
                id = review["id"],
                purchase_date  = review.get("purchase_date", None),
                car_make = review.get("car_make", None),
                car_model = review.get("car_model", None),
                car_year  = review.get("car_year", None),
                sentiment = "none"
            );
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)
    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealer_review):
    json_result = get_request(nlu_url,
                                text=dealer_review,
                                version="2021-08-01",
                                features="sentiment",
                                return_analyzed_text = True,
                                api_key=nlu_key
    )
    if json_result:
        error = json_result.get("error", None)
        if error:
            print("NLU Error")
            return "none"
        else:
            return json_result["sentiment"]["document"]["label"]
    print("NLU Error")
    return "none"

