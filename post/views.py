from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from like.mixins import LikedMixin
from .serializers import *
from .models import *

from post.permissions import IsAuthorPermission


class PermissionMixin:

    def get_permission(self):
        if self.action == 'create':
            permissions = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsAuthorPermission, ]
        else:
            permissions = []
        return [permission() for permission in permissions]


class PostViewset(LikedMixin, PermissionMixin, ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_serializer_context(self):
        return {'request': self.request, 'action': self.action}
