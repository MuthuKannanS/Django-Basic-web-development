from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContactForm,RegisterForm,LoginForm,PostForm
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from .models import Post,Category
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    blog_title = "All Blog"
    all_posts = Post.objects.filter(is_published=True)
    return render(request, 'index.html', {'all_posts': all_posts, 'blog_title': blog_title})
    
def about(request):
	return render(request, 'about.html')

def detail(request, slug):
    try:
        # getting data from model by post id
        post = Post.objects.get(slug=slug)
        related_posts  = Post.objects.filter(category = post.category).exclude(pk=post.id)

    except Post.DoesNotExist:
        raise Http404("Post Does not Exist!")
    return render(request,'detail.html', {'post': post, 'related_posts':related_posts})

    
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        logger = logging.getLogger("TESTING")
        if form.is_valid:
            #logger.debug(f'POST Data is {form.cleaned_data['name']}')
            success_message = 'Your email has been sent'
            return render(request, 'contact.html', {'form': form, 'success_message': success_message})
        else:
            logger.debug('Form validation failure')   
            return render(request, 'contact.html', {'form': form, 'name': name, 'email': email, 'message': message})
	
    return render(request,'contact.html')
   
def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)#user data
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request,'Registration succussfull.You can Login')
            return redirect("blog:login")#return to login
    return render(request, 'register.html',{'form': form})
    
def login(request):
    form = LoginForm()
    if request.method == 'POST':
        #login_form
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                print("Login Success")
                return redirect("blog:dashboard")#return to dashboard
    
    return render(request, 'login.html')

def dashboard(request):
    #getting user
    all_posts = Post.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'all_posts': all_posts})
    
def logout(request):
    auth_logout(request)
    return redirect("blog:index")

def forgotpassword(request):
    # if request.method == 'POST':
        # form = ForgotPasswordForm(request.POST)
        # if form.is_valid():
            # email = form.cleaned_data['email']
            # user = User.object.get(email=email)
            # #send mail
            # token = default_token_generator.make_token(user)
            # uid = urlsafe_base64_encode(force_byte)
    return render(request,'forgot_password.html')

@login_required
def newpost(request):
    category = Category.objects.all()
    user_id = request.user.id
    
    form = PostForm()
    if request.method == 'POST':
        #form
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            post.user_id = user_id
            post.save()
            return redirect('blog:dashboard')
    return render(request, 'new_post.html', {'category': category})
    
@login_required
def edit_post(request,post_id):
    category = Category.objects.all()
    post = get_object_or_404(Post, id=post_id)
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request,'Post updated succussfully ....!')
            return redirect('blog:dashboard')
            
    return render(request, 'edit_post.html', {'category': category, 'post': post, 'form': form})
        
    return render(request, 'edit_post.html',{'category': category, 'post': post})

@login_required
def delete_post(request,post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    messages.success(request,'Post deleted succussfully ....!')
    return redirect('blog:dashboard')

@login_required
def publish_post(request,post_id):
    post = get_object_or_404(Post, id=post_id)
    post.is_published = True
    post.save()
    messages.success(request,'Post publish succussfully ....!')
    return redirect('blog:dashboard')
    
    
    