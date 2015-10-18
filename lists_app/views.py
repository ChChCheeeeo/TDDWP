from django.shortcuts import render
from django.http import HttpResponse
from lists_app.models import Item

def home_page(request):
    # We use a variable called new_item_text, which will either hold
    # the POST contents, or the empty string.
    # .objects.create is a neat shorthand for creating a new Item,
    # without needing to call .save(). 
    if request.method == 'POST':
        new_item_text = request.POST['item_text']  #1
        Item.objects.create(text=new_item_text)  #2
    else:
        new_item_text = ''  #3

    return render(request, 'home.html', {
        'new_item_text': new_item_text,  #4
    })