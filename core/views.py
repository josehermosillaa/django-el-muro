from django.contrib import messages
from django.shortcuts import redirect, render
import bcrypt
from .decorators import login_required
from .models import*
from .auth import *

@login_required
def index(request):
    
    context = {
        'messages_lista': Message.objects.all()
    }
    return render(request,'index.html',context) #arreglar 
    

@login_required
def wall(request):

    context = {
        'messages_lista': Message.objects.all() #TODO falta revisar el codigo
    }
    
    return render(request, 'wall.html', context) 

@login_required
def post_message(request):
    Message.objects.create(message = request.POST['message'], user = User.objects.get(id = request.session['user']['id']))
    return redirect('/wall')

def post_comment(request, id):
    user = User.objects.get(id = request.session['user']['id'])
    message = Message.objects.get(id = id)
    Comment.objects.create(
        comment = request.POST['comment'],
        user = user,
        message = message,
    )
    return redirect('/wall')


