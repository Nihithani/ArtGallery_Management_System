from django import forms

class OrderForm(forms.Form):
    shipping_address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}), label='Shipping Address')
    

