from django.urls import path

from django.contrib.auth import views as auth_views
from .views import loginPage, asset_update
from . import views

urlpatterns = [
    path('', views.home, name="home"),

    path('test/', views.test, name="test"),
    path('regasset/', views.RegAsset, name="register_asset"),
    path('regvendor/', views.RegVendor, name="register_vendor"),

    path('viewasset/', views.viewAsset, name="viewasset"),
    path('view_vendor/', views.viewVendors, name="view_vendor"),

    path('userSetting/', views.UserSetting, name="userSetting"),

    path('messages', views.message_list, name='message_list'),
    path('compose/', views.message_compose, name='message_compose'),
    path('<int:message_id>/', views.message_detail, name='message_detail'),
    path('inbox/', views.inbox, name='inbox'),
    path('<int:message_id>/reply/', views.message_reply, name='message_reply'),

    path('unread_message_count/', views.unread_message_count, name='unread_message_count'),

    path('broadcast_inbox/', views.Broadcast_inbox, name='broadcast_inbox'),












    path('asset/<int:pk>/update/', views.asset_update, name='asset_update'),
   
    #path('updateAsset/<str:pk>/', views.updateAsset, name="updateAsset"),
    #path('updateVendor/<int:pk>/', views.updateVendor, name="updateVendor"),
    path('deleteAsset/<str:pk>/', views.deleteAsset, name="deleteAsset"),
    
    path('users/', views.userPage, name="user-page"),
   
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"),

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),

    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

    path('userdetails/', views.userDetails, name="userdetails"),
    path('userdetails/<int:employee_id>', views.userDetails, name="userdetails"),
    
    #### Reports #####
    path('employeereport/', views.employeeReport, name="employee-report"),
    path('vendorreport/', views.vendorReport, name="vendor-report"),
    path('assetreport/', views.assetReport, name="asset-report"),

    
]