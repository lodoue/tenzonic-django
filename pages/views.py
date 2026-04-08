from django.db.models import Q, F
from django.apps import apps
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import TemplateView, ListView
from .forms import ContactForm, BlogForm, ReviewForm # Import your form class
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from .models import Contact, TITLE_CHOICES, GENDER_CHOICES, Blog, Review
from faker import Faker

# Define your app and model name as strings
app_label = "pages"
app_models = {"contact": {"name": "Contact", "model": Contact, "form": ContactForm}, "blog": {"name": "Blog", "model": Blog, "form": BlogForm}, "review": {"name": "Review", "model": Review, "form": ReviewForm}}

def index(request):
    # Pass the page object to the template context
    return render(request, "home.html", {"models": [('contact', 'Contact'), ('blog', 'Blog'), ('review', 'Review')], "per_page": 5})

class ListModelView(TemplateView):
    model = Contact
    template_name = 'index.html'
    unique_field = None

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        
        # Access the 'params' from the URL else use the default as defined
        model_name = self.kwargs.get('model_name')
        count = self.kwargs.get('count', None)
        page = self.kwargs.get('page', None)

        # Change the model to the model_name passed in URL
        self.model = app_models[model_name]['model']

        context['model_name'] = model_name
        context['fields'] = self.model.get_fields(self.model)
        context['list_template'] = "list.html"
        context['module'] = self.model._meta.verbose_name
        context['tags'] = {'error':'danger','success':'success'}
        total_count = 0
        showing_from = 1

        unique_field_names = [field.name for field in self.model._meta.get_fields() if field.name is not 'id' and getattr(field, 'unique', False)]
        if len(unique_field_names) > 0:
            self.unique_field = unique_field_names[0]
            context['unique_field'] = self.unique_field

        queryset = self.model.objects.all().order_by('-modified_on')

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
            
            total_count = list_obj.number*len(list_obj.object_list)
            showing_from = ((list_obj.number*count)-count)+1
        else:
            print("Queryset is empty")
            list_obj = None

        context['rec_count'] = total_count
        context['list_obj'] = list_obj
        context['showing_from'] = showing_from
        return context
    

class SearchResultsView(ListView):
    model = Contact
    template_name = "index.html"
    unique_field = None

    def get_context_data(self, **kwargs):
        total_count = 0
        showing_from = 1
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        
        # Access the 'params' from the URL else use the default as defined
        model_name = self.kwargs.get('model_name')
        count = self.kwargs.get('count', None)
        page = self.kwargs.get('page', None)

        self.model = app_models[model_name]['model']
        
        context['model_name'] = model_name
        context['search_fields'] = self.model.search_fields(self)
        context['fields'] = self.model.get_fields(self.model)

        queryset = self.get_queryset()
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

            total_count = list_obj.number*len(list_obj.object_list)
            showing_from = ((list_obj.number*count)-count)+1
        else:
            print("Queryset is empty")
            list_obj = None

        context['list_obj'] = list_obj
        context['list_template'] = "list.html"
        context['module'] = self.model._meta.verbose_name
        context['unique_field'] = self.get_unique_field()
        context['tags'] = {'error':'danger','success':'success'}
        context['search_query'] = self.request.GET.get("q")
        context['rec_count'] = total_count
        context['showing_from'] = showing_from
        return context

    def get_queryset(self):
        # Access the 'params' from the URL else use the default as defined
        model_name = self.kwargs.get('model_name')
        self.model = app_models[model_name]['model']
        search_fields = self.model.search_fields(self)

        query = self.request.GET.get('q')        
        conditions = {}

        if query:
            for field in search_fields:
                filter_key = f"{field}__icontains"
                conditions[filter_key] = query

        object_list = self.model.objects.filter(Q(_connector=Q.OR, **conditions))
        return object_list
    

    def get_unique_field(self):
        unique_field_names = [field.name for field in self.model._meta.get_fields() if field.name is not 'id' and getattr(field, 'unique', False)]
        if len(unique_field_names) > 0:
            self.unique_field = unique_field_names[0]

        return self.unique_field


