from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from like.models import Like


class Created(models.Model):
    """
    Нужен для того чтобы, во всех моделях не прописовали одно и тоже поле
    все последующие модели будут наследоваться от этого класса и буду принимать его поля
    """
    created = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        """
        Значение abstract = True означает что при
        создание файлов миграциия для нашей модели
        эти файлы не будут создавться
        """
        abstract = True


class Post(Created):
    title = models.CharField(max_length=50)
    description = models.TextField()
    author = models.ForeignKey(
        'account.CustomUser', on_delete=models.CASCADE,
        related_name='problems'
    )
    likes = GenericRelation(Like)

    @property
    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title