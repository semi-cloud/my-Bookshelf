from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from accounts.forms import UserForm


def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)   # 자동 로그인
            login(request, user)
            return redirect('/book')
    else:
        form = UserForm()
    return render(request, 'accounts/signup.html', {'form': form})


