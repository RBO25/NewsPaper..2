from datetime import datetime
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import SearchFilter
from .forms import PostForm
from django.urls import reverse_lazy

class PostsList(ListView):
    model = Post
    ordering = 'name'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

class Search(ListView):
    model = Post
    ordering = '-id'
    template_name = 'search.html'
    context_object_name = 'search'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = SearchFilter(self.request.GET, queryset=self.get_queryset())
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    # def form_valid(self, form):
    #     post = form.save(commit=False)
    #     post.quantity = 1
    #     return super().form_valid(form)
    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/home/news/create':
            post.type_post = 'news'
        else:
            post.type_post = 'article'
        post.save()

class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')