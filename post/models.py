'''model of post , comments'''
from django.db import models
from account.models import CustomUser


class posts(models.Model):
    '''post model'''
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=10000)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # comment = models.ManyToManyField(comment)

class comment(models.Model):
    '''comment model'''
    comment_text = models.CharField(max_length=500)
    created_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    ofpost = models.ForeignKey(posts,on_delete=models.CASCADE)
