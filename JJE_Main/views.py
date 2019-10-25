from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import redirect
from django.urls import reverse

# Create your views here.


class IndexView(TemplateView):
    template_name = "JJE_Main/index.html"

    def get(self, request, *args, **kwargs):
        return redirect(reverse('waivers_index'))
