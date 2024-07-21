from django.contrib import admin
from .models import DataRecord

@admin.register(DataRecord)
class DataRecordAdmin(admin.ModelAdmin):
    list_display = ('name', 'domain', 'year_founded', 'industry', 'size_range', 'locality', 'country', 'linkedin_url', 'current_employee_estimate', 'total_employee_estimate')
    
    


