from django.urls import path
from . import views

urlpatterns = [
    # Landing & Authentication
    path('', views.landing_view, name='landing'),
    path('register/', views.register, name='register'),
    path('login/', views.login_l, name='login'),
    path('logout/', views.logout_l, name='logout'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Habit Management
    path('add/', views.add_habit, name='add_habit'),
    path('edit/<int:habit_id>/', views.edit_habit, name='edit_habit'),
    path('delete/<int:habit_id>/', views.delete_habit, name='delete_habit'),
    path('complete/<int:habit_id>/', views.complete_habit, name='complete_habit'),
    path('archive_habit/<int:habit_id>/', views.archive_habit, name='archive_habit'),
    path('unarchive_habit/<int:habit_id>/', views.unarchive_habit, name='unarchive_habit'),
    path('archived/', views.archived_habits, name='archived_habits'),

    # Mood Tracking with Sentiment Analysis
    path('mood/', views.mood_log_view, name='mood_log'),


    # Pomodoro Timer (Live)
    path('pomodoro/start/', views.start_pomodoro, name='start_pomodoro'),
    path('pomodoro/stop/<int:session_id>/', views.stop_pomodoro, name='stop_pomodoro'),

    # Pomodoro Manual Logging
    path('log_pomodoro/', views.log_pomodoro_session, name='log_pomodoro'),
]
