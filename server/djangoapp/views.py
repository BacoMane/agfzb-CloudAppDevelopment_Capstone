from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from .restapis import get_dealers_from_cf, get_dealers_by_state, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def get_template(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/template.html', context)


# Create an `about` view to render a static about page
# def about(request):
# ...
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
#def contact(request):
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')
# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
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
        #return render(request, 'djangoapp/index.html', context)
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/55541385-d011-41ed-ad7e-867fc2819f68/dealership-package/get-dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        #dealerships = get_dealers_by_state(url,'Texas')
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        context["dealership_list"] = dealerships
        print("dealerships")
        print(dealerships)
        #return HttpResponse(dealer_names)
        return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        #return render(request, 'djangoapp/index.html', context)
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/55541385-d011-41ed-ad7e-867fc2819f68/dealership-package/get_review"
        # Get dealers from the URL
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        no_reviews = False
        #dealerships = get_dealers_by_state(url,'Texas')
        if reviews:
            context['reviews'] = reviews
            for review in reviews:
                dealer_name = review.name
                
            # Concat all dealer's short name
            context['dealer_name'] = dealer_name
            context['dealer_id'] = dealer_id
            dealer_names = ' '.join([review.review for review in reviews])
        else:
            dealer_names = 'no reviews'
            no_reviews = True
        context['no_reviews'] = no_reviews
        
        # Return a list of dealer short name
        #return HttpResponse(dealer_names)
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id):
    url = "https://us-south.functions.appdomain.cloud/api/v1/web/55541385-d011-41ed-ad7e-867fc2819f68/dealership-package/post_review"
    user = request.user
    context = {}
    if request.method == 'GET':

        if not user.is_authenticated:
            review = {}
            review["id"]= 1
            review["name"]= "Berkly Shepley"
            review["dealership"] = dealer_id
            review["review"] = "This is a great car dealer"
            review["purchase"]= True
            review["purchase_date"]= "07/11/2021"
            review["car_make"]= "Audi"
            review["car_model"]= "A6"
            review["car_year"]= 2010  

            json_payload = {}
            json_payload["review"] = review
            #response = post_request(url, json_payload, dealerId=dealer_id)
            cars = CarModel.objects.filter(Q(dealer_id=dealer_id)) 
            print(cars) 
        else:
            context['dealer_id'] = dealer_id 
            #return HttpResponse("User not logged in")
            return render(request, 'djangoapp/add_review.html', context)

        print("status code ")
        #return HttpResponse(response)
        return HttpResponse(cars)
    #return HttpResponse('no')
    return render(request, 'djangoapp/add_review.html', context)

