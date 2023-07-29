from django.contrib.auth.backends import ModelBackend
from django.shortcuts import redirect

class CustomAuthBackend(ModelBackend):
    def user_can_authenticate(self, user):
        # Ensure that the user is active and not deleted.
        return super().user_can_authenticate(user) and not user.is_deleted

    def get_user(self, user_id):
        try:
            return self.model.objects.get(pk=user_id)
        except self.model.DoesNotExist:
            return None

    def authenticate(self, request, username=None, password=None, **kwargs):
        user = super().authenticate(request, username=username, password=password, **kwargs)

        if user is not None and user.is_superuser:
            return redirect('login')

        return user

#####################################   #########################################

from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.groups.filter(name='admin').exists():
                return redirect('admin-index')
            else:
                return redirect('home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')
        return wrapper_func
    return decorator

def super_user(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = 'super_admin'
            if request.user.groups.exists():
              if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not a super user')
        return wrapper_func
    return decorator

def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'users':
            return redirect('user-page')

        if group == 'admin':
            return view_func(request, *args, **kwargs)
        
        return HttpResponse("You don't have the permission to access this page", status=403)

    return wrapper_function