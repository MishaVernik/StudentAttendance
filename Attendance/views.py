from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

@login_required
def home(request):
    return render(request, 'home.html')


def signup(request):
    print(request)
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            student_or_teacher = request.POST.get('')
            first_name = form.cleaned_data.get("first_name")
            second_name = form.cleaned_data.get("second_name")
            group = form.cleaned_data.get("group")
            email = form.cleaned_data.get("email")
            github = form.cleaned_data.get("github")

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            # TODO: add user into PostgreSQL
            #add_student(first_name, second_name, group, email, github, username, raw_password)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})