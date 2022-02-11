from django.shortcuts import render, redirect
from lists.models import Item, List
from django.core.exceptions import ValidationError

def home_page(request):
    return render(request, 'home.html')

def view_list(request, list_id):
    list_to_view = List.objects.get(id=list_id)
    return render(request, 'list.html', {'list': list_to_view})

def new_list(request):
    list_new = List.objects.create()
    item = Item.objects.create(text=request.POST['item_text'], list=list_new)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_new.delete()
        error = "You can't have an empty list item"
        return render(request, 'home.html', {"error": error})
    return redirect(f'/lists/{list_new.id}/')

def add_item(request, list_id):
    list_to_modify = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_to_modify)
    return redirect(f'/lists/{list_to_modify.id}/')