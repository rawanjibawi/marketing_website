from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, Category
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import NewItemForm, EditItemForm
# Create your views here.


# Browse, take all the items that aren't sold

def items(request):
    # search
    # when clicking on search it will create a query as GET in the url, to access it we can use the method below
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False)

    # if user select category
    if category_id:
        items = items.filter(category_id=category_id)

    # if query exist (user is searching for an item)
    if query:
        # to search for description as well we use the Q
        # icontains is a seach method for name, i in contains is for insensitive case
        # category is foreign key in items, to be abel to query it you have to specify which column in category you want to search on, in my case is name
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query) | Q(category__name__icontains=query))  
    return render(request, 'home.html', {"items": items, 'query': query, 'categories': categories, 'category_id': int(category_id)})


def detail(request, id):
    item = get_object_or_404(Item, pk=id) # retrive data who's id is in pk
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=id)[0:3] # add other options of same category but exclude the one you are already in
    return render(request, 'detail.html', {
        'item':item,
        'related_items': related_items
    })
    
    
# add item
@login_required # if you weren't authenticated you will have to go to the login page
def add_item(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user # the add-item is always authenticated since we have login_required
            item.save()
            # return the user to the item created
            return redirect('item:detail', id=item.id)
    
    form = NewItemForm()
    is_staff = request.user.is_staff # check if he is is_staff
    return render(request, 'form.html', {"form":form, 'title':"Add Item", "staff":is_staff})


@login_required  # if you weren't authenticated you will have to go to the login page
def edit_item(request, id):
    item = get_object_or_404(Item, pk=id, created_by=request.user)
    if request.method == 'GET':
        form = EditItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save() # directly save since there's no need to specify who's created by we did it on add-item
            # return the user to the item created
            return redirect('item:detail', id=item.id)

    form = EditItemForm(instance=item) # if we didn't specify instance the form will be empty
    is_staff = request.user.is_staff  # check if he is is_staff
    return render(request, 'form.html', {"form": form, 'title': "Edit Item", "staff": is_staff})

@login_required
def delete(request, id):
   # delete items that belongs to you only
    item = get_object_or_404(Item, pk=id, created_by=request.user)
    item.delete()
    return redirect('home')

@login_required
def add_cart(request):
    is_staff = request.user.is_staff # in template, we will check if !is_staff (only Customer I want them to show the add_cart)
    return render(request, 'add_cart.html', {"staff":is_staff})
        