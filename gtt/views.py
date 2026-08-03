from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404

from stocks.models import Stock
from .models import GTTOrder
from .forms import GTTOrderForm

@login_required
def create_gtt(request, pk):
    stock = get_object_or_404(Stock, pk=pk)
    if request.method == "POST":
        form = GTTOrderForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.stock = stock
            order.save()

            messages.success(request, "GTT Order Created Successfully.")
            return redirect("gtt_list")

    else:
        form = GTTOrderForm()

    return render(request,"gtt/create.html",{"form": form,"stock": stock,},)


@login_required
def gtt_list(request):

    orders = GTTOrder.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(request,"gtt/list.html",{"orders": orders,},)




@login_required
def edit_gtt(request, pk):
    order = get_object_or_404(
        GTTOrder,
        pk=pk,
        user=request.user
    )

    if order.status != "ACTIVE":
        messages.error(request, "Only active GTT orders can be modified.")
        return redirect("gtt_list")

    if request.method == "POST":
        form = GTTOrderForm(request.POST, instance=order)

        if form.is_valid():
            form.save()
            messages.success(request, "GTT Order Updated Successfully.")
            return redirect("gtt_list")

    else:
        form = GTTOrderForm(instance=order)

    return render(request,"gtt/create.html",{"form": form,"stock": order.stock,},)



@login_required
def cancel_gtt(request, pk):
    order = get_object_or_404(
        GTTOrder,
        pk=pk,
        user=request.user
    )

    if order.status == "ACTIVE":
        order.status = "CANCELLED"
        order.save()

        messages.success(request, "GTT Order Cancelled.")

    return redirect("gtt_list")