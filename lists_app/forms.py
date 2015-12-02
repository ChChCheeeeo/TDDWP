from django import forms
from lists_app.models import Item
from django.core.exceptions import ValidationError

EMPTY_ITEM_ERROR = "You can't have an empty list item"
DUPLICATE_ITEM_ERROR = "You've already got this in your list"

# class ItemForm(forms.Form):
#     text = forms.CharField(
#         # customise the input for a form field
#         widget=forms.fields.TextInput(attrs={
#             'placeholder': 'Enter a to-do item',
#             'class': 'form-control input-lg',
#         }),
#     )

# class ItemForm(forms.models.ModelForm):
#     # ModelForm is Django-provide, a special class which can auto-generate a
#     # form for a model. It's configured with Meta.
#     # In Meta we specify which model the form is for, and which fields we
#     # want it to use.
#     class Meta:
#         model = Item
#         fields = ('text',)

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
    def save(self, for_list):
        # .instance attribute on a form represents the database object
        # that is being modified or created. 
        self.instance.list = for_list
        return super().save()

class ExistingListItemForm(ItemForm):
    def __init__(self, for_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.list = for_list


    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
            self._update_errors(e)