from django.urls import path
from . import views

urlpatterns = [
    path('category/', views.category_view, name='category'),
    path('subcategory/', views.subcategory_view, name='subcategory'),
    # Define other URLs for other views
]