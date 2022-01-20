from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns=[
    path('login/',auth_views.LoginView.as_view(template_name='accounts/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('signup/',views.SignUp.as_view(),name='signup'),
    path('search/',views.search_profile,name='search-profile'),
    path('user/<int:pk>', views.user_detail,name='user_detail'),
    path('edit/user/', views.update_profile,name='edit_profile'),
    path('send_friend_request/<int:userID>/', views.send_friend_request, name='send_friend_request'),
    path('cancel_friend_request/<int:userID>/', views.cancel_friend_request, name='cancel_friend_request'),
    path('accept_friend_request/<int:requestID>/', views.accept_friend_request,name='accept_friend_request'),
    path('unfriend/<int:userID>/', views.unfriend,name='unfriend'),
    path('friends/<int:user_id>/', views.friends_list,name='user_friend_list'),
    path('friend_list/', views.distance,name='distance')

]
