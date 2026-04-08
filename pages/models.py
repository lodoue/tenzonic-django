import datetime
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify

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

    def was_created_recently(self):
        return self.created_on >= timezone.now() - datetime.timedelta(days=1)
    
    # Returns a list of (field_name, field_value) tuples
    def get_fields(self):
        # Check if method name 'exclude_fields' exist and its executable
        if hasattr(self, 'exclude_fields') and callable(getattr(self, 'exclude_fields')):
            # Returns field_names excluding field name returned by exclude_fields() method
            return [(field.name, getattr(self, field.name), field.verbose_name) for field in self._meta.fields if field.name not in self.exclude_fields(self)]
        else:
            return [(field.verbose_name, getattr(self, field.name)) for field in self._meta.fields]
    
    def get_model_name(self):
        return self._meta.verbose_name

# Domain model
class Domain(BaseModel):
    class Meta:
        verbose_name = "Domain"
        verbose_name_plural = "Domains"

    # Domain fields
    name = models.CharField(null=True)
    icon = models.CharField(default='bi bi-images')
    # Related fields
    user = models.ForeignKey(User, on_delete=models.CASCADE)

# Service model
class Service(BaseModel):
    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"

    # Service fields
    name = models.CharField(null=True)
    description = models.CharField(null=True)
    image = models.ImageField(default='default.jpg', upload_to='service_pics')
    # Related fields
    user = models.ForeignKey(User, on_delete=models.CASCADE)

# Profile model
class Profile(BaseModel):
    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    # Profile fields
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    # Related fields settings.AUTH_USER_MODEL
    user = models.OneToOneField(User, on_delete=models.CASCADE)

# Contact model
class Contact(BaseModel):
    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"

    def exclude_fields(self):
        return ('id','created_on','modified_on','message','firstname','lastname')
    
    def search_fields(self):
        return ('firstname','lastname')
    
    def __str__(self):
        return self.message

    # Contact fields
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
    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    def exclude_fields(self):
        return ('id','created_on','modified_on')
    
    def search_fields(self):
        return ('rated','comment')

    # Review fields
    rated = models.PositiveIntegerField(default=0, verbose_name="Rated")
    comment = models.CharField(null=True, verbose_name="Comment")
    image = models.ImageField(default='default.jpg', upload_to='profile_pics', verbose_name="Image")
    # Related fields
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")

# Blog model
class Blog(BaseModel):
    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"

    def __str__(self):
        return self.title
    
    def exclude_fields(self):
        return ('id','created_on','modified_on')
    
    def search_fields(self):
        return ('title','description')

    # Blog fields
    title = models.CharField(
        verbose_name="Title"
    )
    url = models.URLField(
        verbose_name="URL",
        unique=True, 
        null=True,
        blank=True
    )
    description = models.CharField(
        verbose_name="Description"
    )
    image = models.FileField(
        verbose_name="Image",
        upload_to='images', 
        blank=True
    )
    # Related fields
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    reviews = models.ManyToManyField(Review, related_name='blogs', verbose_name="Review")

    def save(self, *args, **kwargs):
        # Use slugified title as url if its empty then save it
        if not self.url and self.title:
            self.url = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)


