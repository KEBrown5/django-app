from django.shortcuts import render, redirect
from .forms import CustomUserForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from .forms import EditProfileForm

# Create your views here.
def login_page(request):
    if request.method == 'POST': # Post request because users are submitting info
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password) # Grabs the posted username and password to authenticate with. Checks it against the database

        if user is not None:
            login(request, user) # Authenticates the user for sessions moving forward
            return redirect('blogsite:home')
        else:
            messages.info(request, 'Try again! Username or password is incorrect')

    context = {}
    return render(request, 'users/login.html', context)

# This just gets rid of your session credentials and returns you back to the login page
def logout_page(request):
    logout(request)
    return redirect('users:login')

def register_page(request):
    # Users will see an empty form on page load
    if request.method != 'POST':
        form = CustomUserForm()
    else:
        # This creates a variable named form that will hold the data being submitted by the user. Request.post takes care of the data
        form = CustomUserForm(request.POST)
        # Checks if the form is valid, such as if all the fields are filled out, or if the data is within the limits
        if form.is_valid():
            form.save() # Once confirmed to be valid, save it to the database
            return redirect('users:login') # Now that a user is registered, send them to the login page to log in
    
    # Saves the form's data in a dictionary and sends it back to the register template
    context = {'form': form}
    return render(request, 'users/register.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
            return redirect('users:login')
    else:
        form = EditProfileForm(instance = request.user)
    return render(request, 'users/edit_profile.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) # Keeps user logged in after changing the password
            return redirect('users:login')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'users/change_password.html', {'form': form})



 


