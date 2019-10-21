from django.views.generic import View, TemplateView

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse


class IndexView(TemplateView):
    """
    This is for rendering out the standings graph
    Some work to be done here
    """
    template_name = "JJE_Standings/standings.html"
