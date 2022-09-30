from django.shortcuts import render,redirect
from .models import Article, Topic,User,Comment,Like
from django.db.models import Q
from django.contrib.auth import login,logout,authenticate
from .forms import UserForm, UserFormUpdate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
# Create your views here.

def homeView(request):
    topics = Topic.objects.all()[0:20]
    q = request.GET.get('q')
    topic = request.GET.get('topic')
    if topic is not None:
        try:
           articles = Article.objects.filter(Topic__Name=topic)
        except:
            articles = {}
    else:
        if q is None:
            q = ''
        articles = Article.objects.filter(
            Q(Content__icontains=q)
            )
    articles = articles[0:20]
    numberOfArticles = articles.count()
    context = {"topics":topics,"articles":articles,"NoArticle":numberOfArticles}
    return render(request,'Social/index.html',context)

def loginView(request):
    message = ""
    if request.user.is_authenticated:
        return redirect('home')
    if(request.method.lower()=="post"):
        userEmail = request.POST.get('email').lower()
        userPassword = request.POST.get('password')
        try:
            user = User.objects.get(email=userEmail)
        except:
            message = "please enter a valid email or password"
        user = authenticate(request,email=userEmail,password=userPassword)
        print(user)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            message ="please enter a correct password"
            
    context = {"login":True,"message":message}
    return render(request,'Social/login-register.html',context)

def registerView(request):
    message = ''
    if request.user.is_authenticated:
        return redirect('home')
    form = UserForm()
    if request.method == 'POST':
        user_email = request.POST.get('email')
        try:
            User.objects.get(username=user_email)
            message = "this email is already exist try sign in"
        except:
            user = UserForm(request.POST)
            if user.is_valid():
                user = user.save(commit=False)
                user.username = user.username.lower()
                user.email = user.email.lower()
                user.password = make_password(user.password)
                user.save()
                login(request,user)
                return redirect('home')
            else:
                message = "some thing wrong with your registration"
    context = {"login":False,"message":message,"form":form}
    return render(request,'Social/login-register.html',context)

def logoutView(request):
    logout(request)
    return redirect('home')

@login_required(login_url='/login')
def createArticle(request):
    if request.method == 'POST':
        Content = request.POST.get('Content')
        Owner = request.user
        topicName = request.POST.get("topicName")
        try:
            topic = Topic.objects.get(Name=topicName)
        except:
            topic = Topic.objects.create(Name=topicName)
        article = Article.objects.create(Owner=Owner,Content=Content,Topic=topic)
        if article is not None:
            topic.NoArticles+=1
            topic.save()
            return redirect('home')

    topics = Topic.objects.all()
    context= {"topics":topics,"value":"Add"}
    return render(request,'Social/addArticle.html',context)

def detailsView(request,pk):
    article = Article.objects.get(id = int(pk))
    topics = Topic.objects.all()
    comments = Comment.objects.filter(Article=article)
    noComments = comments.count()
    numberOfArticles = Article.objects.all().count()
    #print(article)
    try:
        action = Like.objects.get(user=request.user,article=article)
        like = action.like
        dislike = not(like)
    except:
        like = False
        dislike = False

    context = {"like":like,"dislike":dislike,"article":article,"topics":topics,'comments':comments,"noComments":noComments,"NoArticle":numberOfArticles}
    return render(request,'Social/details.html',context)

@login_required(login_url='/login')
def addComment(request,pk):
    article = Article.objects.get(id = int(pk))
    if request.method == 'POST':
        content = request.POST.get('comment')
        Comment.objects.create(Content=content,Owner=request.user,Article=article)
        return redirect('details',pk=int(pk))

@login_required(login_url='/login')
def deleteArticle(request,pk):
    article = Article.objects.get(id=int(pk))
    article.Topic.NoArticles-=1
    article.Topic.save()
    if article.Topic.NoArticles==0:
        article.Topic.delete()
    article.delete()
    return redirect('home')

@login_required(login_url='/login')
def updateArticle(request,pk):
    article = Article.objects.get(id=int(pk))
    if request.method=='POST':
        Content = request.POST.get('Content')
        Owner = request.user
        topicName = request.POST.get("topicName")
        article.Topic.NoArticles-=1
        article.Topic.save()
        if article.Topic.NoArticles==0:
            article.Topic.delete()
        article.Content = Content
        article.Owner = Owner
        try:
            topic = Topic.objects.get(Name=topicName)  
        except:
            topic = Topic.objects.create(Name=topicName)
        article.Topic = topic
        article.Topic.NoArticles+=1
        article.Topic.save()
        article.save()
        return redirect('home')
    topics = Topic.objects.all()
    context= {"topics":topics,"article":article,"value":"Update"}
    return render(request,'Social/addArticle.html',context)

@login_required(login_url='/login')
def deleteComment(request,pk):
    comment = Comment.objects.get(id=int(pk))
    article = comment.Article.id
    comment.delete()
    return redirect('details',pk=article)

@login_required(login_url='/login')
def dislike(request,pk):
    article = Article.objects.get(id=int(pk))
    try:
        action = Like.objects.get(user=request.user,article = article)
        if action.like:
            action.like = False
            article.noLike-=1
            article.noDislike+=1
            article.save()
            action.save()
        else:
            article.noDislike-=1
            article.save()
            action.delete()
    except:
        Like.objects.create(user=request.user,article=article,like=False)
        article.noDislike+=1
        article.save()
    return redirect('details',pk=pk)
    

@login_required(login_url='/login')
def like(request,pk):
    article = Article.objects.get(id=int(pk))
    try:
        action = Like.objects.get(user=request.user,article = article)
        if action.like:
            article.noLike-=1
            article.save()
            action.delete()
        else:
            action.like = True
            article.noLike+=1
            article.noDislike-=1
            article.save()
            action.save()
    except:
        Like.objects.create(user=request.user,article=article,like=True)
        article.noLike+=1
        article.save()
    return redirect('details',pk=pk)

@login_required(login_url='/login')
def profile(request):
    topics = Topic.objects.all()
    numberOfArticles = Article.objects.all().count()
    user = User.objects.get(id=request.user.id)
    form = UserFormUpdate(instance=user)
    if request.method == "POST":
        print(request.FILES)
        form = UserFormUpdate(request.POST,request.FILES,instance=user)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            return redirect('profile')
    context = {"topics":topics,"NoArticle":numberOfArticles,"user":user,"form":form}
    return render(request,'Social/profile.html',context)


