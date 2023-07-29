from django.shortcuts import redirect

def authenticate_user(allowed_roles=None):
    """
    Decorator for redirecting users to appropriate pages after login.
    """
    if allowed_roles is None:
        allowed_roles = []

    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.is_authenticated:
                # Redirect user to appropriate page based on group membership
                if request.user.groups.filter(name__in=allowed_roles).exists():
                    # User is in one of the allowed groups
                    return redirect('admin:index')
                else:
                    # User is not in any allowed group
                    return redirect('home')
            else:
                # User is not authenticated, redirect to login page
                return redirect('login')
        return wrapper_func
    return decorator
