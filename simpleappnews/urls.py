from django.urls import path
from .views import subscribe, CategoryListView, PostsList, PostDetail, PostCreate, PostUpdate, PostDelete, Search, upgrade_me


urlpatterns = [
   path('', PostsList.as_view()),
   path('<int:pk>/', PostDetail.as_view()),
   path('search/', Search.as_view(), name='search'),
   path('news/create/', PostCreate.as_view(), name='post_create'),
   path('news/<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('articles/create/', PostCreate.as_view(), name='post_create'),
   path('articles/<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('articles/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('upgrade/', upgrade_me, name='upgrade')
   path('categories/<int:pk>/', CategoryListView.as_view(), name='category_list')
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe')
]