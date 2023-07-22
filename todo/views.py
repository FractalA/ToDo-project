from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import ToDoForm
from .models import ToDo
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def signupuser(request):
    if request.method == "GET":
        return render(request, 'todo/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todo/signupuser.html', {'form': UserCreationForm(),
                                                                'error': 'That username has been already taken. '
                                                                         'Choose another one'})

        else:
            return render(request, 'todo/signupuser.html', {'form': UserCreationForm(),
                                                            'error': 'Passwords did not match'})


@login_required()
def currenttodos(request):
    todos = ToDo.objects.filter(user=request.user, goal_time__isnull=True)
    return render(request, 'todo/currenttodos.html', {'todos': todos})


def home(request):
    return render(request, 'todo/home.html')


@login_required()
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def loginuser(request):
    if request.method == "GET":
        return render(request, 'todo/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', {'form': AuthenticationForm(),
                                                           'error': 'Username and password did not match'})
        else:
            login(request, user)
            return redirect('currenttodos')


@login_required()
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form': ToDoForm()})
    else:
        try:
            form = ToDoForm(request.POST)
            new_todo = form.save(commit=False)
            new_todo.user = request.user
            new_todo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form': ToDoForm(),
                                                            'error': 'Invalid data passed in. Try again.', })


@login_required()
def show_todo(request, todo_pk):
    todo = get_object_or_404(ToDo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = ToDoForm(instance=todo)
        return render(request, 'todo/show_todo.html', {'todo': todo, 'form': form})
    else:
        try:
            form = ToDoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/show_todo.html', {'todo': todo, 'form': form,
                                                           'error': 'Invalid data passed in. Try again.', })


@login_required()
def completetodo(request, todo_pk):
    todo = get_object_or_404(ToDo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.goal_time = timezone.now()
        todo.save()
        return redirect('currenttodos')


@login_required()
def completed(request):
    todos = ToDo.objects.filter(user=request.user, goal_time__isnull=False).order_by('-goal_time')
    return render(request, 'todo/completed.html', {'todos': todos})


@login_required()
def deleted(request, todo_pk):
    todo = get_object_or_404(ToDo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')

