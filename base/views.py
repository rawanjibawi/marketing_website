from django.shortcuts import render, redirect
from items.models import Category, Item
from django.contrib.auth import authenticate, login, logout
# Create your views here.
from .forms import SignUpForm, LoginForm
import random
from rest_framework.decorators import api_view

@api_view()
def home(request):
    available_item_ids = Item.objects.filter(is_sold=False).values_list('id', flat=True) # get all the id's
    # Shuffle the list of item IDs randomly
    random_item_ids = random.sample(list(available_item_ids), min(6, len(available_item_ids))) # shuffle id's, sample give you a new id everytime
    # The id__in is a Django query filter that is used to filter query results based on a list of specific IDs
    items = Item.objects.filter(id__in=random_item_ids)
    categories = Category.objects.all() # show all the categories available
    return render(request, 'home.html', {
        'categories': categories,
        'items': items,
    }) # to use them in our templates we have to pass them as objects

def show_all(request):
    items = Item.objects.filter(is_sold=False)
    return render(request, 'items.html', {
        "items": items
    })

def contact(request):
    return render(request, 'contact.html', {}) # return keyword is very important else it will cause an error

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('/login/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html',{
        'form':form
    })

# Login
def login_view(request):
    form = LoginForm()
    if request.method == 'POST': # user submit the form
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is None: # doesn't exist
            form = LoginForm() # this will allow us to access the {{ form.username }}
            context={"Error": "Invalid username or password."}
            return render(request, 'login.html', {"context":context, "form":form})

        else:
            login(request, user) # if user exist login
            return redirect('/')
    
    return render(request, 'login.html', {"form": form})


def logout_view(request):
  if request.method == 'GET':
    logout(request)
    return redirect('/')
