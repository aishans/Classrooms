from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Classroom,Student
from .forms import ClassroomForm, SignupForm, SigninForm, AddStudent 
from django.contrib.auth import login, authenticate, logout

def signup(request):
	if request.user.is_authenticated:
		return redirect("classroom-list")
	form = SignupForm()
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)

			user.set_password(user.password)
			user.save()

			login(request, user)
			return redirect("classroom-list")
	context = {
		"form":form,
	}
	Student.objects.filter(gender=Student.MALE)
	return render(request, 'signup.html', context)

def signin(request):
	if request.user.is_authenticated:
		return redirect("classroom-create")
	form = SigninForm()
	if request.method == 'POST':
		form = SigninForm(request.POST)
		if form.is_valid():

			username = form.cleaned_data['username']
			password = form.cleaned_data['password']

			auth_user = authenticate(username=username, password=password)
			if auth_user is not None:
				login(request, auth_user)
				return redirect('classroom-list')
	context = {
		"form":form
	}
	return render(request, 'signin.html', context)

def signout(request):
	logout(request)
	return redirect("signin")

def classroom_list(request):
	classrooms = Classroom.objects.all()
	context = {
		"classrooms": classrooms,
	}
	return render(request, 'classroom_list.html', context)


def classroom_detail(request, classroom_id):
	classroom = Classroom.objects.get(id=classroom_id)
	context = {
		"classroom": classroom,
		"my_students" : Student.objects.filter(classroom=classroom).order_by('name')

	}
	return render(request, 'classroom_detail.html', context)


def classroom_create(request):
	
	if request.user.is_anonymous:
		return redirect('signin')      
	form = ClassroomForm()
	if request.method == "POST":
		form = ClassroomForm(request.POST, request.FILES or None)
		if form.is_valid():
			classroom=form.save(commit=False)
			classroom.teacher = request.user
			classroom.save()
			return redirect('classroom-list')

			
		print (form.errors)
	context = {
	"form": form,
	}
	return render(request, 'create_classroom.html', context)


def classroom_update(request, classroom_id):
	classroom = Classroom.objects.get(id=classroom_id)
	form = ClassroomForm(instance=classroom)
	if request.method == "POST":
		form = ClassroomForm(request.POST, request.FILES or None, instance=classroom)
		if form.is_valid():
			form.save()
			return redirect('classroom-list')
		print (form.errors)
	context = {
	"form": form,
	"classroom": classroom,
	}
	return render(request, 'update_classroom.html', context)


def classroom_delete(request, classroom_id):
	Classroom.objects.get(id=classroom_id).delete()
	return redirect('classroom-list')

def add_student(request):
	form = AddStudent()
	if request.method == "POST":
		form = AddStudent(request.POST)
		if form.is_valid():
			messages.success(request, "Added")
			return redirect("classroom-list")
	context = {
		"form":form,
	}
	return render(request, 'addstudent.html', context)