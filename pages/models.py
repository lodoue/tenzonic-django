import datetime
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils import timezone

# Define title choices
CHOICES = {
    'titles': (
        ('mr', 'Mr.'),
        ('mrs', 'Mrs.'),
        ('ms', 'Ms.'),
        ('miss', 'Miss'),
        ('dr', 'Dr.')
    ),
    'genders': (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('P', 'Prefer not to say'),
    )
}

def validate_pin_length(value):
    if len(str(value)) != 6:
        raise ValidationError('Pin code should be exactly 6 digits.')
    
class BaseModel(models.Model):
    created_on = models.DateTimeField(default=timezone.now)
    modified_on = models.DateTimeField(auto_now=True)
    # Add any other common fields here

    class Meta:
        abstract = True
        # Optional: set default ordering for all child models
        ordering = ("-created_on",)

    def __str__(self):
        return self.message
    
    def was_created_recently(self):
        return self.created_on >= timezone.now() - datetime.timedelta(days=1)

# Contact models
class Contact(BaseModel):
    TITLE_CHOICES=CHOICES['titles']
    GENDER_CHOICES=CHOICES['genders']

    title = models.CharField(
        max_length=5,
    )
    firstname = models.CharField(
        max_length=10,
        help_text='Enter your first name'
    )
    lastname = models.CharField(
        max_length=10,
        help_text='Enter your last name'
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default='M', # Set a default value if needed
        help_text='Select your gender'
    )
    email = models.EmailField(
        # default='tenzin@test.com',
        help_text='Enter your email'
    )
    mobile = models.CharField(
        max_length=10,
        validators=[RegexValidator(regex=r'^\d{10}$')],
        help_text='Enter your 10 digit mobile number'
    )
    subject = models.CharField(
        max_length=100,
        default='Dummy Subjects', # Set a default value if needed
    )
    message = models.CharField()
    
    pin = models.PositiveIntegerField(
        validators=[validate_pin_length],
        help_text='Enter 6 digit pin code'
    )
    # profile_img = models.ImageField(upload_to='profile_img', blank=True)
    # my_file = models.FileField(upload_to='doc', blank=True)
