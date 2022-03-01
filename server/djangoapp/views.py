from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, analyze_review_sentiments, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exists = False

        print(username)
        print(password); print(first_name); print(last_name)
        try:
            User.objects.get(username=username)
            user_exists = True
        except:
            logger.info("New User")

        if not user_exists:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://48d8f675.us-south.apigw.appdomain.cloud/api/dealership"
        dealerships = get_dealers_from_cf(url)
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        return HttpResponse(dealer_names);


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://48d8f675.us-south.apigw.appdomain.cloud/api/review"
        reviews = get_dealer_reviews_from_cf(url, dealership=dealer_id)
        #review_names = ' '.join([review.name for review in reviews])
        review_string = ""
        for review in reviews:
            review_string += "Name: {0}, Review: {1}, Sentiment: {2}<br>".format(review.name, review.review, review.sentiment)
        return HttpResponse(review_string)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    user = request.user
    if user.is_authenticated:
        #TODO: Probably dynamic page?
        review = dict()
        review["time"] = datetime.utcnow().isoformat()
        review["dealership"] = dealer_id
        review["review"] = "Temporary review, but this is great!"

        json_payload = {"review": review}
        url = "https://48d8f675.us-south.apigw.appdomain.cloud/api/review"
        response = post_request(url, json_payload, dealerId=dealer_id)
        return HttpResponse(response)
    else:
        #TODO: Better page? Or like some error dialog box
        return HttpResponse("You must be authenticated to post a review.")
