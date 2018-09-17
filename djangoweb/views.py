from django.shortcuts import get_object_or_404, render, redirect
from blog.models import Blog
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.urls import reverse
from read_statistics.utils import get_seven_days_read_data, get_today_hot_data, get_yesterday_hot_data, get_7_days_hot_blogs
from django.db.models.aggregates import Count
from read_statistics.models import ReadNum
from likes.models import LikeCount
from comment.models import Comment

def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(blog_content_type)

    # 获取7天热门博客的缓存数据
    hot_blogs_for_7_days = cache.get('hot_blogs_for_7_days')
    if hot_blogs_for_7_days is None:
        hot_blogs_for_7_days = get_7_days_hot_blogs()
        cache.set('hot_blogs_for_7_days', hot_blogs_for_7_days, 3600)

    context = {}
    context['dates'] = dates
    context['read_nums'] = read_nums
    context['today_hot_data'] = get_today_hot_data()
    context['yesterday_hot_data'] = get_yesterday_hot_data()
    context['hot_blogs_for_7_days'] = get_7_days_hot_blogs()
    context['read_hot_data'] = get_read_num()
    context['like_hot_data'] = get_likes()
    context['comment_hot_data'] = get_comments()
    return render(request, 'home.html', context)

def get_read_num():
    blog_id = ReadNum.objects.order_by('-read_num').first().object_id
    blog = get_object_or_404(Blog, pk=blog_id)
    return blog

def get_likes():
    blog_id = LikeCount.objects.order_by('-liked_num').first().object_id
    blog = get_object_or_404(Blog, pk=blog_id)
    return blog

def get_comments():
    blog_id = Comment.objects.values('object_id').annotate(total=Count('object_id')).order_by('-total').first()['object_id']
    blog = get_object_or_404(Blog, pk=blog_id)
    return blog