# In forms.py (for a ModelForm)
from django import forms
# from django.forms import Form, ModelForm, ChoiceField, Select, TextInput, Textarea, RadioSelect, EmailInput, ValidationError
from .models import Contact, TITLE_CHOICES, GENDER_CHOICES

# Class ContactForm
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('title', 'firstname', 'lastname', 'gender', 'email', 'mobile', 'subject', 'message', 'pin')
        widgets = {
            'title': forms.Select(choices=TITLE_CHOICES),
            'firstname': forms.TextInput,
            'lastname': forms.TextInput,
            'gender': forms.RadioSelect(choices=GENDER_CHOICES),
            'email': forms.EmailInput,
            'mobile': forms.TextInput,
            'subject': forms.TextInput,
            'message': forms.Textarea(attrs={'rows': 3, 'cols': 10}),
        }
   

    # # Validating all input fields data
    # def clean(self):
    #     cleaned_data = super().clean()
    #     firstname = cleaned_data.get("firstname")
    #     lastname = cleaned_data.get("lastname")
    #     email = cleaned_data.get("email")
    #     mobile = cleaned_data.get("mobile")
    #     subject = cleaned_data.get("subject")
    #     message = cleaned_data.get("message")

    #     if '@' not in email:
    #         msg = f"@ not in {email}."
    #         self.add_error("email", msg)

    #     if 'test' not in message:
    #         msg = f"'test' not in {message}."
    #         self.add_error("message", msg)

    #     if 'Hello' not in subject:
    #         msg = f"'hello' not in {subject}."
    #         self.add_error("subject", msg)
