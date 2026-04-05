# In forms.py (for a ModelForm)
from django import forms
# from django.forms import Form, ModelForm, ChoiceField, Select, TextInput, Textarea, RadioSelect, EmailInput, ValidationError
from .models import Contact, Blog, Review, TITLE_CHOICES, GENDER_CHOICES

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
        # exclude = ('field_to_remove',)
   

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

# Class BlogForm
class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'description', 'image', 'url')
        widgets = {
            'title': forms.TextInput,
            'description': forms.Textarea(attrs={'rows': 3, 'cols': 10}),
            'image': forms.FileInput,
            'url': forms.TextInput
        }

# Class ReviewForm
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rated', 'comment', 'image')
        widgets = {
            'rated': forms.TextInput,
            'comment': forms.Textarea(attrs={'rows': 3, 'cols': 10}),
            'image': forms.FileInput
        }