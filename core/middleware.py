from django.shortcuts import redirect
from django.contrib import messages

class RestrictAdminMiddleware:
    """
    Restricts access to `/admin/` to only superusers.
    Normal staff must use the Custom Staff Dashboard.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/'):
            if not request.user.is_authenticated:
                messages.warning(request, "Please log in to access the system.")
                return redirect('users:login')
            if not request.user.is_superuser:
                messages.error(request, "Access denied. The default admin panel is restricted.")
                return redirect('portfolio:home')
        
        response = self.get_response(request)
        return response
