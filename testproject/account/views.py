from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from .tokens import generate_token
from django.contrib.sites.shortcuts import get_current_site


# Create your views here.

###### solution 1 ######
# def login_view(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect('book:index')
#     else:
#         form = AuthenticationForm()
#     return render(request, 'account/login.html', {
#         'form': form,
#     })


# def logout_view(request):
#     if request.method == 'POST':
#         logout(request)
#         return redirect('book:index')


# def signup_view(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('book:index')
#     else:
#         form = UserCreationForm()
#     return render(request, 'account/signup.html', {
#         'form': form,
#     })


###### solution 2 ######

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            messages.success(request, "Logged In Sucessfully!!")
            return redirect('book:index')
        else:
            messages.error(request, "username or password incorrect!!")
            # return redirect('account2/login.html')

    return render(request, 'account2/login.html')


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, "Logged Out Successfully!!")
        return redirect('book:index')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(
                request, "Username already exist! Please try some other username.")
            return redirect('account:signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('account:signup')

        if len(username) > 20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('account:signup')

        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('account:signup')

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('account:signup')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False

        myuser.save()
        messages.success(
            request, "Your Account has been created succesfully!! ")

        # Welcome Email
        subject = "Welcome to ZAX- Django Login!!"
        message = "Hello " + myuser.first_name + "!! \n" + \
            "Welcome to ZAX!! \nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\nAnywhere with You"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ ZAX - Django Login!!"
        message2 = render_to_string('account2/email_confirmation.html', {
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = True
        email.send()

        return redirect('account:login')

    return render(request, 'account2/signup.html')



def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request,myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('book:index')
    else:
        return render(request,'account2/activation_failed.html')
