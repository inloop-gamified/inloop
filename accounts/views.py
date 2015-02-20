from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from accounts.forms import UserForm


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            registered = True
        else:
            print "The following form validation errors occurred: ", user_form.errors

    else:
        user_form = UserForm()

    return render(request, 'registration/register.html', {
        'user_form': user_form,
        'registered': registered
    })


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # returns user object if credentials are valid
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                # everything alright
                login(request, user)
                return HttpResponseRedirect('/tasks/')
            else:
                # account disabled
                return render(request, 'registration/login.html', {
                    'login_failed': False,
                    'account_disabled': True,
                    'successful_logout': False
                })
        else:
            # invalid credentials
            print "Invalid login details: {0}, {1}".format(username, password)
            return render(request, 'registration/login.html', {
                'login_failed': True,
                'account_disabled': False,
                'successful_logout': False
            })
    else:
        return render(request, 'registration/login.html', {
            'login_failed': False,
            'account_disabled': False,
            'successful_logout': False
        })


@login_required(login_url='accounts/login/')
def user_logout(request):
    logout(request)
    return render(request, 'registration/login.html', {
        'login_failed': False,
        'account_disabled': False,
        'successful_logout': True
    })


@login_required(login_url='/accounts/login/')
def user_profile(request):
    pass
