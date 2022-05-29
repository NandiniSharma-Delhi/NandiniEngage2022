from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm


# page to register user
def register(request):
    if request.method == 'POST':
        # if user wants to register
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'account created for {username}!Now Login')
            #redirect to login page
            return redirect('login')
    else:
        form = UserRegisterForm()
    #normally just continue to register.html
    return render(request,'users/register.html',{'form':form})


#login required to access profile
@login_required
def profile(request):
    if request.method == 'POST':
        #form saved to update the credentials in the profile
        u_form = UserUpdateForm(request.POST,instance=request.user)
        if u_form.is_valid() :
            u_form.save()
            messages.success(request, f'Account Updated')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
    context ={
        'u_form':u_form,
    }
    #context is passed to prefill the update form with old credentials of user
    return render(request,'users/profile.html',context)
    

