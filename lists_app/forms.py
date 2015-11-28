from django import forms
from lists_app.models import Item

EMPTY_ITEM_ERROR = "You can't have an empty list item"

# class ItemForm(forms.Form):
#     text = forms.CharField(
#         # customise the input for a form field
#         widget=forms.fields.TextInput(attrs={
#             'placeholder': 'Enter a to-do item',
#             'class': 'form-control input-lg',
#         }),
#     )

class ItemForm(forms.models.ModelForm):
    # ModelForm is Django-provide, a special class which can auto-generate a
    # form for a model. It's configured with Meta.
    # In Meta we specify which model the form is for, and which fields we
    # want it to use.
    class Meta:
        model = Item
        fields = ('text',)

class ItemForm(forms.models.ModelForm):

    class Meta:
        # override widgets for ModelForm fields, similarly with the normal form
        model = Item
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(attrs={
                'placeholder': 'Enter a to-do item',
                'class': 'form-control input-lg',
            }),
        }
        error_messages = {
            'text': {'required': EMPTY_ITEM_ERROR}
        }