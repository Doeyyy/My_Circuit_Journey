from django.urls import path
from . import views
from django.utils.text import slugify
from django.conf import settings
from django.conf.urls.static import static

urlpatterns= [
    path('', views.index, name='index'),
    path('create/', views.create_blog, name='new_log'),
    path('update/<slug:slug>/', views.edit_blog, name='edit_blog'),
    path('details/<slug:slug>/', views.post_info, name='details'),
    path('delete/<slug:slug>/', views.delete_blog, name='delete'),
    path('search', views.search_blogs, name="search"),
    path('categories/<slug:slug>/', views.cat, name="categories"),
    path("about/", views.about, name="about"),
      # ... your existing URLs ...
   
]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
