from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


from django.shortcuts import render, redirect, get_object_or_404
from .models import UserIndicator
from .forms import UserIndicatorForm


@login_required
def indicator_list(request):
    indicators = UserIndicator.objects.filter(user=request.user)
    return render(request,"indicators/list.html",{"indicators": indicators})


@login_required
def add_indicator(request):
    if request.method == "POST":
        form = UserIndicatorForm(request.POST)
        if form.is_valid():
            indicator = form.save(commit=False)
            indicator.user = request.user
            indicator.save()
            return redirect("indicator_list")

    else:

        form = UserIndicatorForm()
    return render(request,"indicators/add.html",{"form": form})






@login_required
def edit_indicator(request, pk):
    indicator = get_object_or_404(UserIndicator, pk=pk, user=request.user)

    if request.method == "POST":
        form = UserIndicatorForm(request.POST, instance=indicator)
        if form.is_valid():
            form.save()
            return redirect("indicator_list")
    else:
        form = UserIndicatorForm(instance=indicator)

    return render(request, "indicators/add.html", {"form": form})


@login_required
def delete_indicator(request, pk):
    indicator = get_object_or_404(UserIndicator, pk=pk, user=request.user)

    if request.method == "POST":
        indicator.delete()
        return redirect("indicator_list")

    return render(request, "indicators/delete.html", {"indicator": indicator})