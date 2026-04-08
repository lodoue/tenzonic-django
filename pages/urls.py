from django.urls import include, path
from . import views
from .views import ListModelView, SearchResultsView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# URLConf
app_name = "pages"
urlpatterns = [
    path("", views.index, name="index"),
    path("search/<str:model_name>", SearchResultsView.as_view(), name="searchModel"),
    path("search/<str:model_name>/<int:count>", SearchResultsView.as_view(), name="searchModel"),
    path("search/<str:model_name>/<int:page>/<int:count>", SearchResultsView.as_view(), name="searchModel"),
    path("list/<str:model_name>", ListModelView.as_view(), name="listModel"),
    path("list/<str:model_name>/<int:count>", ListModelView.as_view(), name="listModel"),
    path("list/<str:model_name>/<int:page>/<int:count>", ListModelView.as_view(), name="listModel"),
    path("create/<str:model_name>", views.create_model, name="createModel"),
    path("edit/<str:model_name>/<int:rec_id>/", views.edit_model, name="editModel"),
    path("<str:model_name>/<int:rec_id>/", views.view_model, name="viewModel"),
    path("delete/<str:model_name>", views.delete_model, name="deleteModel"),
    path("delete/<str:model_name>/<int:rec_id>", views.delete_model, name="deleteModel"),
    path("seed/<str:model_name>/<int:rec_num>", views.seed_model, name="seedModel"),
]
