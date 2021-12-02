from django.contrib import admin
from django.urls import path, include
from .yasg import urlpatterns as doc_urls
from post.views import PostViewset

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('post', PostViewset)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/', include('account.urls')),

]

urlpatterns += doc_urls
