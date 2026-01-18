from django import forms
from .models import category, product, profile


class ProductForm(forms.ModelForm):
    class Meta:

        model = product
        exclude = ['us']
        # fields = '__all__'
        # fields = ['name', 'description', 'price', 'img1', 'cat']


class categoryform(forms.ModelForm):
    class Meta:
        model = category
        fields = '__all__'


class editproductform(forms.ModelForm):
    class Meta:
        model = product
        # fields = '__all__'
        exclude = ['us']


class profileform(forms.ModelForm):
    class Meta:
        model = profile
        exclude = ['us']
