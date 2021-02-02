from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import Url
from link_collector import get_parameter_html_table


class HomePageView(TemplateView):
    template_name = 'home.html'
    def get(self, request, *args, **kwargs):
        form = Url()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = Url(request.POST)
        if form.is_valid():
            url = request.POST['url']
            parameter_table = get_parameter_html_table(url)
            context = {'parameter_table': parameter_table, 'form': Url()}
            return render(request, self.template_name, context)
        return render(request, self.template_name, {'form': form})
