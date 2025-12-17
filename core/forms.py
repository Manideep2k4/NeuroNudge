from django import forms
from django.contrib.auth.models import User
from .models import Habit, MoodLog, PomodoroSession, PomodoroLog

# ================================
# 🔐 User Registration Form
# ================================
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

# ================================
# 📋 Habit Form with Reminder
# ================================
class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['name', 'description', 'reminder_time']
        widgets = {
            'reminder_time': forms.TimeInput(attrs={'type': 'time'}),
        }

# ================================
# 😊 Mood Logging Form
# ================================
class MoodLogForm(forms.ModelForm):
    class Meta:
        model = MoodLog
        fields = ['mood', 'note']
        widgets = {
            'mood': forms.Select(attrs={'class': 'form-select rounded-pill'}),
            'note': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your thoughts...'
            }),
        }

# ================================
# ⏱️ Pomodoro Session Form (Live)
# ================================
class PomodoroSessionForm(forms.ModelForm):
    class Meta:
        model = PomodoroSession
        fields = ['habit']
        widgets = {
            'habit': forms.Select(attrs={'class': 'form-select'}),
        }

# ================================
# 📝 Pomodoro Log Form (Manual)
# ================================
class PomodoroLogForm(forms.ModelForm):
    class Meta:
        model = PomodoroLog
        fields = ['habit', 'duration_minutes']
        widgets = {
            'habit': forms.Select(attrs={'class': 'form-select'}),
            'duration_minutes': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '5',
                'step': '5'
            }),
        }
