from django.urls import path
from . import views

urlpatterns = [
    path('<name>', views.show_tree, name='show_tree'),
]
