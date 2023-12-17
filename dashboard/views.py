from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
# Create your views here.
from items.models import Item

@login_required
def index(request):
    print("hello dash")
    items = Item.objects.filter(created_by=request.user)
    is_staff = request.user.is_staff #check if user is is staff
    return render(request, 'index.html', {"items":items, "staff":is_staff})
    