from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Category(models.Model):
    """
    Django 要求模型必须继承models.Model类
    Category 只需要一个简单的分类名name就可以了
    CharField 的 max_length 参数指定最大的长度
    Django 还提供了其他数据类型（日期时间类型DataTimeField、整数类型IntegerField等）
    全部内置类型查看：https://docs.djangoproject.com/en/1.10/ref/models/fields/#field-types
    """
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Post(models.Model):
    """
    文章的数据库表稍微复杂一点，主要是涉及的字段更多
    """
    title = models.CharField(max_length=100)
    # 正文用TextField
    body = models.TextField()
    # 文章创建时间和修改时间用DateTimeField
    create_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    # 文章摘要， 可以没有文章摘要，但默认情况下CharField要求我们必须存入数据
    # 指定CharField的blank=True后就允许空值了
    excerpt = models.CharField(max_length=200, blank=True)

    # 下面将文章对应的数据库表和分类、标签对应的数据库表关联起来
    # 我们规定一篇文章只能对应一个分类，但是一个分类下可以由多篇文章，使用ForeignKey，是一对多的关系
    # 而对于标签来说，一篇文章可以对应多个标签，同一个标签下可能有多篇文章，所以使用ManyToManyField，是多对多的关系
    # 同时文章可以没有标签，所以标签tags指定了blank=True
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)

    # 文章作者，这里User是从 django.contrib.auth.models 导入的
    # django.contrib.auth 是django内置的应用，专门用于处理网站用户的注册、登陆等流程，User是Diango为我们已经写好的用户模型
    # 这里我们通过 ForeignKey把文章和User关联起来
    # 规定一篇文章只能有一个作者，而一个作者可以由多篇文章，是一对多的关系
    author = models.ForeignKey(User)

    def __str__(self):
        return self.title

    # 自定义 get_absolute_url 方法
    # 记得从django.urls 中导入 reverse 函数
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-create_time']





