from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('accounts/register/', views.register_view, name='register'),
    path('track_coin/', views.track_coin_view, name='track_coin'),
    path('delete-coin-ajax/', views.delete_tracked_coin_ajax, name='delete_coin_ajax'),
    path('logout/', views.custom_logout, name='logout'),

    # path('account/login/', views.dashboard, name='login'),

]
