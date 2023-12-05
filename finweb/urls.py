from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('about/', views.about, name='about'),
    path('security/', views.security, name='security'),
    path('faq/', views.faq, name='faq'),
    path('support/', views.support, name='support'),
    path('signup/', views.signup, name='signup'),
    path('airtime/', views.airtime, name='airtime'),
    path('data/', views.mntData, name='data'),
    path('index/', views.index, name='index'),
    path('data/', views.display_data, name='data'),
    path('get-variation/', views.variation_names, name='get_variation'),
    path('confirmation/', views.confirmation, name='confirm_transaction'),
    path('get_services/', views.get_services, name='get_services'),

]

