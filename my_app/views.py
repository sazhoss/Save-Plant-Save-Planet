from django.shortcuts import render, HttpResponse, redirect
from .models import Post, Category, User, Aboutus, Contactus, Donation, UserNotification
from django.db.models import Q
from .forms import SignupForm, PostForm, UpdateProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    searched_category = request.GET.get('category') if request.GET.get('category') != None else ''
    all_posts = Post.objects.filter(
        Q(description__icontains=searched_category)|
        Q(category__category_name__icontains=searched_category), is_active=True
        ).order_by('-id')
    recent_posts = Post.objects.all().order_by('-id')[:4]
    all_categories = Category.objects.all()
    context = {
        'all_posts': all_posts,
        'recent_posts': recent_posts,
        'all_categories': all_categories
    }
    return render(request, 'my_app/index.html', context)

def user_signup(request):
    signup_form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'my_app/signup.html', {'signup_form': form})
    return render(request, 'my_app/signup.html', {'signup_form': signup_form})

@login_required(login_url='login')
def add_new_post(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            description = form.cleaned_data.get('description')
            category = form.cleaned_data.get('category')
            image = form.cleaned_data.get('image')
            post = Post.objects.create(description=description, category=category, image=image, uploader=request.user)
            post.save()
            return redirect('home')
        else:
            return render(request, 'my_app/add_new_post.html', {'form': form})
    return render(request, 'my_app/add_new_post.html', {'form': form})

@login_required(login_url='login')
def user_profile(request):
    user_posts = Post.objects.filter(uploader=request.user)
    context = {
        'user_posts': user_posts
    }
    return render(request, 'my_app/user_profile.html', context)

@login_required(login_url='login')
def update_post(request, post_id):
    post = Post.objects.get(id=post_id, uploader=request.user)
    form = PostForm(instance=post)
    if request.method == 'POST':
        updated_form = PostForm(request.POST, request.FILES, instance=post)
        if updated_form.is_valid():
            updated_form.save()
            return redirect('home')
        else:
            return render(request, 'my_app/update_post.html', {'post_id': post.id, 'form': updated_form})
    return render(request, 'my_app/update_post.html', {'post_id': post.id, 'form': form})

@login_required(login_url='login')
def delete_post(request, post_id):
    if request.method == 'POST':
        confirmation = request.POST.get('yes')
        if confirmation:
            post = Post.objects.get(id=post_id, uploader=request.user)
            post.delete()
            return redirect('user_profile')
    return render(request, 'my_app/delete_post.html', {'post_id': post_id})

@login_required(login_url='login')
def deactivate_post(request, post_id):
    if request.method == 'POST':
        confirmation = request.POST.get('yes')
        if confirmation:
            post = Post.objects.get(id=post_id, uploader=request.user)
            post.is_active = False
            post.save()
            return redirect('user_profile')
    return render(request, 'my_app/deactivate_post.html', {'post_id': post_id})

@login_required(login_url='login')
def activate_post(request, post_id):
    if request.method == 'POST':
        confirmation = request.POST.get('yes')
        if confirmation:
            post = Post.objects.get(id=post_id, uploader=request.user)
            post.is_active = True
            post.save()
            return redirect('user_profile')
    return render(request, 'my_app/activate_post.html', {'post_id': post_id})

@login_required(login_url='login')
def update_profile(request):
    profile = request.user
    update_profile_form = UpdateProfileForm(instance=profile)
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
        else:
            return render(request, 'my_app/update_profile.html', {'update_profile_form': form})
    return render(request, 'my_app/update_profile.html', {'update_profile_form': update_profile_form})

def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, 'my_app/post_detail.html', {
        'post': post
    })

def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')
            return redirect('login')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Wrong email or password')
            return redirect('login')
    return render(request, 'my_app/login.html')

def about_us(request):
    organization = Aboutus.objects.all().order_by('-id')[:1]
    return render(request, 'my_app/about_us.html', {
        'organization': organization[0]
    })

def contact_us(request):
    organization = Aboutus.objects.all().order_by('-id')[:1]
    contact = Contactus.objects.all().order_by('-id')[:1]
    return render(request, 'my_app/contact_us.html', {
        'organization': organization[0],
        'contact': contact[0]
    })

@login_required(login_url='login')
def donation(request, post_id):
    organization = Aboutus.objects.all().order_by('-id')[:1]
    post = Post.objects.get(id=post_id)
    contact = Contactus.objects.all().order_by('-id')[:1]
    if request.method == 'POST':
        donator_bkash_number = request.POST.get('bkash_number')
        transaction_id = request.POST.get('transaction_id')
        donation_amount = request.POST.get('donation_amount')
        donation = Donation.objects.create(receiver=post.uploader, donator = request.user, donator_bkash_number=donator_bkash_number, money_transaction_id=transaction_id, donation_amount=donation_amount, project=post)
        donation.save()
        messages.success(request, 'Please wait for the donation confirmation!!!')
        return redirect('home')

    return render(request, 'my_app/donation.html', {
        'post': post,
        'organization': organization[0],
        'contact': contact[0]
    })

@login_required(login_url='login')
def received_donations(request):
    donations = Donation.objects.filter(receiver=request.user).order_by('-id')
    return render(request, 'my_app/received_donations.html', {'donations': donations})

@login_required(login_url='login')
def approve_donation(request, donation_id):
    donation = Donation.objects.get(id=donation_id, receiver=request.user)
    donation.is_approved = True
    donation.save()
    notification_message = f'Your donation for ({donation.project.description[:5]}...) has been approved.'
    notification = UserNotification.objects.create(sender=request.user, receiver=donation.donator, notification=notification_message, project=donation.project)
    notification.save()
    return redirect('received_donations')


@login_required(login_url='login')
def notifications(request):
    all_notifications = UserNotification.objects.filter(receiver=request.user).order_by('-id')
    for notification in all_notifications:
        if notification.is_active:
            notification.is_active=False
            notification.save()
    return render(request, 'my_app/notifications.html', {
        'all_notifications': all_notifications
    })

@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect('home')