from django.contrib import admin

# Register your models here.
from .models import Contact, Blog, Review

class ContactAdmin(admin.ModelAdmin):
    list_display = ("title", "firstname", "lastname", "gender", "email", "mobile", "subject", "message", "pin",)

admin.site.register(Contact, ContactAdmin)

class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "url", "description", "image",)

admin.site.register(Blog, BlogAdmin)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ("rated", "comment", "image",)

admin.site.register(Review, ReviewAdmin)