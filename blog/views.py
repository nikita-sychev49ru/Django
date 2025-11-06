from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from .models import Publication

class PublicationCreateView(CreateView):
    model = Publication
    fields = ['heading', 'text', 'preview']
    template_name = 'blog/publication_create.html'
    success_url = reverse_lazy('blog:publication_list')


class PublicationListView(ListView):
    model = Publication
    template_name = 'blog/publication_list.html'
    context_object_name = 'publications'

    def get_queryset(self):
        return Publication.objects.filter(is_publicated=True)


class PublicationDetailView(DetailView):
    model = Publication
    template_name = 'blog/publication_detail.html'
    context_object_name = 'publication'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()
        return self.object


class PublicationUpdateView(UpdateView):
    model = Publication
    fields = ['heading', 'text', 'preview']
    template_name = 'blog/publication_create.html'
    success_url = reverse_lazy('blog:publication_list')

    def get_success_url(self):
        return reverse_lazy('blog:publication_detail', args=[self.kwargs.get('pk')])


class PublicationDeleteView(DeleteView):
    model = Publication
    template_name = 'blog/publication_confirm_delete.html'
    success_url = reverse_lazy('blog:publication_list')
