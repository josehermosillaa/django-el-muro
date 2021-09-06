from django.shortcuts import redirect
from django.contrib import messages

def login_required(function):

    def wrapper(request, *args,**kargs):
        if 'user' not in request.session:
            messages.error(request, "Debes loguearte para ingresar.")
            return redirect('/login')
        resp = function(request, *args,**kargs)
        
        return resp
    
    return wrapper