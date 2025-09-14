from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from main.forms import ProductForm
from main.models import Product
from django.http import JsonResponse

def show_main(request):
    product_list = Product.objects.all()

    context = {
        "product_list": product_list,
    }

    return render(request, "main/main.html", context)

def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:show_main')
    else:
        form = ProductForm()

    context = {'form': form}
    return render(request, "main/add_product.html", context)

def get_products_json(request):
    product_list = Product.objects.all().values(
        'id', 'name', 'price', 'stock', 'description', 'thumbnail', 'category', 'is_featured', 'rating'
    )
    return JsonResponse(list(product_list), safe=False)


def show_product(request, id):
    product = get_object_or_404(Product, pk=id)

    context = {
        'product': product
    }

    return render(request, "main/product_detail.html", context)

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
