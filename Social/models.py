from email.policy import default
from io import open_code
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    username = models.CharField(null=True,max_length=50)
    Avatar = models.ImageField(null=True,default='avatar.svg')
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username+" "+self.email+" "+str(self.is_superuser)

class Topic(models.Model):
    Name = models.CharField(max_length=30)
    NoArticles = models.IntegerField(default=0)
    def __str__(self):
        return self.Name +" "+ str(self.NoArticles)

class Article(models.Model):
    Topic = models.ForeignKey(Topic,on_delete=models.CASCADE)
    Content = models.TextField(max_length=1000)
    Owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name="author")
    updated_at = models.DateTimeField(null=True,auto_now=True)
    created_at = models.DateTimeField(null=True,auto_now_add=True)
    noLike = models.PositiveIntegerField(default=0)
    noDislike = models.PositiveIntegerField(default=0)
    userLike = models.ManyToManyField(User,related_name="Users_like_article")
    userDisLike = models.ManyToManyField(User,related_name="User_dislike_article") 
    def __str__(self):
        return str(self.Topic) + " "+self.Content[:100]+" "+str(self.Owner)
    class Meta:
        ordering = ('-updated_at','-created_at')


class Like(models.Model):
    user = models.ForeignKey(User,related_name="liked_user",on_delete=models.CASCADE)
    article = models.ForeignKey(Article,related_name="liked_article",on_delete=models.CASCADE)
    like = models.BooleanField(default=False)

class Comment(models.Model):
    Owner = models.ForeignKey(User,on_delete=models.CASCADE)
    Article = models.ForeignKey(Article,on_delete=models.CASCADE)
    Content = models.TextField(max_length=200)
    updated = models.DateTimeField(null=True,auto_now=True)
    created = models.DateTimeField(null=True,auto_now_add=True)
    def __str__(self):
        return str(self.Owner) +" "+str(self.Article)+" "+self.Content
    
    class Meta:
        ordering = ('-updated','-created')
