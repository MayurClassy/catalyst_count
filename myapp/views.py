
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
import csv
import codecs

from .forms import UploadCSVForm, QueryBuilderForm
from .models import DataRecord

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'myapp/login.html')






from django.shortcuts import render
from .forms import QueryBuilderForm
from .models import DataRecord

def query_builder_view(request):
    form = QueryBuilderForm(request.GET or None)
    data = []
    record_count = 0

    if request.method == 'GET' and form.is_valid():
        queryset = DataRecord.objects.all()
        
        # Apply filters based on form input
        for field, value in form.cleaned_data.items():
            if value:
                filter_kwargs = {f"{field}__icontains": value}
                queryset = queryset.filter(**filter_kwargs)
        
        # Remove duplicates
        queryset = queryset.distinct()
        
        record_count = queryset.count()
        
        # Convert queryset to list of dictionaries
        data = list(queryset.values(
            'name', 'domain', 'year_founded', 'industry', 'size_range', 
            'locality', 'country', 'linkedin_url', 'current_employee_estimate', 
            'total_employee_estimate'
        ))

        # Get record count
       

    return render(request, 'myapp/query_builder.html', {'query_form': form, 'data': data, 'record_count': record_count})




# views.py
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import DataRecord
from .serializers import DataRecordSerializer

@api_view(['GET'])
def record_count_view(request):
    filters = request.GET
    queryset = DataRecord.objects.all()
    
    for field, value in filters.items():
        if value:
            filter_kwargs = {f"{field}__icontains": value}
            queryset = queryset.filter(**filter_kwargs)
    
    record_count = queryset.count()
    return Response({'record_count': record_count})




from django.shortcuts import render, redirect
from django.contrib.auth.models import User

def users_view(request):
    users = User.objects.all()
    return render(request, 'myapp/users.html', {'users': users})

def add_user_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if username and email and password:
            User.objects.create_user(username=username, email=email, password=password)
            return redirect('users')
        else:
            return redirect('users')
    return redirect('users')



@login_required
def dashboard_view(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            fs = FileSystemStorage()
            filename = fs.save(csv_file.name, csv_file)
            try:
                with fs.open(filename, 'rb') as f:
                    reader = csv.DictReader(codecs.iterdecode(f, 'utf-8'))
                    for row in reader:
                        mapped_row = {
                            'name': row.get('name'),
                            'domain': row.get('domain'),
                            'year_founded': row.get('year founded'),
                            'industry': row.get('industry'),
                            'size_range': row.get('size range'),
                            'locality': row.get('locality'),
                            'country': row.get('country'),
                            'linkedin_url': row.get('linkedin url'),
                            'current_employee_estimate': row.get('current employee estimate'),
                            'total_employee_estimate': row.get('total employee estimate'),
                        }
                        DataRecord.objects.create(**mapped_row)
                messages.success(request, 'File uploaded successfully!')
            except UnicodeDecodeError:
                messages.error(request, 'Error decoding file. Please ensure it is UTF-8 encoded.')
            except Exception as e:
                messages.error(request, f'An error occurred: {e}')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid form submission.')
    elif request.method == 'GET' and 'name' in request.GET:
        query_form = QueryBuilderForm(request.GET)
        if query_form.is_valid():
            queryset = DataRecord.objects.all()
            for field, value in query_form.cleaned_data.items():
                if value:
                    filter_kwargs = {f"{field}__icontains": value}
                    queryset = queryset.filter(**filter_kwargs)
            return JsonResponse({'count': queryset.count()})
        else:
            return JsonResponse({'message': 'Invalid query!'})

    form = UploadCSVForm()
    query_form = QueryBuilderForm()
    users = User.objects.all()
    return render(request, 'myapp/dashboard.html', {'form': form, 'query_form': query_form, 'users': users})



