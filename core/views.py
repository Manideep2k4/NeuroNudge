from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.timezone import localdate, now
from datetime import date

from .forms import RegisterForm, HabitForm, MoodLogForm, PomodoroLogForm
from .models import Habit, MoodLog, HabitCompletion, PomodoroSession, PomodoroLog

from .ml.sentiment_utils import predict_sentiment
from django.contrib import messages

# ================================
# Authentication Views
# ================================

def landing_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'landing.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_l(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def logout_l(request):
    logout(request)
    return redirect('login')

# ================================
# Dashboard View
# ================================

@login_required
def dashboard(request):
    user = request.user
    today = localdate()

    habits = Habit.objects.filter(user=user, is_archived=False)
    completion_logs = HabitCompletion.objects.filter(
        habit__user=user,
        habit__is_archived=False
    ).order_by('-date')

    latest_mood = MoodLog.objects.filter(user=user).order_by('-date').first()
    habits_done_today = habits.filter(last_completed=today).count()
    top_streak = habits.order_by('-streak').first().streak if habits.exists() else 0
    pomodoros = PomodoroSession.objects.filter(user=user)
    all_completed = all(habit.last_completed == today for habit in habits)

    return render(request, 'dashboard.html', {
        'habits': habits,
        'latest_mood': latest_mood,
        'completion_logs': completion_logs,
        'today': today,
        'habits_done_today': habits_done_today,
        'top_streak': top_streak,
        'pomodoros': pomodoros,
        'all_completed': all_completed,
    })

# ================================
# Pomodoro Timer (Live)
# ================================

@login_required
def start_pomodoro(request):
    if request.method == 'POST':
        habit_id = request.POST.get('habit_id')
        habit = Habit.objects.filter(id=habit_id, user=request.user).first()
        PomodoroSession.objects.create(user=request.user, habit=habit)
    return redirect('dashboard')

@login_required
def stop_pomodoro(request, session_id):
    session = get_object_or_404(PomodoroSession, id=session_id, user=request.user)
    session.end_time = now()
    session.save()
    return redirect('dashboard')

# ================================
# Manual Pomodoro Log
# ================================

@login_required
def log_pomodoro_session(request):
    if request.method == 'POST':
        form = PomodoroLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.save()
            return redirect('dashboard')
    else:
        form = PomodoroLogForm()

    return render(request, 'log_pomodoro.html', {'form': form})

# ================================
# Habit Management
# ================================

@login_required
def add_habit(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            return redirect('dashboard')
    else:
        form = HabitForm()
    return render(request, 'add_habit.html', {'form': form})

@login_required
def edit_habit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    if request.method == 'POST':
        form = HabitForm(request.POST, instance=habit)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = HabitForm(instance=habit)
    return render(request, 'edit_habit.html', {'form': form, 'habit': habit})

@login_required
def delete_habit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    if request.method == 'POST':
        habit.delete()
        return redirect('dashboard')
    return render(request, 'delete_habit.html', {'habit': habit})

@login_required
def complete_habit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    habit.mark_completed()
    return redirect('dashboard')

@login_required
def archive_habit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    habit.is_archived = True
    habit.save()
    return redirect('dashboard')

@login_required
def unarchive_habit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    habit.is_archived = False
    habit.save()
    return redirect('archived_habits')

@login_required
def archived_habits(request):
    habits = Habit.objects.filter(user=request.user, is_archived=True)
    return render(request, 'archived_habits.html', {'habits': habits})

# ================================
# Mood Logging (with Sentiment)
# ================================

@login_required
def mood_log_view(request):
    if request.method == 'POST':
        form = MoodLogForm(request.POST)
        if form.is_valid():
            mood_entry = form.save(commit=False)
            mood_entry.user = request.user


            sentiment = predict_sentiment(mood_entry.note)
            mood_entry.sentiment = sentiment  # this should be 'positive' or 'negative'
            mood_entry.save()
            print(f"[DEBUG] Sentiment saved: {sentiment}")



            messages.success(request, f"Mood logged successfully! Sentiment: {sentiment}")
            return redirect('dashboard')
    else:
        form = MoodLogForm()

    return render(request, 'mood_log.html', {'form': form})
