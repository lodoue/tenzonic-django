from django.db.models import F
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from .forms import ContactForm # Import your form class
from .models import Contact

# Create your views here.
def say_hello(request):
    return render(request, "hello.html")

# Listing all contactus created
def contact_index(request):
    # Retrieve all contacts
    all_contacts = Contact.objects.all().order_by('-modified_on')
    return render(request, "list.html", {"contacts": all_contacts, "tags": {'error':'danger','success':'success'}})

# Creating new contactus
def contact_form(request):
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

    return render(request, "contact_form.html", {"form": form})

def contact_detail(request, contact_id):
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
                return render(request, "contact_form.html", {"form": form,"alert":"Error while updating contact."})
        else:
            form = ContactForm(instance=instance)
            return render(request, "contact_form.html", {"form": form})


def deleteall_contact(request):
    if request.method == "POST":
        print(request.POST)
    return redirect('pages:listContactus')


def delete_contact(request, contact_id):
    try:
        # Retrieve the object
        contact = Contact.objects.get(pk=contact_id)
        # Delete the object
        contact.delete()
        messages.success(request, 'Contact deleted successfully!') # Redirect or display success

    except Contact.DoesNotExist:
        messages.error(request, 'No such Contact found!') # Redirect or display success

    return redirect('pages:listContactus')
    