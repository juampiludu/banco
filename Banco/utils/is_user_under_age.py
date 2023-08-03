from django.utils import timezone

def is_user_under_age(born_date):
    current_date = timezone.localdate()
    eighteen_years_ago = current_date.replace(year=current_date.year - 18)
    return born_date > eighteen_years_ago