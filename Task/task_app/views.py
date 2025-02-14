from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from .forms import CustomUserCreationForm, TaskForm, TaskFilterForm
from .models import Task
from django.db.models import Q
from django.views.decorators.cache import cache_control
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from io import BytesIO

# Authentication views
def home(request):
    return render(request, 'task_app/home.html')


def welcome(request):
    return render(request, 'task_app/welcome.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('task_app:user_login')
        else:
            messages.error(request, 'There was an error in your registration form. Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'task_app/register.html', {'form': form})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('task_app:welcome')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid form submission.')
    else:
        form = AuthenticationForm()
    return render(request, 'task_app/login.html', {'form': form})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('task_app:user_login')


@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        new_email = request.POST.get('email')
        if new_email:
            user.email = new_email
            user.save()
            messages.success(request, 'Profile updated successfully!')
        else:
            messages.error(request, 'Please provide a valid email address.')
        return redirect('task_app:welcome')
    return render(request, 'task_app/update_profile.html')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)  # Prevent logout after password change
            messages.success(request, 'Password updated successfully!')
            return redirect('task_app:welcome')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'task_app/change_password.html', {'form': form})


def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            associated_users = User.objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "task_app/password_reset_email.txt"

                    context = {
                        "email": user.email,
                        "domain": request.get_host(),
                        "site_name": "Task App",
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        "token": default_token_generator.make_token(user),
                        "protocol": request.scheme,
                    }

                    email_body = render_to_string(email_template_name, context)

                    send_mail(
                        subject,
                        email_body,
                        'your_email@example.com',  # Replace with your email
                        [user.email],
                        fail_silently=False,
                    )

                messages.success(request, 'A password reset email has been sent.')
                return redirect('task_app:user_login')
            else:
                messages.error(request, 'No user is associated with this email.')
    else:
        form = PasswordResetForm()

    return render(request, 'task_app/password_reset.html', {'form': form})


# Task views
@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_app:task_list')
    else:
        form = TaskForm()
    return render(request, 'task_app/task_form.html', {'form': form})


@login_required
def task_update(request, pk):
    task = Task.objects.get(pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_app:task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_app/task_form.html', {'form': form})


@login_required
def task_delete(request, pk):
    task = Task.objects.get(pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_app:task_list')
    return render(request, 'task_app/task_confirm_delete.html', {'task': task})




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)

    if not request.user.is_authenticated:
        # Show read-only tasks for unauthenticated users
        return render(request, 'task_app/task_read_only.html', {'tasks': tasks})

    filter_form = TaskFilterForm(request.GET)
    if filter_form.is_valid():
        name = filter_form.cleaned_data.get('name')
        description = filter_form.cleaned_data.get('description')
        status = filter_form.cleaned_data.get('status')
        start_date = filter_form.cleaned_data.get('start_date')
        end_date = filter_form.cleaned_data.get('end_date')

        if name:
            tasks = tasks.filter(name__icontains=name)
        if description:
            tasks = tasks.filter(description__icontains=description)
        if status:
            tasks = tasks.filter(status=status)
        if start_date:
            tasks = tasks.filter(created_at__gte=start_date)
        if end_date:
            tasks = tasks.filter(created_at__lte=end_date)

    # Check if the user requested PDF export
    if request.GET.get('export') == 'pdf':
        return generate_pdf_report(tasks)

    return render(request, 'task_app/task_list.html', {'tasks': tasks, 'filter_form': filter_form})

def generate_pdf_report(tasks):
    # Load the task data into the template
    html_template = render_to_string('task_app/task_pdf_template.html', {'tasks': tasks})

    # Generate the PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="tasks_report.pdf"'
    pisa_status = pisa.CreatePDF(html_template, dest=response)

    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)

    return response
