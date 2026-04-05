from django.urls import include, path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# URLConf
app_name = "pages"
urlpatterns = [
    path("", views.index, name="index"),
    path("list/<str:model_name>", views.list_model, name="listModel"),
    path("list/<str:model_name>/<int:count>", views.list_model, name="listModel"),
    path("list/<str:model_name>/<int:page>/<int:count>", views.list_model, name="listModel"),
    path("create/<str:model_name>", views.create_model, name="createModel"),
    path("edit/<str:model_name>/<int:rec_id>/", views.edit_model, name="editModel"),
    path("<str:model_name>/<int:rec_id>/", views.view_model, name="viewModel"),
    path("delete/<str:model_name>", views.delete_model, name="deleteModel"),
    path("delete/<str:model_name>/<int:rec_id>", views.delete_model, name="deleteModel"),
    path("seed/<str:model_name>/<int:rec_num>", views.seed_model, name="seedModel"),
]

# urlpatterns += staticfiles_urlpatterns()

urlpatterns2 = [
    # path("contactus/list", views.contact_index, name="listContactus"),
    # path("contactus/list/<int:count>", views.contact_index, name="listContactus"),
    # path("contactus/list/<int:page>/<int:count>", views.contact_index, name="listContactus"),
    # path("contactus/create", views.contact_create, name="createContact"),
    # path("contactus/edit/<int:contact_id>/", views.contact_edit, name="contactEdit"),
    # path("contactus/<int:contact_id>/", views.contact_view, name="contactView"),
    # # To delete multiple checked contacts
    # path("contactus/delete", views.delete_contact, name="deleteContact"),
    # # To delete specific contact by its ID
    # path("contactus/delete/<int:contact_id>", views.delete_contact, name="deleteContact"),
    # path("contactus/seed/<int:rec_num>", views.seed_contact, name="seedContact"),
    # # path("contactus/delete", views.deleteall_contact, name="deleteAllContact"),
    # # path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    # # path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    # # path("<int:question_id>/vote/", views.vote, name="vote"),
    # path("blogs/list", views.blog_index, name="listBlogs"),
    # path("blogs/list/<int:count>", views.blog_index, name="listBlogs"),
    # path("blogs/list/<int:page>/<int:count>", views.blog_index, name="listBlogs"),
    # path("blogs/seed/<int:rec_num>", views.seed_blog, name="seedBlog"),
    # path("blogs/<int:blog_id>/", views.blog_view, name="blogView"),
    # path("blogs/edit/<int:blog_id>/", views.blog_edit, name="blogEdit"),
    # path("blogs/delete", views.delete_blog, name="deleteBlog"),
    # # To delete specific contact by its ID
    # path("blogs/delete/<int:blog_id>", views.delete_blog, name="deleteBlog"),
    # path('qr_code/', include('qr_code.urls', namespace="qr_code")),
]