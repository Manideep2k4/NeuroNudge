
from celery import shared_task
from django.utils.timezone import localtime, now
from .models import Habit
from django.core.mail import send_mail

@shared_task
def send_habit_reminders():
    current_time = localtime(now()).time()
    habits = Habit.objects.filter(reminder_time__hour=current_time.hour,
                                  reminder_time__minute=current_time.minute)

    for habit in habits:
        user = habit.user
        message = f"❓ Have you completed your habit: '{habit.name}' today?"
        
        # Placeholder: Print to console (later can be push/email/smartwatch)
        print(f"[Reminder] {user.username}: {message}")
        
        # Optionally send email (or push)
        send_mail(
            subject="NeuroNudge Habit Reminder",
            message=message,
            from_email="noreply@neuronudge.com",
            recipient_list=[user.email],
            fail_silently=True
        )
