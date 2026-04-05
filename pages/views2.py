from django.db.models import F
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from .forms import ContactForm, BlogForm # Import your form class
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Contact, TITLE_CHOICES, GENDER_CHOICES, Blog
from faker import Faker

# Listing all contactus created
def contact_index(request, page=None, count=None):
    # Retrieve all contacts order by modified_on in descending order
    queryset = Contact.objects.all().order_by('-modified_on')

    if queryset:
        # Change count to total records if not set
        if(count is None):
            count = len(queryset)

        paginator = Paginator(queryset, count)

        try:
            # Get the Page object for the requested page number
            list_obj = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            list_obj = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page.
            list_obj = paginator.page(paginator.num_pages)
    else:
        print("Queryset is empty")
        list_obj = None

    # Pass the page object to the template context
    return render(request, "index.html", {"list_template": "list.html", "module": "Contact Us", "list_obj": list_obj, "rec_count": list_obj.number*len(list_obj.object_list), "tags": {'error':'danger','success':'success'}})

# Creating new contactus
def contact_create(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = ContactForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            print(form.cleaned_data)
            form.save()
            messages.success(request, 'Contact created successfully.')
            return redirect('pages:listContactus')
        else:
            messages.error(request, 'Something went wrong while creating new Contact.') 

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ContactForm()

    return render(request, "create.html", {"form": form})

# For viewing contact by its ID
def contact_view(request, contact_id):
    try:
        contact = get_object_or_404(Contact, pk=contact_id)
    except:
        messages.error(request, 'No such contact found.') 
    else:
        label_title = dict(TITLE_CHOICES)
        contact.title = label_title.get(contact.title, "Unknown Title")
        
        label_gender = dict(GENDER_CHOICES)
        contact.gender = label_gender.get(contact.gender, "Unknown Gender")
        return render(request, "view.html", {"contact": contact, "module": "Contact Us" })
        
# For showing edit form or updating form data
def contact_edit(request, contact_id):
    try:
        instance = get_object_or_404(Contact, pk=contact_id)
    except:
        messages.error(request, 'No such contact found.') 
    else:
        # if this is a POST request we need to process the form data
        if request.method == "POST":
            # create a form instance and populate it with data from the request:
            form = ContactForm(request.POST, instance=instance)
            # check whether it's valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required
                print(form.cleaned_data)
                form.save()
                messages.success(request, 'Successfully updated contact.') 
                
                return redirect('pages:listContactus')
            else:
                messages.error(request, 'Error while updating contact.') 
                return render(request, "edit.html", {"form": form,"alert":"Error while updating contact.","module": "Contact Us"})
        else:
            form = ContactForm(instance=instance)
            return render(request, "edit.html", {"form": form, "module": "Contact Us"})

# For deleting one or more contact data
def delete_contact(request, contact_id=None):
    if request.method == "POST":
        contact_ids = request.POST.getlist('contact_ids')

        if(contact_ids is not None and len(contact_ids) > 0):
            # Filter the QuerySet to include only the selected IDs and delete them
            deleted_count, _ = Contact.objects.filter(id__in=contact_ids).delete()

            messages.success(request, f"{deleted_count} contact(s) deleted successfully.")
        else:
            messages.error(request, 'Must select atleast 1 contact to delete.')
    
    elif contact_id is not None:
        try:
            # Retrieve the object
            contact = Contact.objects.get(pk=contact_id)
            # Delete the object
            contact.delete()
            messages.success(request, 'Contact deleted successfully!') # Redirect or display success

        except Contact.DoesNotExist:
            messages.error(request, 'No such Contact exist!') # Redirect or display success

    else:
        messages.error(request, 'Kindly select 1 or more contact to delete.')

    return redirect('pages:listContactus')

def seed_contact(request, rec_num=1):
    # Truncate table before creating
    Contact.objects.all().delete()

    # Example in a script or shell
    fake = Faker()
    for _ in range(rec_num):
        Contact.objects.create(
            # title=fake.prefix(), 
            title=fake.random_element(elements=[choice[0] for choice in TITLE_CHOICES]),
            firstname=fake.first_name(),
            lastname=fake.last_name(),
            gender=fake.random_element(elements=[choice[0] for choice in GENDER_CHOICES]),
            email=fake.email(),
            mobile=fake.numerify('##########'),
            subject=fake.sentence(),
            message=fake.text(),
            pin=fake.numerify('######')
        )

    return HttpResponse(f"Seeded {rec_num} contact(s) successfully!")

# def deleteall_contact(request):
#     if request.method == "POST":
#         contact_ids = request.POST.getlist('contact_ids')

#         if(len(contact_ids) > 0):
#             # Filter the QuerySet to include only the selected IDs and delete them
#             deleted_count, _ = Contact.objects.filter(id__in=contact_ids).delete()

#             messages.success(request, f"{deleted_count} contact(s) deleted successfully.")
#         else:
#             messages.error(request, 'Must select atleast 1 contact to delete.')

#     return redirect('pages:listContactus')

# Listing all blog created
def blog_index(request, page=None, count=None):
    # Retrieve all blogs order by modified_on in descending order
    queryset = Blog.objects.all().order_by('-modified_on')

    if queryset:
        # Change count to total records if not set
        if(count is None):
            count = len(queryset)

        paginator = Paginator(queryset, count)

        try:
            # Get the Page object for the requested page number
            list_obj = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            list_obj = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page.
            list_obj = paginator.page(paginator.num_pages)
    else:
        print("Queryset is empty")
        list_obj = None

    # Pass the page object to the template context
    return render(request, "index.html", {"list_template": "blogs/list.html", "module": "Blogs", "list_obj": list_obj, "rec_count": list_obj.number*len(list_obj.object_list), "tags": {'error':'danger','success':'success'}})

# For viewing blog by its ID
def blog_view(request, blog_id):
    try:
        blog = get_object_or_404(Blog, pk=blog_id)
    except:
        messages.error(request, 'No such blog found.') 
    else:
        # label_title = dict(TITLE_CHOICES)
        # contact.title = label_title.get(contact.title, "Unknown Title")
        
        # label_gender = dict(GENDER_CHOICES)
        # contact.gender = label_gender.get(contact.gender, "Unknown Gender")
        return render(request, "blogs/view.html", {"blog": blog, "model_name": blog._meta.verbose_name })
        
# For showing edit form or updating form data
def blog_edit(request, blog_id):
    try:
        instance = get_object_or_404(Blog, pk=blog_id)
    except:
        messages.error(request, 'No such blog found.') 
    else:
        # if this is a POST request we need to process the form data
        if request.method == "POST":
            # create a form instance and populate it with data from the request:
            form = BlogForm(request.POST, instance=instance)
            # check whether it's valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required
                print(form.cleaned_data)
                form.save()
                messages.success(request, 'Successfully updated blog.') 
                
                return redirect('pages:listBlogs')
            else:
                messages.error(request, 'Error while updating blog.') 
                return render(request, "blogs/edit.html", {"form": form,"alert":"Error while updating blog.", "module": "Blogs"})
        else:
            form = BlogForm(instance=instance)
            return render(request, "blogs/edit.html", {"form": form, "module": "Blogs"})
        
# For deleting one or more blog data
def delete_blog(request, blog_id=None):
    if request.method == "POST":
        blog_ids = request.POST.getlist('blog_ids')

        if(blog_ids is not None and len(blog_ids) > 0):
            # Filter the QuerySet to include only the selected IDs and delete them
            deleted_count, _ = Blog.objects.filter(id__in=blog_ids).delete()

            messages.success(request, f"{deleted_count} blog(s) deleted successfully.")
        else:
            messages.error(request, 'Must select atleast 1 blog to delete.')
    
    elif blog_id is not None:
        try:
            # Retrieve the object
            blog = Blog.objects.get(pk=blog_id)
            # Delete the object
            blog.delete()
            messages.success(request, 'Blog deleted successfully!') # Redirect or display success

        except Blog.DoesNotExist:
            messages.error(request, 'No such Blog exist!') # Redirect or display success

    else:
        messages.error(request, 'Kindly select 1 or more blog to delete.')

    return redirect('pages:listBlogs')

def seed_blog(request, rec_num=1):
    # Truncate table before creating
    Blog.objects.all().delete()

    # Example in a script or shell
    fake = Faker()
    for _ in range(rec_num):
        Blog.objects.create(
            title=fake.sentence(),
            url=fake.first_name(),
            description=fake.text(),
            image=fake.sentence(),
            user_id=1
        )

    return HttpResponse(f"Seeded {rec_num} blog(s) successfully!")