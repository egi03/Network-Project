from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    def __str__(self):
        return f"{self.username}"
    
    
class Post(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.content} by {self.user}"

class Like(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="user_like")
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name="post_like")
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user} liked {self.post}"

class Follow(models.Model):
    follower = models.ForeignKey('User', on_delete=models.CASCADE, related_name="following")
    subject = models.ForeignKey('User', on_delete=models.CASCADE, related_name="being_followed")
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.follower} is following {self.subject}"