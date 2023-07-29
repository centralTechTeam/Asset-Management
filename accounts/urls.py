from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.Home, name="admin_page"),

    path('regassettype/', views.RegAssetType, name="register_asset_type"),
    path('view_asset_type/', views.viewAssetType, name="view_asset_type"),
    path('asset_type/<str:assettype_id>/edit/', views.edit_asset_type, name='edit_asset_type'),
    path('asset_type/<str:assettype_id>/delete/', views.delete_asset_type, name='delete_asset_type'),

    path('regassigngroup/', views.RegAssignGroup, name="register_assign"),
    path('view_assign/', views.viewAssignType, name="view_assign"),
    path('assign/<str:assign_id>/edit/', views.edit_assign, name='edit_assign'),
    path('assign/<str:assign_id>/delete/', views.delete_assign, name='delete_assign'),

    path('regemployee/', views.RegEmployee, name="register_employee"),
    path('view_employee/', views.viewEmployee, name="view_employee"),
    path('employee/<str:employee_id>/edit/', views.edit_employee, name='edit_employee'),
    path('employee/<str:employee_id>/delete/', views.delete_employee, name='delete_employee'),

    path('view_assets/', views.viewAssetData, name="view_assets"),
    path('view_vendors/', views.viewVendorsData, name="view_vendors"),
    path('asset/<str:asset_id>/edit/', views.edit_asset, name='edit_asset'),
    path('asset/<str:asset_id>/delete/', views.delete_asset, name='delete_asset'),

    path('reg_user/', views.add_user, name="reg_user"),
    path('view_users/', views.list_users, name="view_users"),

    path('reg_group/', views.create_group, name="reg_group"),
    path('view_group/', views.viewGroups, name="view_group"),

    path('groups/<str:group_id>/edit/', views.edit_group, name='edit_group'),
    path('groups/<str:group_id>/delete/', views.delete_group, name='delete_group'),

    path('users/<int:user_id>/edit/', views.edit_user, name='edit_user'),
    path('users/<int:user_id>/delete/', views.delete_user, name='delete_user'),

    path('UserProfile/', views.UserProfile, name="UserProfile"),

    path('logout/', views.logout_view, name='logout'),

    path('message_list', views.admin_message_list, name='message_list'),

    path('message_list/<int:message_id>/', views.user_message_detail, name='user_message_detail'),
    
    path('reply/<int:message_id>/', views.message_reply, name='message_reply'),

    path('sent_message/<int:user_id>/', views.sent_message_list, name='sent_message'),
    path('compose_message/', views.compose_message, name='compose_message'),

    path('broadcast_message/', views.broadcast_message, name='broadcast_message'),
    path('sent_broadcast_message/<int:user_id>/', views.sent_broadcast_message, name='sent_broadcast_message'),
    path('broadcast_message/<int:message_id>/', views.broadcast_message_detail, name='broadcast_message_detail'),

    path('employeereport/', views.employeeReport, name="employee-report"),
    path('vendorreport/', views.vendorReport, name="vendor-report"),
    path('assetreport/', views.assetReport, name="asset-report"),



    path('asset/<str:pk>/update/', views.edit_asset, name='asset_update'),
]