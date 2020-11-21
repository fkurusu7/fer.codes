from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_user(request):
  print(request.POST)
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
      login(request, user)
      messages.success(request, ('Logged in successfully. Write some awesome Posts.'))
      return redirect('posts')
    else:
      messages.error(request, ('Username/password invalid.'))
      return redirect('index')
  else:
    return render(request, 'pages/index.html', {})

def logout_user(request):
  logout(request)
  messages.success(request, ('Logged out successfully, Come back soon ;)'))
  return redirect('index')