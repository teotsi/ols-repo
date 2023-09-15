from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('terms/',views.terms, name="terms"),
    path('terms/<str:id>',views.term, name="terms"),
]