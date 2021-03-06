from django.shortcuts import render, redirect
from lists.models import Item, List
from django.core.exceptions import ValidationError

def home_page(request):
    return render(request, 'home.html')

def view_list(request, list_id):
    list_to_view = List.objects.get(id=list_id)
    error = None

    if request.method == 'POST':
        try:
            item = Item(text=request.POST['item_text'], list=list_to_view)
            item.full_clean()
            item.save()
            return redirect(list_to_view)
        except ValidationError:
            error = "You can't have an empty list item"
        
    return render(request, 'list.html', {'list': list_to_view, 'error': error})

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
    return redirect(list_new)

