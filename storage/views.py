import os
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404
from .models import File, AccessLog






# ----------------------------
# Dashboard
# ----------------------------

@login_required
def dashboard(request):

    files = File.objects.filter(user=request.user)

    # Temporary storage calculation
    total_files = files.count()

    # Assume avg 5MB per file (Cloudinary doesn't expose size easily)
    total_size = total_files * 5 * 1024 * 1024

    quota = 100 * 1024 * 1024

    storage_used_percent = int((total_size / quota) * 100) if quota > 0 else 0

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

    # security check
    if file_obj.user != request.user and not request.user.is_staff:
        raise Http404("Unauthorized")

    # log access
    AccessLog.objects.create(
        file=file_obj,
        accessed_by=request.user
    )

    file_obj.download_count += 1
    file_obj.save()

    # redirect to Cloudinary file
    return redirect(file_obj.file.url)

# ----------------------------
# Delete file
# ----------------------------

@login_required
def delete_file(request, file_id):

    try:
        file_obj = File.objects.get(
            id=file_id,
            user=request.user
        )

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

    return render(
        request,
        "registration/register.html",
        {"form": form}
    )


# ----------------------------
# Share download link
# ----------------------------



def share_download(request, token):

    try:
        file_obj = File.objects.get(share_token=token)
    except File.DoesNotExist:
        raise Http404("File not found")

    file_obj.download_count += 1
    file_obj.save()

    return redirect(file_obj.file.url)