# Creating new record
def create_model(request, model_name):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = app_models[model_name]["form"](request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            print(form.cleaned_data)
            form.save()
            messages.success(request, f"{app_models[model_name]['name']} created successfully.")
            return redirect('pages:listModel', model_name)
        else:
            messages.error(request, f"Something went wrong while creating new {app_models[model_name]['name']}.") 

    # if a GET (or any other method) we'll create a blank form
    else:
        form = app_models[model_name]["form"]()

    return render(request, "create.html", {"form": form, "module": app_models[model_name]['name'], "model_name": model_name})

# For viewing record by its ID
def view_model(request, model_name, rec_id):
    MyModel = apps.get_model(app_label, app_models[model_name]["name"])
    try:
        record = get_object_or_404(MyModel, pk=rec_id)
    except:
        messages.error(request, f"No such {app_models[model_name]['name']} found.") 
    else:
        if model_name == 'contact':
            label_title = dict(TITLE_CHOICES)
            record.title = label_title.get(record.title, "Unknown Title")
            
            label_gender = dict(GENDER_CHOICES)
            record.gender = label_gender.get(record.gender, "Unknown Gender")

        unique_field_names = [field.name for field in MyModel._meta.get_fields() if field.name is not 'id' and getattr(field, 'unique', False)]
        return render(request, "view.html", {"record": record, "model_name": model_name, "module": app_models[model_name]['name'], "fields": MyModel.get_fields(MyModel), "unique_field": unique_field_names[0] })
        
# For showing edit form or updating form data
def edit_model(request, model_name, rec_id):
    MyModel = apps.get_model(app_label, app_models[model_name]["name"])
    try:
        instance = get_object_or_404(MyModel, pk=rec_id)
    except:
        messages.error(request, f"No such {model_name} found.")
        return redirect('pages:listModel', model_name)
    else:
        # if this is a POST request we need to process the form data
        if request.method == "POST":
            # create a form instance and populate it with data from the request:
            form = app_models[model_name]['form'](request.POST, instance=instance)
            # check whether it's valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required
                print(form.cleaned_data)
                form.save()
                messages.success(request, f"Successfully updated {model_name}.") 
                
                return redirect('pages:listModel', model_name)
            else:
                messages.error(request, f"Error while updating {model_name}.") 
                return render(request, "edit.html", {"form": form,"alert": f"Error while updating {model_name}.","module": app_models[model_name]['name']})
        else:
            form = app_models[model_name]['form'](instance=instance)
        
        return render(request, "edit.html", {"form": form, "model_name": model_name, "module": app_models[model_name]['name']})

# For deleting one or more data
def delete_model(request, model_name, rec_id=None):
    MyModel = apps.get_model(app_label, app_models[model_name]["name"])
    if request.method == "POST":
        rec_ids = request.POST.getlist('rec_ids')

        if(rec_ids is not None and len(rec_ids) > 0):
            # Filter the QuerySet to include only the selected IDs and delete them
            deleted_count, _ = MyModel.objects.filter(id__in=rec_ids).delete()

            messages.success(request, f"{deleted_count} {model_name}(s) deleted successfully.")
        else:
            messages.error(request, f"Must select atleast 1 {model_name} to delete.")
    
    elif rec_id is not None:
        try:
            # Retrieve the object
            record = MyModel.objects.get(pk=rec_id)
            # Delete the object
            record.delete()
            messages.success(request, f"{app_models[model_name]['name']} deleted successfully!") # Redirect or display success

        except MyModel.DoesNotExist:
            messages.error(request, f"No such {app_models[model_name]['name']} exist!") # Redirect or display success

    else:
        messages.error(request, f"Kindly select 1 or more {model_name} to delete.")

    return redirect('pages:listModel', model_name)

def seed_model(request, model_name, rec_num=1):
    MyModel = apps.get_model(app_label, app_models[model_name]["name"])
    # Truncate table before creating
    MyModel.objects.all().delete()

    # Example in a script or shell
    fake = Faker()
    for _ in range(rec_num):
        if model_name == "contact":
            MyModel.objects.create(
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
        elif model_name == "blog":
            MyModel.objects.create(
                title=fake.sentence(),
                # url=fake.first_name(),
                description=fake.text(),
                image=fake.sentence(),
                user_id=1
            )
        elif model_name == "review":
            MyModel.objects.create(
                rated=fake.random_int(min=0, max=5),
                comment=fake.text(),
                image=fake.sentence(),
                user_id=1
            )
        

    return HttpResponse(f"Seeded {rec_num} {model_name}(s) successfully!")
