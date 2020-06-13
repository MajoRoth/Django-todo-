from django.shortcuts import render, redirect
from django.utils import timezone
from index.models import Todo, CreateUserFrom
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user
from django.contrib.auth.models import User


@login_required(login_url='login')
def home(request):
    # todo_items =  Todo.objects.all().order_by("-added_date")
    user = request.user
    todo_items = Todo.objects.filter(user_id=user.id )
    content = {"todo_items": todo_items}
    return render(request, 'index/mainapp.html', content)


@login_required(login_url='login')
def add_todo(request):
    current_date = timezone.now()
    content = request.POST["content"]
    priority = request.POST.get("priority", 1)
    time = request.POST.get("est_time", 0)
    timeU = request.POST.get("est_time_unit", 1)
    Todo.objects.create(user=request.user, added_date=current_date, text=content, priority=priority, est_time=time, est_time_unit=timeU)
    return HttpResponseRedirect('/')


@login_required(login_url='login')
def delete_todo(request, todo_id):
    Todo.objects.get(id=todo_id).delete()
    return HttpResponseRedirect('/')

@unauthenticated_user
def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect')

    context = {}
    return render(request, 'index/login.html', context)


@login_required(login_url='login')
def log_out_user(request):
    logout(request)
    return redirect('login')

@unauthenticated_user
def register_page(request):
    form = CreateUserFrom()
    if request.method == "POST":
        form = CreateUserFrom(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for '+user)
            return redirect('login')

    context = {'form': form}
    return render(request, 'index/register.html', context)



