from django.shortcuts import render, redirect
from django.urls import reverse
from items.models import Category, Item
from django.contrib.auth import authenticate, login, logout, get_user_model
# Create your views here.
from .forms import SignUpForm, LoginForm
import random
from rest_framework.decorators import api_view
from django.contrib import messages # it is used to send messages between views and templates
from django.utils.html import mark_safe # used to add python variable inside an html inside a string in python
# packages needed for email verification
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from .tokens import account_activation_token # this is taken from token.py
from django.utils.encoding import force_str
# cache home page, browser page for fast loading
from django.views.decorators.cache import cache_page # use it if you want to cache pages of different url
from django.core.cache import cache


isEmailSend = False
def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
    
        messages.success(request, "Thank you for email confirmation. Now login to your account.")
        login_url = reverse('login') # this will pass url as absolute path, not depending to the previous path
        return redirect(login_url)
    
    else:
        messages.error(request, "Activation link is invalid!, try again")
        login_url = reverse('signup') # this will pass url as absolute path, not depending to the previous path
        return redirect(login_url)

# this view function will be called in signup
def activateEmail(request, user, to_email):
    # code to send email will be written here
     mail_subject = "Activate your account"
     message = render_to_string( # convert html template to string
         'email_template.html',
         {
         'user': user.username,
         'domain': get_current_site(request).domain,
         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
         'token': account_activation_token.make_token(user),
         "Protocol":'https' if request.is_secure() else 'http'
         }
     )
     email = EmailMessage(mail_subject, message, to={to_email})
     print(email)
     if email.send(): # check if email send
        print("success email") 
        messages.success(
            request, f"Dear {user}</b> please verify your account by clicking on activation link in your email")
     else:
        messages.error(
            request, f"Problem sending email, check if you typed your email correctly")
@api_view()
def home(request):
    if cache.get('home_cache'):
        print("the content is cached")
    else:
        print("the content is not cached")
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
            user = form.save(commit=False) # we want to send email request, and then save it
            user.is_active = False # by default it's true, but we want it unactive tell user accept email verification
            user.save() # save user to database
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('/signup/')
    else:
        # since we have mark_safe we have to add |safe in the template
        # if isEmailSend:
        #     print("hello")
        #     messages.success(request, f"Dear {user}</b> please verify your account by clicking on activation link in your email")
        # else:
        #     print("world")
        #     messages.error(request, f"Problem sending email, check if you typed your email correctly")
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

# cache home page, browser page for fast loading

# cache home page for images only


# @cache_page(3600, key_prefix='home_cache')
# def view1(request):
#     context = {}
#     return render(request, 'home.html', context)


# @cache_page(3600, key_prefix='browse_cache')
# def view1(request):
#     context = {}
#     return render(request, 'items.html', context)


# # check if it cached or not
# if cache.get('home_cache'):
#     print('View 1 content is in the cache.')
# else:
#     print("not cached")
