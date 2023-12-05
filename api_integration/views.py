from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
import requests

def get_api_data(url):
    API_KEY = "ap_7fc5492227c0643709a95c8727286880"
    HEADERS = {"Authorization": f"Bearer {API_KEY}"}
    
    response = requests.get(url, headers=HEADERS)
    return response.json()

def category_view(request):
    categories = get_api_data("https://www.vtusub.com/api/category")
    return render(request, "api_integration/category.html", {"categories": categories})

def subcategory_view(request):
    category = "mobile_vtu"
    subcategory = get_api_data(f"https://www.vtusub.com/api/sub-category?category={category}")
    return render(request, "api_integration/subcategory.html", {"subcategory": subcategory})

# Similarly, define views for other API calls: service, fields, plans, variation
