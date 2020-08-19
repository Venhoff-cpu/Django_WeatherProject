from django.shortcuts import render
from django.views.generic import TemplateView


class Index(TemplateView):
    template_name = "base.html"


class About(TemplateView):
    template_name = "about.html"

