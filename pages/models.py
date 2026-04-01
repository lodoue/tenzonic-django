import datetime
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils import timezone
from django.contrib.auth.models import User

# Define title choices
TITLE_CHOICES = (
    ('mr', 'Mr.'),
    ('mrs', 'Mrs.'),
    ('ms', 'Ms.'),
    ('miss', 'Miss'),
    ('dr', 'Dr.')
)

# Define gender choices
GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
    ('P', 'Prefer not to say'),
)

def validate_pin_length(value):
    if len(str(value)) != 6:
        raise ValidationError('Pin code should be exactly 6 digits.')
    
# Define Parent Model
class BaseModel(models.Model):
    # Below fields will be automatically added to Models which are derived from this model
    created_on = models.DateTimeField(default=timezone.now, verbose_name="Created On")
    modified_on = models.DateTimeField(auto_now=True, verbose_name="Updated On")
    # Add any other common fields here

    class Meta:
        abstract = True
        # Optional: set default ordering for all child models
        ordering = ("-created_on",)

    def __str__(self):
        return self.message
    
    def was_created_recently(self):
        return self.created_on >= timezone.now() - datetime.timedelta(days=1)
    
    def get_fields(self):
        # Returns a list of (field_name, field_value) tuples
        return [(field.verbose_name, getattr(self, field.name)) for field in self._meta.fields]

# Profile model
class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    

# Contact model
class Contact(BaseModel):
    class Meta:
        verbose_name = "Contact"
        verbose_name_plural="Contacts"

    title = models.CharField(
        max_length=5,
        verbose_name="Title",
        choices=TITLE_CHOICES
    )
    firstname = models.CharField(
        max_length=10,
        verbose_name="First Name",
        help_text='Enter your first name'
    )
    lastname = models.CharField(
        max_length=10,
        verbose_name="Last Name",
        help_text='Enter your last name'
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        verbose_name="Gender",
        default='M', # Set a default value if needed
        help_text='Select your gender'
    )
    email = models.EmailField(
        # default='tenzin@test.com',
        unique=True,
        verbose_name="Email",
        help_text='Enter your email'
    )
    mobile = models.CharField(
        max_length=10,
        verbose_name="Mobile",
        validators=[RegexValidator(regex=r'^\d{10}$')],
        unique=True,
        help_text='Enter your 10 digit mobile number'
    )
    subject = models.CharField(
        max_length=100,
        verbose_name="Subject",
        default='Dummy Subjects', # Set a default value if needed
    )
    message = models.CharField(
        verbose_name="Message",
    )
    pin = models.PositiveIntegerField(
        verbose_name="Postal Code",
        validators=[validate_pin_length],
        help_text='Enter 6 digit pin code'
    )
    # profile_img = models.ImageField(upload_to='profile_img', blank=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"
    

# Review model
class Review(BaseModel):
    rated = models.PositiveIntegerField(),
    comment = models.CharField(),
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

# Blog model
class Blog(BaseModel):
    title = models.CharField(
        max_length=5,
        choices=TITLE_CHOICES
    )
    message = models.CharField()
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.FileField(upload_to='images', blank=True)

