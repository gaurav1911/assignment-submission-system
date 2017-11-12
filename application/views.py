from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from .forms import SolutionForm, UserProfileForm, UserForm
from .models import Assignment, Solution, UserProfile
import datetime
from django.shortcuts import redirect

# Create your views here.
def index(request):
	if not request.user.is_authenticated():
		return render(request, 'application/index.html')
	else:
		return redirect('application:profile')

def detail(request, assign_id):
	if not request.user.is_authenticated():
		return render(request, 'application/index.html', {'error_message': "You must be logged in!!"})
	else:
		user = request.user
		assign = get_object_or_404(Assignment, pk=assign_id)
		return render(request, 'application/details.html', {'assignment': assign, 'user': user})

def profile(request):
	if not request.user.is_authenticated():
		return render(request, 'application/index.html')
	else:
		usr_profile = UserProfile.objects.get(user=request.user)
		usr_assign = Assignment.objects.filter(year=usr_profile.year)
		usr_soln = Solution.objects.filter(student=usr_profile)
		print(len(usr_assign))
		print(len(usr_assign))
		return render(request, 'application/profile.html', {
			'assignments': usr_assign,
			'solutions': usr_soln
		})


def logout_user(request):
	logout(request)
	return HttpResponseRedirect('/application/')

def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				# usr_year = UserProfile.objects.get(user=request.user).year
				# usr_assign = Assignment.objects.filter(year=year)
				# rno = UserProfile.objects.get(user=request.user).roll_no
				return redirect('application:profile')
			else:
				return render(request, 'application/index.html', {'error_message': 'Your account has been disabled'})
		else:
			return render(request, 'application/index.html', {'error_message': 'Invalid login'})
	return render(request, 'application/index.html')

def register(request):
	# context = RequestContext(request)
	if request.user.is_authenticated():
		return render(request, 'application/profile.html', {'error_message':"You are already registered!!"})
	else:
		user_form = UserForm(request.POST or None)
		profile_form = UserProfileForm(request.POST or None)
		registered = False
		if request.method == 'POST':
			if user_form.is_valid() and profile_form.is_valid():
				user = user_form.save(commit=False)
				username = user_form.cleaned_data['username']
				password = user_form.cleaned_data['password']
				user.set_password(user.password)
				user.save()
				profile = profile_form.save(commit=False)
				profile.user = user
				profile.save()
				registered = True
				user = authenticate(username=username, password=password)
				if user is not None:
					if user.is_active:
						login(request, user)
						return redirect('application:profile')

		context = {
			"pform": profile_form,
			"uform": user_form,
		}
		return render(request, 'application/register.html', context)


def submit(request):
	if not request.user.is_authenticated():
		return render(request, 'application/index.html')
	else:
		if request.method == 'POST':
			form = SolutionForm(user=request.user, data=request.POST, files=request.FILES)
			if form.is_valid():
				solution = form.save(commit=False)
				solution.student = UserProfile.objects.get(user=request.user)
				solution.file = request.FILES['file']
				file_type = solution.file.url.split('.')[-1]
				file_type = file_type.lower()
				solution.save()
				return redirect('application:profile')
		else:
			print("###########")
			# print(request.user)
			# usr_year = UserProfile.objects.get(user=request.user).year
			# usr_assign = Assignment.objects.filter(year=usr_year)
			form = SolutionForm(user=request.user)
		return render(request, 'application/sol_submit.html', {'form': form})
