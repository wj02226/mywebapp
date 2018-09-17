from pyquery import PyQuery as pq
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNumExpandMethod, ReadDetail

class BlogType(models.Model):
    type_name = models.CharField(max_length=20)

    def __str__(self):        
        return self.type_name

class Blog(models.Model, ReadNumExpandMethod):
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE)
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    read_details = GenericRelation(ReadDetail)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    def html2text(self):
        lines = map(lambda s: '%s' % s.replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>'), filter(lambda s: s.strip() != '', self.content.split("\n")))
        return ''.join(lines)

    def get_contentimg_url(self):
        temp = Blog.objects.filter(pk=str(self.id)).values('content') #values获取Article数据表中的content字段内容
        if not temp[0]['content'] or 'img' not in temp[0]['content']:
            return '/media/upload/default.jpg'
        else:
            html = pq(temp[0]['content']) #pq方法获取编辑器html内容
            img_path = pq(html)('img').attr('src')#截取html内容中的路径
            return img_path

    def __str__(self):
        return "<Blog: %s>" % self.title

    class Meta:
        ordering = ['-created_time']
