from django.shortcuts import render, get_object_or_404, redirect
from .models import Category


def show_tree(request, **initkwargs):
    return render(request, "app_menu/tree.html", {})

