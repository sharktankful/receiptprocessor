from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('process/', views.process),
    path('<uuid:id>/points/', views.calculate_points)
]
