
from django.shortcuts import render

from ..models.blacklist import BlackList


def unsubscribe(request):
    """
    Unsubscribe from the mailing list.
    """
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if email:
            # Check if the email is already in the blacklist
            if not BlackList.objects.filter(email=email).exists():
                # Add the email to the blacklist
                BlackList.objects.create(email=email)
                return render(request, 'unsubscribe.html', {'email': email, 'success': True})
            else:
                return render(request, 'unsubscribe.html', {'email': email, 'success': True})
    else:
        email = request.GET.get('email', '').strip()
    
    return render(request, 'unsubscribe.html', {'email': email, 'success': False})
