from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    ...
    path('ckeditor/', include('ckeditor_uploader.urls')),
    ...
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextUploadingField()

    def _str_(self):
        return self.title



from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title',)



from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']


from django.shortcuts import render, redirect
from .forms import PostForm

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('post_list')  # Post yaratıldıqdan sonra yönləndiriləcək URL-i daxil edin
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form': form})


from django.urls import path
from .views import create_post

urlpatterns = [
    path('create/', create_post, name='create_post'),
    ...
]