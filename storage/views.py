import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, Http404

from .models import File, AccessLog


# ----------------------------
# Dashboard
# ----------------------------

@login_required
def dashboard(request):

    files = File.objects.filter(user=request.user)

    # simple estimation (Cloudinary does not expose size easily)
    total_files = files.count()
    total_size = total_files * 5 * 1024 * 1024

    quota = 100 * 1024 * 1024

    storage_used_percent = int((total_size / quota) * 100)
    used_mb = round(total_size / (1024 * 1024), 2)
    quota_mb = 100

    if request.method == "POST":

        uploaded_file = request.FILES.get("file")

        if uploaded_file:
            File.objects.create(
                user=request.user,
                file=uploaded_file
            )

            return redirect("dashboard")

    return render(
        request,
        "dashboard.html",
        {
            "files": files,
            "storage_used_percent": storage_used_percent,
            "used_mb": used_mb,
            "quota_mb": quota_mb,
        },
    )


# ----------------------------
# Download file
# ----------------------------

@login_required
def download_file(request, file_id):

    try:
        file_obj = File.objects.get(id=file_id)
    except File.DoesNotExist:
        raise Http404("File not found")

    if file_obj.user != request.user and not request.user.is_staff:
        raise Http404("Unauthorized")

    file_url = file_obj.file.url

    response = requests.get(file_url)

    filename = f"{file_obj.file.public_id}.{file_obj.file.format}"

    http_response = HttpResponse(
        response.content,
        content_type="application/octet-stream"
    )

    http_response["Content-Disposition"] = f'attachment; filename="{filename}"'

    file_obj.download_count += 1
    file_obj.save()

    return http_response


# ----------------------------
# Delete file
# ----------------------------

@login_required
def delete_file(request, file_id):

    try:
        file_obj = File.objects.get(id=file_id, user=request.user)
    except File.DoesNotExist:
        raise Http404("File not found")

    file_obj.delete()

    return redirect("dashboard")


# ----------------------------
# Register user
# ----------------------------

def register(request):

    if request.method == "POST":

        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("login")

    else:
        form = UserCreationForm()

    return render(request, "registration/register.html", {"form": form})


# ----------------------------
# Share download link
# ----------------------------

def share_download(request, token):

    try:
        file_obj = File.objects.get(share_token=token)
    except File.DoesNotExist:
        raise Http404("File not found")

    file_url = file_obj.file.url

    response = requests.get(file_url)

    filename = f"{file_obj.file.public_id}.{file_obj.file.format}"

    http_response = HttpResponse(
        response.content,
        content_type="application/octet-stream"
    )

    http_response["Content-Disposition"] = f'attachment; filename="{filename}"'

    file_obj.download_count += 1
    file_obj.save()

    return http_response