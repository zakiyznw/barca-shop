from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from main.forms import ProductForm
from main.models import Product
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
import requests
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import strip_tags
import json
from django.http import JsonResponse


@login_required(login_url='/login')
def show_main(request):
    product_list = Product.objects.all()
    filter_type = request.GET.get("filter", "all") 
    
    if filter_type == "all":
        product_list = Product.objects.all()
    
    else:
        product_list = Product.objects.filter(user=request.user)

    context = {
        "product_list": product_list,
        'last_login': request.COOKIES.get('last_login', 'Never')
    }

    return render(request, "main.html", context)


def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product_entry = form.save(commit = False)
            product_entry.user = request.user
            product_entry.save()
            return redirect("main:show_main")
    else:
        form = ProductForm()

    context = {"form": form}
    return render(request, "add_product.html", context)


@login_required(login_url='/login')
def show_product(request, id):
    product = get_object_or_404(Product, pk=id)

    context = {
        "product": product
    }

    return render(request, "product_detail.html", context)


def show_xml(request):
    product_list = Product.objects.all()
    xml_data = serializers.serialize("xml", product_list)
    return HttpResponse(xml_data, content_type="application/xml")


def show_json(request):
    product_list = Product.objects.all()
    json_data = serializers.serialize("json", product_list)
    return HttpResponse(json_data, content_type="application/json")


def show_xml_by_id(request, product_id):
    try:
        product_item = Product.objects.filter(pk=product_id)
        xml_data = serializers.serialize("xml", product_item)
        return HttpResponse(xml_data, content_type="application/xml")
    except Product.DoesNotExist:
        return HttpResponse(status=404)


def show_json_by_id(request, product_id):
    try:
        product_item = Product.objects.get(pk=product_id)
        json_data = serializers.serialize("json", [product_item])
        return HttpResponse(json_data, content_type="application/json")
    except Product.DoesNotExist:
        return HttpResponse(status=404)
    

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)


def login_user(request):
   if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)

      if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response

   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response


def rate_product(request, id):
    product = get_object_or_404(Product, pk=id)

    if request.method == "POST":
        try:
            new_rating = float(request.POST.get("rating"))
            product.add_rating(new_rating)
        except ValueError as e:
            return render(request, "rate_product.html", {"product": product, "error": str(e)})

        return redirect("main:show_product", id=product.id)

    return render(request, "rate_product.html", {"product": product})


def add_stock(request, id):
    product = get_object_or_404(Product, pk=id)

    if request.method == "POST":
        try:
            amount = int(request.POST.get("amount"))
            product.add_stock(amount)
        except ValueError as e:
            return render(request, "add_stock.html", {"product": product, "error": str(e)})

        return redirect("main:show_product", id=product.id)

    return render(request, "add_stock.html", {"product": product})


def reduce_stock(request, id):
    product = get_object_or_404(Product, pk=id)

    if request.method == "POST":
        try:
            amount = int(request.POST.get("amount"))
            product.reduce_stock(amount)
        except ValueError as e:
            return render(request, "reduce_stock.html", {"product": product, "error": str(e)})

        return redirect("main:show_product", id=product.id)

    return render(request, "reduce_stock.html", {"product": product})

def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:show_main')

    context = {
        'form': form
    }

    return render(request, "edit_product.html", context)

def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    product.delete()
    return HttpResponseRedirect(reverse('main:show_main'))

def proxy_image(request):
    image_url = request.GET.get('url')
    if not image_url:
        return HttpResponse('No URL provided', status=400)
    
    try:
        # Fetch image from external source
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        
        # Return the image with proper content type
        return HttpResponse(
            response.content,
            content_type=response.headers.get('Content-Type', 'image/jpeg')
        )
    except requests.RequestException as e:
        return HttpResponse(f'Error fetching image: {str(e)}', status=500)
    
@csrf_exempt
def create_product_flutter(request):
    if request.method != 'POST':
        return JsonResponse({"status": "invalid method"}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        return JsonResponse({"status": "invalid json"}, status=400)

    # Pastikan user ter-autentikasi
    if not request.user.is_authenticated:
        return JsonResponse({"status": "unauthorized"}, status=401)

    # Ambil fields dengan fallback default
    name = strip_tags(data.get("name", "")).strip()
    price = data.get("price", None)
    stock = data.get("stock", 0)
    description = strip_tags(data.get("description", "")).strip()
    thumbnail = data.get("thumbnail", "") or None
    category = data.get("category", "Jersey")
    is_featured = bool(data.get("is_featured", False))

    # Validasi minimal
    if not name or price is None:
        return JsonResponse({"status": "error", "message": "name and price required"}, status=400)

    # Konversi price (jika string)
    try:
        price = int(price)
    except Exception:
        return JsonResponse({"status": "error", "message": "price must be integer"}, status=400)

    # Pastikan category cocok dengan choices (opsional)
    if category not in dict(Product.CATEGORY_CHOICES).keys():
        # Map common values (case-insensitive)
        mapped = None
        for k in dict(Product.CATEGORY_CHOICES).keys():
            if k.lower() == category.lower():
                mapped = k
                break
        if mapped:
            category = mapped
        else:
            category = Product.CATEGORY_CHOICES[0][0]  # default first

    product = Product.objects.create(
        name = name,
        price = price,
        stock = stock,
        description = description,
        thumbnail = thumbnail,
        category = category,
        is_featured = is_featured,
        rating = 0.0,
        total_ratings = 0,
        user = request.user
    )

    return JsonResponse({"status": "success", "id": str(product.id)}, status=200)