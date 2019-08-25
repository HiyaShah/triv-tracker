from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from . import forms, models
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
import datetime

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, "registration/email_confirmation.html")
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def index(request):
    return render(request, "triv_tracker_app/index.html")

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect("/")

            else:
                return render(request, "registration/inactive_user.html")
        else:
            return render(request, "registration/invalid_credentials.html")

    return render(request, "triv_tracker_app/login.html")

def register(request):
    if request.method == "POST":
        user_form = forms.UserForm(request.POST)
        # profile_form = forms.UserProfileForm(request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.is_active = False
            user.save()

            profile = models.UserProfile(user=user, points=0)
            profile.save()

            current_site = get_current_site(request)
            mail_subject = 'Activate your tracker account.'
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = user_form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, "registration/email_confirmation.html")

    else:
        user_form = forms.UserForm()
        # profile_form = forms.UserProfileForm()

    context_dict = {
        "user_form": user_form,
    }

    return render(request, "triv_tracker_app/register.html", context=context_dict)

@login_required(login_url="/login/")
def update(request):
    if request.method == "POST":
        form = forms.UpdateForm(request.POST)

        if form.is_valid():
            user = request.user

            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.username = request.POST.get('username')
            user.email = request.POST.get('email')
            user.save()

            return HttpResponseRedirect("/")

    else:
        form = forms.UpdateForm(initial={
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "username": request.user.username,
            "email": request.user.email,
        })

    return render(request, "triv_tracker_app/update.html", context={"form": form})

@login_required(login_url="/login/")
def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/")

@login_required(login_url="/login/")
def achievements(request):
    achievements = models.Achievement.objects.all() # Getting all achievements
    categories = list(set([achievement.category for achievement in achievements])) # Picking out unique categories
    categories = {category: [] for category in categories} # Storing it into dictionary with empty lists

    for achievement in achievements: # Appending respective achievements to certain categories
        category = achievement.category
        achievements_category = models.Achievement.objects.filter(category=category)
        print(list(achievements_category))
        categories[category] = [i for i in list(achievements_category)]

    if request.method == "POST":
        code = request.POST.get('code')
        reward = request.POST.get('reward')
        last_achievement_id = request.POST.get('last_achievement_id')
        last_achievement_time = datetime.datetime.now()
        matching_code = models.MentorCode.objects.filter(code=code)

        if matching_code:
            user = models.UserProfile.objects.filter(user=request.user)[0]
            user.points += int(reward)
            user.last_achievement_id = last_achievement_id
            user.last_achievement_time = last_achievement_time
            user.save()

            record = models.AchievementRecord.objects.filter(user=user)[0]
            print(getattr(record, "achievement{}".format(last_achievement_id)))

            return HttpResponseRedirect("/achievements/")

        else:
            return HttpResponse("Invalid code")

    print(categories)
    return render(request, "triv_tracker_app/achievements.html", context={"categories": categories})

@login_required(login_url="/login/")
def progress(request):
    user = models.UserProfile.objects.filter(user=request.user)[0]
    history = user.history.all()

    records = {}

    for record in history:
        id = record.last_achievement_id
        achievement = models.Achievement.objects.filter(id=id)[0]
        records[record] = achievement

    return render(request, "triv_tracker_app/progress.html", context={"records": records})

@login_required(login_url="/login/")
def leaderboards(request):
    users = models.UserProfile.objects.raw("select * from triv_tracker_app_UserProfile order by points desc limit 5")

    context_dict = {
        "users": users,
    }

    return render(request, "triv_tracker_app/leaderboards.html", context=context_dict)

@login_required(login_url="/login/")
def leaderboards_all(request):
    users = models.UserProfile.objects.raw("select * from triv_tracker_app_UserProfile order by points desc")

    context_dict = {
        "users": users,
    }

    return render(request, "triv_tracker_app/leaderboards_all.html", context=context_dict)

@login_required(login_url="/login/")
def my_account(request):
    return render(request, "triv_tracker_app/my_account.html", context={"profile": models.UserProfile.objects.filter(user=request.user)[0]})

def contact_us(request):
    return render(request, "triv_tracker_app/contact-us.html")

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, "registration/activate_email_confirmation.html")
    else:
        return render(request, "registration/invalid_link.html")

@login_required(login_url="/login/")
def enter_code(request):
    if request.method == "POST":
        form = forms.CodeForm(request.POST)

        if form.is_valid():
            code = form.cleaned_data['code']

            matching_code = models.Code.objects.filter(code=code)

            if matching_code:
                user = models.UserProfile.objects.filter(user=request.user)[0]
                user.points = user.points + matching_code[0].amount
                user.save()

            else:
                return HttpResponse("Invalid code")

    else:
        form = forms.CodeForm()

    return render(request, "triv_tracker_app/enter_code.html", context={"form": form})
