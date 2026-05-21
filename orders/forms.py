from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class CheckoutForm(forms.Form):
    # User fields (Only required if guest)
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input'}), required=False)
    first_name = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-input'}))
    phone_number = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-input'}))

    # Shipping fields
    city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-input'}))
    neighborhood = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-input'}))
    street_address = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-input'}))
    delivery_notes = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-input', 'rows': 3}), required=False)
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if self.request and not self.request.user.is_authenticated:
            self.fields['email'].required = True
            self.fields['password'].required = True
            self.fields['first_name'].required = True
            self.fields['phone_number'].required = True

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.request and not self.request.user.is_authenticated:
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("An account with this email already exists. Please log in first.")
        return email
