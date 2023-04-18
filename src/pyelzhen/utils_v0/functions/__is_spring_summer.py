from django.utils import timezone


def isSpringSummer():
    # base should be local time not UTC, but because this time send to device analyzer, we couldn't do anything else:
    today = timezone.now()

    result = False

    if today.month == 3:
        # month == March
        if today.day >= 21:
            result = True
        else:
            result = False

    elif today.month == 9:
        # month == September
        if today.day >= 22:
            result = False
        else:
            result = True
    elif today.month > 3 and today.month < 9:
        result = True
    elif today.month > 9:
        result = False

    return result
