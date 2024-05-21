from django.contrib import admin
from blog_post.models import Post

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'pub_date']


admin.site.register(Post, PostAdmin)  # 修改
