from django import forms
from .models import Item
# from django.forms import ModelForm

EMPTY_LIST_ERROR = "You can't have an empty list item"

class ItemForm(forms.models.ModelForm):

  class Meta:
    model = Item
    fields = ['text',]
    widgets = {
      'text' : forms.fields.TextInput(attrs={
        'placeholder': 'Enter a to-do item',
        'class': 'form-control input-lg',
    }),
  }
    error_messages = {
      'text' : {'required': EMPTY_LIST_ERROR}
    }

  def save(self, for_list):
    self.instance.list = for_list
    return super().save()
