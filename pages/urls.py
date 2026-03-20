from django.urls import path

from . import views

# URLConf
app_name = "pages"
urlpatterns = [
    path("hello", views.say_hello),
    path("contactus/list", views.contact_index, name="listContactus"),
    path("contactus/create", views.contact_form, name="createContact"),
    path("contactus/<int:contact_id>/", views.contact_detail, name="contactDetail"),
    path("contactus/<int:contact_id>/delete", views.delete_contact, name="deleteContact"),
    path("contactus/delete", views.deleteall_contact, name="deleteAllContact"),
    # path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    # path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    # path("<int:question_id>/vote/", views.vote, name="vote"),
]