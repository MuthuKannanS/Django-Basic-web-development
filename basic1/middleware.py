from django.urls import reverse
from django.shortcuts import redirect
class RedirectAuthenticatedMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response
		
	def __call__(self,request):
		#user authenticated cheking
		if request.user.is_authenticated:
			#list of paths to cheking
			paths_to_redirect = [reverse('blog:login'),reverse('blog:register')]
			
			if request.path in paths_to_redirect:
				return redirect(reverse('blog:dashboard'))#change to home
				
				
		response = self.get_response(request)
		return response

class RestrictUnauthenticatedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        restricted_path = [reverse('blog:dashboard')]
        
        if not request.user.is_authenticated and request.path in restricted_path:
            return redirect(reverse('blog:login'))
        
    
    
        response = self.get_response(request)
        return response    
        
        