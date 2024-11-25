from django.shortcuts import render, get_object_or_404,redirect
from django.utils import timezone
from .models import Post,Category,Tag,Comment
from .forms import PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login,get_user_model,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse



User  = get_user_model()



def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    category = Category.objects.all()
    tag = Tag.objects.all()
    context = {'tag': tag, 'posts': posts, 'category': category}

    return render(request, 'blog/post_list.html',context)

@csrf_exempt
def post_detail(request, slug):
    if request.method == "POST":
        reply = request.POST.get('reply',None)
        parent = request.POST.get('comment',None)
        post = get_object_or_404(Post, slug=slug)
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        text = request.POST.get('text', None)
        # print(text, 'gdfvsdfsdfasdfd')
        try:
            comment = Comment.objects.filter(id=int(parent)).first()
            Comment.objects.create(text=reply, post=post,parent=comment,name=name)
        except Exception as e:
            Comment.objects.create(name=name,email=email,text=text, post=post)
        return redirect(reverse('post_detail', kwargs={'slug': post.slug}))        
    else:
        post = get_object_or_404(Post, slug=slug)
        comment = Comment.objects.filter(post=post,  parent__isnull= True)
        category = Category.objects.all()
        tags = Tag.objects.all()
        context =  {'post': post,'comment':comment,'category':category,'tags':tags}
        return render(request, 'blog/post_detail.html',context)
        



def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


@csrf_exempt
def login_page(request):
    # Check if the HTTP request method is POST (form submission)
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login Succesful")
            return redirect('post_list')
        else:
         messages.error(request, "Invalid Username or Password")
         return redirect('/login/')
    
    return render(request, 'blog/login.html')

# User  = get_user_model()
@csrf_exempt
def signup_page(request):
    if request.method == "POST":
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        profile_image = request.FILES.get('profile_image')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.info(request, "Username taken")
            return redirect('/sign/')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.info(request, "Email already registered")
            return redirect('/sign/')

        # Create the user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            profile_image=profile_image,
            phone_number=phone_number
        )

        # Display success message and redirect to login page
        messages.info(request, "Account created successfully!")
        return redirect('/login/')

    # Handle GET request
    return render(request, 'blog/sign.html')  # Make sure to render your signup template

@login_required
def profile_view(request):
    user = request.user  # Access the logged-in user's custom user model instance
    context = {"user": user}
    return render(request, 'blog/profile.html',context)
    
def edit_profile(request):
    user = request.user

    if request.method == "POST":
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        profile_image = request.FILES.get('profile_image')
        if profile_image:
            user.profile_image = profile_image

        if User.objects.filter(username=username).exclude(id=user.id).exists():
         if user.exists():
            messages.info(request, "Username Taken")
            return redirect('/edit/')

        user.username = username
        user.email = email
        if password:  # Only update password if a new password is provided
            user.set_password(password)
        # if profile_image:  # Update profile image if a new one is uploaded
        #     user.profile_image = profile_image
        user.phone_number = phone_number  

        user.save()  # Save the updated user details
        messages.success(request, "Profile updated successfully!")
        return redirect('login/')  

    initial_data = {
        'phone_number': user.phone_number,
        'email': user.email,
        'username': user.username,
    }
    return render(request, 'blog/edit.html', {'initial_data': initial_data})


    # return render(request, 'blog/edit.html')


   

def logout_view(request):
    logout(request)  # Log the user out
    return render(request, 'blog/login.html')

def category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category)
    context = {'category': category, 'posts': posts}
    return render(request, 'blog/category.html', context)

def tag(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tag=tag)
    context = {'tag': tag, 'posts': posts}
    return render(request, 'blog/tag.html', context)