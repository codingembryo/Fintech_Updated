
from .forms import SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
import requests
import random
import string
import json
from django.http import JsonResponse, HttpResponse
from datetime import datetime


# Create your views here.

def home(request):
     return render(request, 'home.html')



def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in!!")
            return redirect('home')
        else:
            messages.error(request, "There was an error trying to login")
            return redirect('login')
    
    return render(request, 'login.html', {})
            


def logout_user(request):
    logout(request)
    messages.success(request, 'You have logged out successfully.')
    return render(request, 'logout.html')

def about(request):
    return render(request, 'about.html')

def security(request):
    return render(request, 'security.html')

def faq(request):
    return render(request, 'faq.html')

def support(request):
    return render(request, 'support.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have registered successfully...!!!")
            return redirect('home')
    else:
        form = SignUpForm()
    
    return render(request, 'signup.html', {'form':form})




def airtime(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        amount = request.POST.get('amount')
        email = request.POST.get('email')
        from .utils import generate_request_id
        data = {
            "serviceID": "mtn",
            "amount": "199",
            "phone": "08011111111",
            "request_id": str(generate_request_id())
        }
        try:
            print('request created---------------------------------------------------------------')
            response = requests.post("https://sandbox.vtpass.com/api/pay", data=json.dumps(data), headers={
                "Content-Type":"application/json",
                "api-key": "fc80349ce564c62d9be85521cc3b242c",
                "secret-key": "SK_6287e7a1cb97b1981a4970459aef8f4afb214bb3a6d",
                "public-key": "PK_9955836332abf19ef78780f34f79c92fcd48d98f0b8"
            })
            
            print(response)
            print(json.dumps(data))
            print('request completed--------------------------------------------------------------')
            # Process the response
            if response.status_code == 200:
                response_data = response.json()
                print(response_data)
                if response_data['code'] == "000":
                    return render(request, "success.html")
                else:
                    return render(request, "failed.html")
                return JsonResponse(response_data)
            else:
                error_message = "An error occurred while processing the request."
                return render(request, "error_page.html", {"error_message": error_message})
        except Exception as e:
            print(e)
            return render(request, "airtime.html")

    return render(request, "airtime.html")

def mntData(request):
    # bouquet_options = [

    #     {"name": "DStv Padi", "value": "N2,500"},
    #     {"name": "DStv Yanga", "value": "N3,500"},
    #     {"name": "Dstv Confam", "value": "N6,200"},
    #     {"name": "DStv Compact", "value": "N10,500"},
    # ]
    try:
        response = requests.get("https://sandbox.vtpass.com/api/service-variations?serviceID=mtn-data", headers={
            "Content-Type":"application/json",
            "api-key": "fc80349ce564c62d9be85521cc3b242c",
            "secret-key": "SK_6287e7a1cb97b1981a4970459aef8f4afb214bb3a6d",
            "public-key": "PK_9955836332abf19ef78780f34f79c92fcd48d98f0b8"
        })
        
        formatted_data = []

        for item in json.loads(response.content)["content"]['varations']:
            name_parts = item["name"].split()
            name = " ".join(name_parts[:-1])  # Extracting the name part
            value = item["variation_amount"]  # Using "variation_amount" as the value
            code = item["variation_code"]
            formatted_item = {"name": name, "code":code, "value": value}
            formatted_data.append(formatted_item)
        # print(formatted_data)
        bouquet_options = formatted_data
    except Exception as e:
        print("unable to make request, Following exception occured")
        print(e)
    
    context = {
        "bouquet_options": bouquet_options,
    }
    # active = 0
    # body = None
    if request.method == "POST":
        selected_bouquet = request.POST.get("bouquet")
        phone = smartcard_num = request.POST.get("phone")
        email = request.POST.get("email")
        active = request.POST.get("active")
        print(active,type(active))
        from .utils import generate_request_id
        body ={
            "request_id":str(generate_request_id()),
            "serviceID":"mtn-data",
            "billersCode":str(smartcard_num),
            "variation_code":str(selected_bouquet),
            "phone":str(phone),
            "email":email
        }

        for option in bouquet_options:
            if option["name"] == selected_bouquet:
                context["selected_amount"] = option["value"]
                body["amount"] = option["value"]
                break
        if active == "true":
            return render(request, "confirmation.html", {"options":body})
        else:
            print(body)
            response = requests.post("https://sandbox.vtpass.com/api/pay", data=json.dumps(body), headers={
                    "Content-Type":"application/json",
                    "api-key": "fc80349ce564c62d9be85521cc3b242c",
                    "secret-key": "SK_6287e7a1cb97b1981a4970459aef8f4afb214bb3a6d",
                    "public-key": "PK_9955836332abf19ef78780f34f79c92fcd48d98f0b8"
            })
            options = json.loads(response.content.decode('utf-8')) 
            if options['code'] == "000":
                return render(request, "success_data.html")
            else:
                return render(request, "failed.html")
            
            return render(request, "response.html", {"options":options})

    return render(request, "MTN_data.html",context)



# Define a function to get variation codes
def get_variation_codes():

    serviceID = "mtn-data"
    # Set the API endpoint
    api_url = "https://sandbox.vtpass.com/api/service-variations"
    # Send a GET request with serviceID as query parameter
    response = requests.get(api_url, params={"serviceID": serviceID})
    # Parse the response as JSON
    data = response.json()
    # Return the content field
    return data["content"]

# Define a function to purchase product
# def purchase_product(request_id, phone, variation_code):
# # Set your API key and secret key
#     api_key = "fc80349ce564c62d9be85521cc3b242c"
#     secret_key = "SK_952894cffaecd3191d6a580041776279f644e87db0a"

#     # Set the serviceID
#     serviceID = "mtn-data"
#     # Set the amount (will be ignored by API)
#     amount = 0
#     # Set the API endpoint
#     api_url = "https://sandbox.vtpass.com/api/pay"

#     # Set the data parameters based on user input and function arguments
#     data = {
#     "request_id": request_id,
#     "serviceID": serviceID,
#     "billersCode": phone,
#     "variation_code": variation_code,
#     "amount": amount,
#     "phone": phone
#     }

#     # Set the header parameters
#     headers = {
#     "api-key": api_key,
#     "secret-key": secret_key
#     }

#     # Send a POST request with data and header parameters
#     response = requests.post(api_url, data=data, headers=headers)

#      # Parse the response as JSON
#     data = response.json()

#     # Get the content field of the data or an empty dictionary if not found
#     content = data.get('content', {})

#     # Return the content as the output of the function
#     return content



# # Import requests library
# import requests

# # Define a function to query transaction status
# def query_transaction_status(request_id):
# # Set your API key and secret key
#     api_key = "fc80349ce564c62d9be85521cc3b242c"
#     secret_key = "SK_952894cffaecd3191d6a580041776279f644e87db0a"

#     # Set the API endpoint
#     api_url = "https://sandbox.vtpass.com/api/requery"

#     # Set the header parameters
#     headers = {
#     "api-key": api_key,
#     "secret-key": secret_key
#     }

#     # Set the data parameter with request_id
#     data = {"request_id": request_id}

#     # Send a POST request with data and header parameters
#     response = requests.post(api_url, data=data, headers=headers)

#     # Parse the response as JSON
#     data = response.json()

#     # Get the content field of the data or an empty dictionary if not found
#     content = data.get('content', {})

#     # Return the content as the output of the function
#     return content



def index(request):
    pass
#     # Get variation codes from API
#     variations = get_variation_codes()

#     # Initialize purchase result and transaction status as None
#     purchase_result = None
#     transaction_status = None

#     # Check if request method is POST
#     if request.method == "POST":
#         # Get user input from form fields
#         phone = request.POST["phone"]
#         print("request.POST:", request.POST)
#         variation_code = request.POST["variation_code"]

#         # Generate a random request_id
#         request_id = "".join(random.choices(string.ascii_letters + string.digits, k=16))

#         # Purchase product from API with user input and request_id
#         purchase_result = purchase_product(request_id, phone, variation_code)

#         # Check if purchase_result is a dictionary
#         if isinstance(purchase_result, dict):
#             # Check if purchase_result contains transactions field
#             if "transactions" in purchase_result:
#                 # Get the status of the transaction
#                 purchase_status = purchase_result["transactions"]["status"]
#             else:
#                 # Handle the case when purchase_result does not contain transactions field
#                 purchase_status = "Purchase failed: No transaction details found"
#         else:
#             # Handle the case when purchase_result is not a dictionary
#             purchase_status = f"Purchase failed: {purchase_result}"

#         # Query transaction status from API with request_id
#         transaction_status = query_transaction_status(request_id)

#         # Convert the transaction_status into a JSON string
#         transaction_status = json.dumps(transaction_status)

#         # Render HTML template with context variables
#         return render(request, "index.html", {
#             "variations": variations,
#             "purchase_status": purchase_status,
#             "transaction_status": transaction_status,
#             "phone": phone
#         })

#     # Add a default return statement outside the if block
#     return render(request, "index.html", {"variations": variations})


# Import requests library
import requests

# Define a function to query variation detail
def query_variation_detail(service, value):

    api_key = "ap_7fc5492227c0643709a95c8727286880"

    # Set the API endpoint
    api_url = "https://www.vtusub.com/api/variation"

    # Set the header parameter
    headers = {
    "Authorization": api_key
    }

    # Set the query parameters
    params = {
    "service": service,
    "value": value
    }

    # Send a GET request with header and query parameters
    response = requests.get(api_url, headers=headers, params=params)

    # Parse the response as JSON
    data = response.json()

    # Return the data as the output of the function
    return data


# import requests module
import requests
from .models import Category, Subcategory
from django.shortcuts import render

# define a function to get category
def get_category():
    response = requests.get("https://www.vtusub.com/api/category")
    # check if the request was successful
    if response.status_code == 200:
    # parse the JSON response
        data = response.json()
        # return the list of categories
        return data
    else:
        # return an error message
        return f"Request failed with status code {response.status_code}"

        # define a function to get subcategory given a category name
def get_subcategory(category):
        # send a GET request to the subcategory endpoint with the category parameter
    response = requests.get(f"https://www.vtusub.com/api/sub-category?category={category}")
        # check if the request was successful
    if response.status_code == 200:
        # parse the JSON response
        data = response.json()
        # return the list of subcategories
        return data
    else:
        # return an error message
        return f"Request failed with status code {response.status_code}"

#         # test the functions
# print(get_category())
# print(get_subcategory("mobile_vtu"))

def display_data(request):
# query all the categories and subcategories from the database
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    # pass the data to a template called data.html
    return render(request, "data.html", {"categories": categories, "subcategories": subcategories})


# import requests and os modules
import requests
import os

# import render function from django.shortcuts
from django.shortcuts import render

# get the base URL and API key from settings.py
BASE_URL = os.environ.get("BASE_URL")
API_KEY = os.environ.get("API_KEY")

# define a view function that takes a request object as an argument
def get_categories(request):
# send a GET request to the category endpoint with the API key as a header
    response = requests.get(BASE_URL + "/api/category", headers={"x-api-key": API_KEY})
    # check if the request was successful
    if response.status_code == 200:
    # parse the JSON response
        data = response.json()
    # pass the data to a template called categories.html
        return render(request, "categories.html", {"data": data})
    else:
    # return an error message
        return f"Request failed with status code {response.status_code}"
import requests

from django.shortcuts import render
import requests

import requests
from django.shortcuts import render

from django.shortcuts import render
import requests



def confirmation(request):
    return render(request, "confirm_transaction.html")

# Your existing view function
def variation_names(request):
    if request.method == 'POST':
        # Handle form submission
        # Extract form data (variation, smart_card, phone, email, amount) from request.POST
        variation = request.POST.get('variation')
        smart_card = request.POST.get('smart_card')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        amount = request.POST.get('amount')

        # Calculate the total payable amount based on the selected variation
        # You can add your calculation logic here

        
        transaction_details = {
            'variation': variation,
            'smart_card': smart_card,
            'amount': amount,
            # Add other details like phone, email, and total amount
        }

        return render(request, 'confirm_transaction.html', {'transaction_details': transaction_details})

    else:
        # Handle GET requests (display the form)
        # Define the API URL
        url = "https://api-service.vtpass.com/api/service-variations?serviceID=dstv"

        # Make the GET request
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            variation_data = response.json()

            # Extract the variations from the response
            variations = variation_data.get('content', {}).get('variations', [])

            # Pass the variations to the template
            return render(request, 'get_variation.html', {'variations': variations})
        else:
            # Handle the error if the request was not successful
            error_message = f"Error: {response.status_code}, {response.text}"
            return render(request, 'error_template.html', {'error_message': error_message})



# views.py

from django.shortcuts import render

def get_services(request):
    # Creating sample data directly (replace this with your own logic)
    services_list = [
        {"identifier": "airtime", "name": "Airtime Recharge"},
        {"identifier": "data", "name": "Data Services"},
        # Add more sample data as needed
    ]

    # Create the context for the template
    response_data = {
        "response_description": "000",
        "content": services_list
    }

    # Render the template with the context
    return render(request, 'services_template.html', {'data': response_data})




