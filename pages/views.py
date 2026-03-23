from django.db.models import F
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from .forms import ContactForm # Import your form class
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Contact

# Listing all contactus created
def contact_index(request, page=None, count=None):
    # Retrieve all contacts order by modified_on in descending order
    queryset = Contact.objects.all().order_by('-modified_on')

    paginator = Paginator(queryset, count)

    try:
        # Get the Page object for the requested page number
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page_obj = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page.
        page_obj = paginator.page(paginator.num_pages)

    # return render(request, "index.html", {"contacts": all_contacts, "tags": {'error':'danger','success':'success'}})
    # Pass the page object to the template context
    # print(page_obj.object_list)
    return render(request, 'index.html', {'page_obj': page_obj})

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
                return render(request, "edit.html", {"form": form,"alert":"Error while updating contact."})
        else:
            form = ContactForm(instance=instance)
            return render(request, "edit.html", {"form": form})

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



    