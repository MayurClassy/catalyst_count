import os
import csv
import codecs
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, UploadCSVForm, QueryBuilderForm
from .models import DataRecord
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt

def login_view(request):
    if request.method == "POST":
        try:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password')
        except Exception as e:
            messages.error(request, 'An error occurred: {}'.format(str(e)))
    return render(request, 'myapp/login.html')


@login_required
def query_builder_view(request):
    form = QueryBuilderForm(request.GET or None)
    data = []
    record_count = 0

    if request.method == 'GET' and form.is_valid():
        queryset = DataRecord.objects.all()
        
        filters_applied = False
        for field, value in form.cleaned_data.items():
            if value:
                filter_kwargs = {f"{field}__icontains": value}
                queryset = queryset.filter(**filter_kwargs)
                filters_applied = True
        
        record_count = queryset.count()
        
        data = list(queryset.values(
            'name', 'domain', 'year_founded', 'industry', 'size_range', 
            'locality', 'country', 'linkedin_url', 'current_employee_estimate', 
            'total_employee_estimate'
        ))

    else:
        
        record_count = DataRecord.objects.count()

    return render(request, 'myapp/query_builder.html', {
        'query_form': form, 
        'data': data, 
        'record_count': record_count,
    })





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


@login_required
def users_list(request):
    users = User.objects.all()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_superuser = True  
            user.is_staff = True      
            user.save()
            messages.success(request, 'New user has been successfully added!')
            return redirect('users_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'myapp/users.html', {'users': users, 'form': form})



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




@csrf_exempt
def upload_chunk(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        chunk_index = int(request.POST.get('chunk_index', 0))
        total_chunks = int(request.POST.get('total_chunks', 0))
        filename = request.POST.get('filename')

        if not file:
            return JsonResponse({'status': 'No file uploaded'}, status=400)

        fs = FileSystemStorage()
        chunk_path = fs.save(f'{filename}.part{chunk_index}', file)
        
        if chunk_index + 1 == total_chunks:
            
            full_path = fs.path(filename)
            with open(full_path, 'wb') as full_file:
                for i in range(total_chunks):
                    part_path = fs.path(f'{filename}.part{i}')
                    with open(part_path, 'rb') as part_file:
                        full_file.write(part_file.read())
                    os.remove(part_path)
            
           
            process_file(full_path)
            
            return JsonResponse({'status': 'File uploaded and processed successfully!'})

        return JsonResponse({'status': 'Chunk uploaded successfully!'})

    return JsonResponse({'status': 'Failed to upload chunk.'}, status=400)

def process_file(filepath):

    with open(filepath, 'rb') as f:
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
            try:
                DataRecord.objects.create(**mapped_row)
            except Exception as e:
                print(f"Error saving record {mapped_row}: {e}")
