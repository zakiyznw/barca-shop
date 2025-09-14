from django.urls import path
from main.views import show_json_by_id, show_main, show_product, show_xml, show_json, show_xml_by_id, show_json_by_id, add_product, rate_product, add_stock, reduce_stock

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("product/<uuid:id>/", show_product, name="show_product"),
    path("product/<uuid:id>/rate/", rate_product, name="rate_product"),
    path("product/<uuid:id>/add_stock/", add_stock, name="add_stock"),
    path("product/<uuid:id>/reduce_stock/", reduce_stock, name="reduce_stock"),
    path("products/xml/", show_xml, name="show_xml"),
    path("products/json/", show_json, name="show_json"),
    path("products/xml/<str:product_id>/", show_xml_by_id, name="show_xml_by_id_products"),
    path("products/json/<str:product_id>/", show_json_by_id, name="show_json_by_id_products"),
    path("add_product/", add_product, name="add_product"),
]
