from datetime import datetime
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View


from .models import Post, Category
from .filters import SearchFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import mail_managers


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


# # создаём функцию-обработчик с параметрами под регистрацию сигнала
# @receiver(post_save, sender=Category)
# def notify_managers_category(sender, instance, created, **kwargs):
#
#     if created:
#         subject = f'{instance.name} {instance.date.strftime("%d %m %Y")}'
#     else:
#         subject = f'Category changed for {instance.name} {instance.date.strftime("%d %m %Y")}'
#
#     mail_managers(
#         subject=subject,
#         message=instance.message,
#     )


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        current_day = datetime.now().date()
        count = Post.objects.filter(id_author=post.id_author, date__gte=current_day).count()

        if count < 3:
            if self.request.path == '/home/news/create':
                post.type_post = 'news'
            else:
                post.type_post = 'article'
        else:
            print("Один пользователь не может публиковать более трёх новостей в сутки.")
        post.save()


class PostUpdate(UpdateView, LoginRequiredMixin, TemplateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        return context


@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='author')
    if not request.user.groups.filter(name='author').exists():
        author_group.user_set.add(user)
    return redirect('/')


class ProtectedView(LoginRequiredMixin, TemplateView):
    template_name = 'prodected_page.html'


class MyView(PermissionRequiredMixin):
    permission_required = ('news.create_post',
                           'news.delete_post')

class CategoryListView(ListView):
    model = Post
    template_name = 'simpleappnews/mail2.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context

@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы подписались на рассылку новостей.'
    return render(request, 'news/subscribe.html', {'category': category, 'message': message})

    #
    # def get(self, request, *args, **kwargs):
    #     return render(request, 'mail.html', {})
    #
    # def post(self, request, *args, **kwargs):
    #     category = Category(date=datetime.strptime(request.POST['date'], '%Y-%m-%d'), name=request.POST['client_name'])
    #     category.save()
    #
    #     html_content = render_to_string(
    #         'mail.html',
    #         {
    #             'category': category,
    #         }
    #     )
    #
    #     msg = EmailMultiAlternatives(
    #         subject=f'{category.name} {category.date.strftime("%Y-%M-%d")}',
    #         from_email='rimmabogrets@yandex.ry',
    #         to=['cooba@gmail.com'],
    #     )
    #     msg.attach_alternative(html_content, "text/html")  # добавляем html
    #
    #     msg.send()  # отсылаем
    #
    #     return redirect('simpleappnews:make_category')