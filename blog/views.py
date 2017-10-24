from django.shortcuts import render, get_object_or_404
from .models import Post, Category
from comments.forms import CommentForm
import markdown

def index(request):
    post_list = Post.objects.all()
    return render(request, 'blog/index.html', context={'post_list': post_list})

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                     'markdown.extensions.extra',
                                     'markdown.extensions.codehilite',
                                     'markdown.extensions.toc',
                                  ])
    form = CommentForm()
    comment_list = post.comment_set.all() # 获取该post下的所有评论
    # 将文章、表单、以及文章下的评论列表作为模板变量传给detail.html模板，以便渲染相应数据
    context = {
                'post': post,
                'form': form,
                'comment_list': comment_list
                }
    return render(request, 'blog/detail.html', context=context)

# 归档页面视图
def archives(request, year, month):
    post_list = Post.objects.filter(create_time__year=year,
                                    create_time__month=month
                                    )
    return render(request, 'blog/index.html', context={'post_list': post_list})

# 分类页面视图
def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate)
    return render(request, 'blog/index.html', context={'post_list': post_list})