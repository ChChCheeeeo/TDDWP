# from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

from lists_app.forms import ExistingListItemForm, ItemForm
from lists_app.models import List #,Item, List

from lists_app.forms import ExistingListItemForm, ItemForm, NewListForm
from lists_app.models import List #,Item

from django.contrib.auth import get_user_model
User = get_user_model()


def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})

# def new_list(request):
#     list_ = List.objects.create()
#     item = Item.objects.create(text=request.POST['text'], list=list_)
#     item.full_clean()
#     return redirect('/lists/%d/' % (list_.id,))

# def new_list(request):
#     list_ = List.objects.create()
#     item = Item.objects.create(text=request.POST['text'], list=list_)
#     try:
#         item.full_clean()
#     except ValidationError:
#         error = "You can't have an empty list item"
#         return render(request, 'home.html', {"error": error})
#     return redirect('/lists/%d/' % (list_.id,))

# def new_list(request):
#     list_ = List.objects.create()
#     item = Item(text=request.POST['text'], list=list_)
#     try:
#         item.full_clean()
#         item.save()
#     except ValidationError:
#         list_.delete()
#         error = "You can't have an empty list item"
#         return render(request, 'home.html', {"error": error})
#     return redirect(list_)
    # return redirect('/lists/%d/' % (list_.id,))
    #return redirect('view_list', list_.id)
# def new_list(request):
#     # pass the request.POST data into the form’s constructor. 
#     form = ItemForm(data=request.POST)
#     if form.is_valid():
#         list_ = List.objects.create()
#         Item.objects.create(text=request.POST['text'], list=list_)
#         return redirect(list_)
#     else:
#         # invalid - pass the form down to the template, instead of
#         # our hardcoded error string
#         return render(request, 'home.html', {"form": form})
def new_list(request):
    form = NewListForm(data=request.POST)
    if form.is_valid():
        list_ = form.save(owner=request.user)
        return redirect(list_)
    else:
        return render(request, 'home.html', {"form": form})

# def view_list(request, list_id):
#     list_ = List.objects.get(id=list_id)
#     if request.method == 'POST':
#         Item.objects.create(text=request.POST['text'], list=list_)
#         return redirect('/lists/%d/' % (list_.id,))
#     return render(request, 'list.html', {'list': list_})

# def view_list(request, list_id):
#     list_ = List.objects.get(id=list_id)
#     error = None

#     if request.method == 'POST':
#         try:
#             item = Item(text=request.POST['text'], list=list_)
#             item.full_clean()
#             item.save()
#             return redirect(list_)
#         except ValidationError:
#             error = "You can't have an empty list item"
#     form = ItemForm()
#     return render(request, 'list.html', {
#         'list': list_, "form": form, "error": error
#     })
        #     item.save()
        #     return redirect('/lists/%d/' % (list_.id,))
        # except ValidationError:
        #     error = "You can't have an empty list item"

    # return render(request, 'list.html', {'list': list_, 'error': error})
# def view_list(request, list_id):
#     # You can&#39;t have an empty list item
#     # found in as part of forms.
#     list_ = List.objects.get(id=list_id)
#     form = ItemForm()
#     if request.method == 'POST':
#         form = ItemForm(data=request.POST)
#         if form.is_valid():
#             Item.objects.create(text=request.POST['text'], list=list_)
#             return redirect(list_)
#     return render(request, 'list.html', {'list': list_, "form": form})
def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()#for_list=list_)
            return redirect(list_)
    return render(request, 'list.html', {'list': list_, "form": form})

# def add_item(request, list_id):
#     list_ = List.objects.get(id=list_id)
#     Item.objects.create(text=request.POST['text'], list=list_)
#     return redirect('/lists/%d/' % (list_.id,))


def my_lists(request, email):
    owner = User.objects.get(email=email)
    return render(request, 'my_lists.html', {'owner': owner})

def share_list(request, list_id):
    # find list and redirect to it
    list_ = List.objects.get(id=list_id)
    list_.shared_with.add(request.POST['email'])
    return redirect(list_)