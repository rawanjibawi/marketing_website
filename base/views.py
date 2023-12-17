from django.shortcuts import render, redirect
from items.models import Category, Item
from django.contrib.auth import authenticate, login, logout
# Create your views here.
from .forms import SignUpForm, LoginForm


def home(request):
    items = Item.objects.filter(is_sold=False)[0:6] # we want to get all items that are available and we just want to show 6 of them
    categories = Category.objects.all() # show all the categories available
    return render(request, 'home.html', {
        'categories': categories,
        'items': items,
    }) # to use them in our templates we have to pass them as objects

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


    