from datetime import date, timedelta
from django.db import models
from django.contrib.auth.models import User

# ======================
# 🧠 Habit Model
# ======================
class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_completed = models.DateField(null=True, blank=True)
    streak = models.PositiveIntegerField(default=0)
    reminder_time = models.TimeField(null=True, blank=True)
    is_archived = models.BooleanField(default=False)  # ✅ Archive System

    def mark_completed(self):
        today = date.today()
        if self.last_completed == today:
            return
        elif self.last_completed == today - timedelta(days=1):
            self.streak += 1
        else:
            self.streak = 1
        self.last_completed = today
        self.save()

    def __str__(self):
        return f"{self.name} (Streak: {self.streak})"


# ======================
# ✅ Habit Completion Log
# ======================
class HabitCompletion(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='completions')
    date = models.DateField()

    def __str__(self):
        return f"{self.habit.name} on {self.date}"


# ======================
# 😊 Mood Log (with Sentiment)
# ======================
class MoodLog(models.Model):
    MOOD_CHOICES = [
        ('😊', 'Happy'),
        ('😐', 'Neutral'),
        ('😞', 'Sad'),
        ('😡', 'Angry'),
        ('😴', 'Tired'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mood = models.CharField(max_length=2, choices=MOOD_CHOICES)
    note = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)
    sentiment = models.CharField(max_length=10, blank=True)  # ✅ Sentiment from ML model

    def __str__(self):
        return f"{self.user.username} - {self.mood} on {self.date}"


# ======================
# ⏱️ Pomodoro Live Session
# ======================
class PomodoroSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    habit = models.ForeignKey(Habit, on_delete=models.SET_NULL, null=True, blank=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def duration_minutes(self):
        if self.end_time:
            delta = self.end_time - self.start_time
            return int(delta.total_seconds() / 60)
        return None

    def __str__(self):
        return f"{self.user.username} - Session ({self.start_time})"


# ======================
# 📘 Pomodoro Log (Manual Entry)
# ======================
class PomodoroLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    habit = models.ForeignKey(Habit, on_delete=models.SET_NULL, null=True, blank=True)
    start_time = models.DateTimeField(auto_now_add=True)
    duration_minutes = models.IntegerField(default=25)

    def __str__(self):
        return f"{self.user.username} - {self.habit.name if self.habit else 'Unassigned'} - {self.start_time}"
