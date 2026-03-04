from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import File, AccessLog

@login_required
def dashboard(request):
    files = File.objects.filter(user=request.user)

    if request.method == "POST":
        uploaded_file = request.FILES.get('file')
        if uploaded_file:
            File.objects.create(user=request.user, file=uploaded_file)
            return redirect('dashboard')

    return render(request, 'dashboard.html', {'files': files})
from django.http import FileResponse, Http404
import os
from django.conf import settings

@login_required
def download_file(request, file_id):
    try:
        file_obj = File.objects.get(id=file_id)
    except File.DoesNotExist:
        raise Http404("File not found")

    # Security check
    if file_obj.user != request.user and not request.user.is_staff:
        raise Http404("Unauthorized")

    # Log access
    AccessLog.objects.create(file=file_obj, accessed_by=request.user)

    # ✅ Increase download count
    file_obj.download_count += 1
    file_obj.save()

    file_path = file_obj.file.path
    return FileResponse(open(file_path, 'rb'), as_attachment=True)

@login_required
def delete_file(request, file_id):
    file_obj = File.objects.get(id=file_id, user=request.user)
    file_obj.delete()
    return redirect('dashboard')