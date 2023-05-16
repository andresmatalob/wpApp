from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Company, Department, Task, Project, User
import json

@login_required
def create_company(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email_com = request.POST.get('email_com', None)
        num_workers = request.POST.get('num_workers')
        created_by_id = request.user.id
        created_by = User.objects.get(pk=created_by_id)
        if not email_com:
            email_com = None
        company = Company.objects.create(name=name, email_com=email_com, num_workers=num_workers, admin=request.user)
        company.workers.add(request.user)
        company.admin = request.user
        messages.success(request, f'{name} has been created.')
        return redirect('web-home')

    return render(request, 'web/create_company.html')

def add_user_to_company(request, company_id):
    company = get_object_or_404(Company, id=company_id)

    if request.method == 'POST':
        username = request.POST.get('username')
        user = get_object_or_404(User, username=username)
        if user in company.workers.all():
            messages.warning(request, f'{username} is already a member of {company.name}.')
        else:
            company.workers.add(user)
            messages.success(request, f'{username} has been added to {company.name}.')
        return redirect('company_detail', company_id=company_id)

    context = {
        'company': company,
    }
    return render(request, 'company.html', context)

@login_required
def add_user_to_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    company_id = Company.objects.filter(departments=department_id).first().id
    if request.method == 'POST':
        username = request.POST.get('username')
        user = get_object_or_404(User, username=username)
        if user in department.users.all():
            messages.warning(request, f'{username} is already a member of {department.name}.')
        else:
            department.users.add(user)
            messages.success(request, f'{username} has been added to {department.name}.')
        return redirect('department_detail', department_id=department_id, company_id=company_id)

@csrf_exempt
def create_department(request, company_id):
    company = Company.objects.get(id=company_id)
    if request.method == 'POST':
        data = json.loads(request.body)
        department_name = data.get('name', '')
        department = Department.objects.create(name=department_name, admin=request.user)
        company.departments.add(department)
        user_id = request.user.id
        user = User.objects.get(pk=user_id)
        department.users.add(user)
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
    
@csrf_exempt
def modify_task(request, task_id):
    task = Task.objects.get(id=task_id)

    if request.method == 'POST':
        data = json.loads(request.body)
        new_task_name = data['name']
        task.name = new_task_name
        task.save()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False})

@csrf_exempt
def create_project(request, department_id):
    print("Request method:", request.method)
    department = Department.objects.get(id=department_id)
    if request.method == 'POST':
        data = json.loads(request.body)
        created_by_id = request.user.id
        project_name = data.get('name', '')
        project = Project.objects.create(name=project_name, admin=request.user)
        default_task = Task.objects.create(name='default')
        project.tasks.add(default_task)
        department.projects.add(project)
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@csrf_exempt
def add_task(request, project_id):
    project = Project.objects.get(id=project_id)
    if request.method == 'POST':
        data = json.loads(request.body)
        task_name = data.get('name', '')
        task = Task.objects.create(name=task_name)
        project.tasks.add(task)
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
    
@csrf_exempt
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    if request.method == 'POST':
        task.delete()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
    
    
@csrf_exempt
def delete_project(request, project_id):
    project = Project.objects.get(id=project_id)
    if project.admin == request.user:
        if request.method == 'POST':
            project.delete()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
    else: 
        print("He has no permission to delete this project.")
        return JsonResponse({'status': 'error', 'message': 'You have no rights to delete this.(You are not the creator).'})
    
@csrf_exempt
def delete_company(request, company_id):
    company = Company.objects.get(id=company_id)
    if company.admin == request.user:
        if request.method == 'POST':
            company.delete()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
    else: 
        print("He has no permission to delete this project.")
        return JsonResponse({'status': 'error', 'message': 'You have no rights to delete this.(You are not the creator).'})

@csrf_exempt
def delete_department(request, department_id):
    department = Department.objects.get(id=department_id)
    if department.admin == request.user:
        if request.method == 'POST':
            department.delete()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
    else: 
        print("He has no permission to delete this project.")
        return JsonResponse({'status': 'error', 'message': 'You have no rights to delete this.(You are not the creator).'})
    
@csrf_exempt
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Account was created for ' + form.cleaned_data.get('username'))
            return redirect('login_user')
    context = {'form':form}

    return render(request, 'registration/register.html', context) 

@csrf_exempt
def loginPage(request):
    """if request.user.is_authenticated:
        return redirect('web-home')
    else:"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            #return redirect('web-home')
            return redirect('web-home')
        else:
            messages.info(request, 'Username OR password is incorrect')
    context = {}
    return render(request, 'registration/login.html', context)

def company_detail(request, company_id):
    company = get_object_or_404(Company, pk=company_id)
    return render(request, 'models/company_detail.html', {'company': company})

def department_detail(request, department_id, company_id):
    department = get_object_or_404(Department, pk=department_id)
    company = get_object_or_404(Company, pk=company_id)
    return render(request, 'models/department_detail.html', {'department': department, 'company': company })

def logoutPage(request):
    logout(request)
    return redirect('login_user')

@login_required(login_url='registration/login')
def home(request):
    companies = Company.objects.filter(workers=request.user)
    return render(request, 'web/home.html',  {'companies': companies}) #

@login_required(login_url='registration/login')
def about(request):
    return render(request, 'web/about.html', {'title': 'About Us'})