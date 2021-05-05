from . import forms
from . import models
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views import generic
import os


class RouteListView(generic.ListView):
    model = models.Route
    form_class = forms.RouteForm


class RouteCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Route
    form_class = forms.RouteForm

    def form_valid(self, form):
        form.instance.created_by_id = self.request.user.id
        return super(RouteCreateView, self).form_valid(form)


class RouteDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.Route
    form_class = forms.RouteForm


class RouteUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = models.Route
    form_class = forms.RouteForm
    pk_url_kwarg = "pk"


class RouteDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.edit.DeleteView):
    model = models.Route
    success_url = reverse_lazy('myapp_Route_list')

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff


class RouteMultiUploadView(LoginRequiredMixin, generic.FormView):
    form_class = forms.RouteMultipleUploadForm
    template_name = 'myapp/routes_upload.html'
    success_url = reverse_lazy('myapp_Route_list')

    def form_valid(self, form):
        file_list = form.save()
        name = form.data.get('name')
        for file in file_list:
            filestem = os.path.splitext(os.path.basename(file))[0]
            models.Route.objects.create(name = name + ' ' + filestem, file = file, created_by_id = self.request.user.id)
        return super().form_valid(form)


class AppUserListView(generic.ListView):
    model = models.AppUser
    form_class = forms.AppUserForm


class AppUserDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.AppUser
    form_class = forms.AppUserForm
