from .models import UserLog

def log_activity(user, action, target_model, description):
    """
    Fungsi bantu untuk menyimpan log aktivitas user.
    """
    if user.is_authenticated:
        UserLog.objects.create(
            user=user,
            action=action,
            target_model=target_model,
            description=description
        )