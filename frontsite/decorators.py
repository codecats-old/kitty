def anonymous_required(function=None, redirect_field_name='frontsite:index'):
    def decorator(request, redirect_field_name=redirect_field_name, *args, **kwargs):
        if request.user.is_authenticated() is True:
            from django.shortcuts import redirect
            return redirect(redirect_field_name)
        return function(request)
    return decorator
def login_required(function=None, redirect_field_name='frontsite:login'):
    def decorator(request, redirect_field_name=redirect_field_name, *args, **kwargs):
        if request.user.is_authenticated() is False:
            from django.shortcuts import redirect
            return redirect(redirect_field_name)
        return function(request)
    return decorator