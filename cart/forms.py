from django import forms


class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=100, label="Повне ім'я")
    email = forms.EmailField(label='Email')
    phone = forms.CharField(max_length=20, label='Телефон')
