from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import (UserRegisterForm,
	UserUpdateForm, ProfileUpdateForm)
from django.contrib.auth.decorators import login_required


def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		# validate that we have the data we want
		if form.is_valid():
			# it'll save user with all the
			# password hashing
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f"Account was created: {username}")
			return redirect('login')
	else:
		form = UserRegisterForm()
	return render(request, 'users/register.html',
		{'form': form})


@login_required
def user_profile(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST,
								   request.FILES,
								   instance=request.user.profile)

		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f'Your acc has been updated!')
			return redirect('profile')

	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)
		
	context = {
		'u_form': u_form,
		'p_form': p_form
	}

	return render(request, 'users/profile.html', context)
