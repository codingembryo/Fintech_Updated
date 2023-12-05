from django.shortcuts import render, redirect
import requests
from django.shortcuts import render
from .utils import get_vtpass_basic_auth
from django.http import HttpResponse



def verify_smartcard(request):
    if request.method == 'POST':
        smartcard_number = request.POST.get('smartcard_number')
        service_id = 'dstv'
        verify_url = f'https://sandbox.vtpass.com/api/merchant-verify'

        headers = {
            'Authorization': get_vtpass_basic_auth(),
        }

        data = {
            'billersCode': smartcard_number,
            'serviceID': service_id,
        }

        response = requests.post(verify_url, headers=headers, data=data)

        if response.status_code == 200:
            api_response = response.json()
            # Process the API response and display relevant data to the user
            return render(request, 'verify_smartcard.html', {'api_response': api_response})
        else:
            error_message = "Error occurred while verifying smart card"
            return render(request, 'verify_smartcard.html', {'error_message': error_message})
        
    return render(request, 'verify_smartcard.html')




# views.py
def purchase_product(request):
    if request.method == 'POST':
        smartcard_number = request.POST.get('smartcard_number')
        variation_code = request.POST.get('variation_code')
        amount = request.POST.get('amount')
        service_id = 'dstv'
        request_id = 'your_unique_request_id'  # Generate a unique request ID

        purchase_url = f'https://sandbox.vtpass.com/api/pay'

        headers = {
            'Authorization': get_vtpass_basic_auth(),
        }

        data = {
            'request_id': request_id,
            'serviceID': service_id,
            'billersCode': smartcard_number,
            'variation_code': variation_code,
            'amount': amount,
            'phone': 'customer_phone_number',
            'subscription_type': 'renew',  # or 'change' for bouquet change
            'quantity': 1,
        }

        response = requests.post(purchase_url, headers=headers, data=data)

        if response.status_code == 200:
            api_response = response.json()
            # Process the API response and display relevant data to the user
            return render(request, 'purchase_product.html', {'api_response': api_response})
        else:
            error_message = "Error occurred while purchasing product"
            return render(request, 'purchase_product.html', {'error_message': error_message})
        
    return HttpResponse("This is the purchase_product view.")







import json
def subscription_form(request):

    bouquet_options = [

        {"name": "DStv Padi", "value": "N2,500"},
        {"name": "DStv Yanga", "value": "N3,500"},
        {"name": "Dstv Confam", "value": "N6,200"},
        {"name": "DStv Compact", "value": "N10,500"},
    ]
    try:
        response = requests.get("https://sandbox.vtpass.com/api/service-variations?serviceID=dstv", headers={
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
    
    if request.method == "POST":
        selected_bouquet = request.POST.get("bouquet")
        smartcard_num = request.POST.get("iuc")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        ammount = request.POST.get("amount")
        from .utils import generate_request_id
        body ={
            "request_id":str(generate_request_id()),
            "serviceID":"dstv",
            "billersCode":str(smartcard_num),
            "variation_code":str(selected_bouquet),
            "phone":str(phone),
            "subscription_type":"change",
            "quantity":"1"
        }
        for option in bouquet_options:
            if option["name"] == selected_bouquet:
                context["selected_amount"] = option["value"]
                body["amount"] = option["value"]
                break
        response = requests.post("https://sandbox.vtpass.com/api/pay", data=json.dumps(body), headers={
                "Content-Type":"application/json",
                "api-key": "fc80349ce564c62d9be85521cc3b242c",
                "secret-key": "SK_6287e7a1cb97b1981a4970459aef8f4afb214bb3a6d",
                "public-key": "PK_9955836332abf19ef78780f34f79c92fcd48d98f0b8"
        })
        options = json.loads(response.content.decode('utf-8')) 
        if options['code'] == "000":
            return render(request, "success.html")
        else:
            return render(request, "failed.html")
        return render(request, "response.html", {"options":options})

    return render(request, "subscription_form.html", context)






