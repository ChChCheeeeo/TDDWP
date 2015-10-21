from django.shortcuts import redirect, render
from django.http import HttpResponse
from lists_app.models import Item

def home_page(request):
    # redirect to homepage after savign contents from POST
    # this solves error 200 != 302
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/lists/the-only-list-in-the-world/')
    # so can list all items
    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})

def view_list(request):
    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})