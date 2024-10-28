from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.user_signup, name='user_signup'),
    path('login/', auth_views.LoginView.as_view(template_name='auction/login.html'), name='user_login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='user_login'), name='user_logout'),
    path('auctionlist', views.auction_list, name='auction_list'),
    path('auction/<int:auction_id>/', views.auction_detail, name='auction_detail'),
    path('auction/<int:auction_id>/bid/', views.place_bid, name='place_bid'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact_us, name='contact_us'),
    path('create_auction/', views.create_auction, name='create_auction'),
]