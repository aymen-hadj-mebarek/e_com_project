from django.shortcuts import render , redirect
from django.http import HttpResponse
from .models import * 
from .forms import ProfileChangeForm
# Create your views here.

def userprofile(request):
    if request.user.is_authenticated:
        pr = UserProfile.objects.get(user=request.user)
        
    else :
        return HttpResponse("user is logged out ")
    
    context={'profile':pr}
    return  render(request,'profileapp/profile.html', context)

def editprofile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileChangeForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('userprofile')  # Redirect to the profile view after successful update
    else:
        form = ProfileChangeForm(instance=user_profile)
    return render(request, 'profileapp/editprofile.html', {'form': form})