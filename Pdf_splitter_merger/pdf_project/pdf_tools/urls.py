from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('split/', views.split_pdf, name='split'),
    path('merge/', views.merge_pdfs, name='merge'),
]