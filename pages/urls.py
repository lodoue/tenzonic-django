from django.urls import path

from . import views

# URLConf
app_name = "pages"
urlpatterns = [
    path("contactus/list", views.contact_index, name="listContactus"),
    path("contactus/list/<int:count>", views.contact_index, name="listContactus"),
    path("contactus/list/<int:page>/<int:count>", views.contact_index, name="listContactus"),
    path("contactus/create", views.contact_create, name="createContact"),
    path("contactus/edit/<int:contact_id>/", views.contact_edit, name="contactEdit"),
    # To delete multiple checked contacts
    path("contactus/delete", views.delete_contact, name="deleteContact"),
    # To delete specific contact by its ID
    path("contactus/delete/<int:contact_id>", views.delete_contact, name="deleteContact"),
    # path("contactus/delete", views.deleteall_contact, name="deleteAllContact"),
    # path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    # path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    # path("<int:question_id>/vote/", views.vote, name="vote"),
]