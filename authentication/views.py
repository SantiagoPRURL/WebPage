from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
import json
from validate_email import validate_email
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.

class EmailValidationView(View): 
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        
        if not validate_email(email):
            return JsonResponse({'email_error':'Email not is valid'}, status=400)
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({'username_error':'username is used for other user'}, status=400)        
        return JsonResponse({'email_valid': True})
    
    
class UsernameValidationView(View): 
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        
        if not str(username).isalnum():
            return JsonResponse({'username_error':'username should only contain alphanumeric characters'}, status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'username is used for other user'}, status=400)        
        return JsonResponse({'username_valid': True})
    
    

class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
    
    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']


        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'authentication/register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already taken')
            return render(request, 'authentication/register.html')
        
        if len(password) < 6:
            messages.error(request, 'Password is too short')
            return render(request, 'authentication/register.html')
        
        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.is_active = True
        user.save()
        
        messages.success(request, 'User created successfully. Please check your email to activate your account.')
        print('CREADO')
        
        return render(request, 'authentication/register.html')
        

class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        print("Usuario Entro y listo para mostrar")
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in.')
            return redirect('expenses')  
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'authentication/login.html')
           

class Logoutview(View):
    def post(self, request):
        logout(request)  
        messages.success(request, "You have successfully logged out.")
        return redirect('login')  
            
        
        
        
        
        