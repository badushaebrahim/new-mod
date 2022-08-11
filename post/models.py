from xml.etree.ElementTree import Comment
from django.db import models
from account.models import CustomUser
# Create your models here.





class posts(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=10000)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # comment = models.ManyToManyField(comment)

class comment(models.Model):
    comment_text = models.CharField(max_length=500)
    created_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    ofpost = models.ForeignKey(posts,on_delete=models.CASCADE)
    
    
    @property
    def comments(self):
        instance = self
        qs = comment.objects.filter(parent=instance)
        return qs
    
    



