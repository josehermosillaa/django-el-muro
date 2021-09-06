from django.db import models
import re

# Create your models here.
class UserManager(models.Manager):
    def validador_basico(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        SOLO_LETRAS = re.compile(r'^[a-zA-Z. ]+$')

        errors = {}

        if len(postData['first_name']) < 2:
            errors['firstname_len'] = "nombre debe tener al menos 2 caracteres de largo";

        
        if len(postData['last_name']) < 2:
            errors['lastname_len'] = "Apellido debe tener al menos 2 caracteres de largo";

        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "correo invalido"

        if not SOLO_LETRAS.match(postData['first_name']):
            errors['solo_letras'] = "solo letras en nombre porfavor"
        
        if not SOLO_LETRAS.match(postData['last_name']):
            errors['solo_A_letras'] = "solo letras en apellidos porfavor"

        if len(postData['password']) < 4:
            errors['password'] = "contraseña debe tener al menos 8 caracteres";

        if postData['password'] != postData['password_confirm'] :
            errors['password_confirm'] = "contraseña y confirmar contraseña no son iguales. "

        
        return errors

class CommentManager(models.Manager):
    def basic_validator(self, postData):

        # errors dictionnary
        errors = {}
        
        # checking first name
        if len(postData['comment']) == 0:
            errors['comment'] = "No se permiten comentarios vacios "
            
        return errors

class User(models.Model):
    CHOICES = (
        ("user", 'User'),
        ("admin", 'Admin')
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    role = models.CharField(max_length=255, choices=CHOICES)
    password = models.CharField(max_length=70)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return f"{self.first_name}"

    def __repr__(self):
        return f"{self.first_name}"

class MessageManager(models.Manager):
    def basic_validator(self, postData):

        # errors dictionnary
        errors = {}
        
        # checking first name
        if len(postData['message']) == 0:
            errors['message'] = "El mensaje no puede estar vacio"
            
        return errors
                

class Message(models.Model):
    message = models.TextField()
    user = models.ForeignKey(User, related_name='messages', on_delete = models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = MessageManager()    
    
    def __str__(self):
        return f"{self.message}"
def __repr__(self):
        return f"Message: (ID: {self.id}) -> {self.user} {self.message}"

class Comment(models.Model):
    comment = models.TextField()
    message = models.ForeignKey(Message, related_name='comments', on_delete = models.CASCADE)
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)   
    objects = CommentManager()
    def __repr__(self):
        return f"Comment: (ID: {self.id}) -> {self.comment}"  
