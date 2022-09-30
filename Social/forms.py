from .models import *
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm


class myUserCreation(UserCreationForm):

    class Meta:
        model = User
        fields =['username','email','password',]

class UserFormUpdate(ModelForm):

    class Meta:
        model = User
        fields =  ['Avatar','username','email']

class UserForm(ModelForm):
    
    class Meta:
        model = User
        fields = ['username','password','email']

class TopicForm(ModelForm):
    
    class Meta:
        model = Topic
        fields = '__all__'

class ArticleForm(ModelForm):
    
    class Meta:
        model = Article
        fields = '__all__'

class CommentForm(ModelForm):
    
    class Meta:
        model = Comment
        fields = '__all__'


