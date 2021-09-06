from django.contrib import messages
from django.shortcuts import redirect, render
import bcrypt
from .models import User


def logout(request):
    if 'user' in request.session:
        del request.session['user']
    
    return redirect("/")
    

def login(request):
    if request.method == 'GET':
        if 'user' in request.session:
            messages.warning(request,"Ya estás logeado.")
            return redirect("/")

    if request.method == "POST":
        print(request.POST)
        user = User.objects.filter(email=request.POST['email'])
        if user:
            log_user = user[0]

            if bcrypt.checkpw(request.POST['password'].encode(), log_user.password.encode()):

                user = {
                    "id" : log_user.id,
                    "first_name": f"{log_user}",
                    "last_name":log_user.last_name,
                    "email": log_user.email,
                    "role": log_user.role
                }

                
                request.session['user'] = user
                messages.success(request, "Logueado correctamente.")
                return redirect("/")
            else:
                messages.error(request, "Password o Email  incorrectos.")
        else:
            messages.error(request, "Email o password incorrectos.")



        return redirect("/login")
    else:
        return render(request, 'login.html')


def registro(request):
    if request.method == "POST":

        errors = User.objects.validador_basico(request.POST)
        # print(errors)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                # print("DESDE EL FOR: ",key, value)
            
            request.session['register_first_name'] =  request.POST['first_name']
            request.session['register_email'] =  request.POST['email']

        else:
            request.session['register_first_name'] = ""
            request.session['register_email'] = ""

            password_encryp = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode() 

            usuario_nuevo = User.objects.create(
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                email=request.POST['email'],
                password=password_encryp,
                role=request.POST['role']
            )

            messages.success(request, "El usuario fue agregado con exito.")
            

            request.session['user'] = {
                "id" : usuario_nuevo.id,
                "first_name": f"{usuario_nuevo.first_name}",
                "last_name": f"{usuario_nuevo.last_name}",
                "email": usuario_nuevo.email
            }
            return redirect("/")

        return redirect("/registro")
    else:
        return render(request, 'registro.html')
