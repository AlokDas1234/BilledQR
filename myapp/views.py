from http.client import responses

import qrcode
import base64
from io import BytesIO
from django.shortcuts import render
from django.http import HttpResponse
from .models import Item


def index(request):
    if request.method == "POST":
        item_code = request.POST.get("item_code")
        item_name = request.POST.get("item_name")
        stock_qty = request.POST.get("stock_qty")

        Item.objects.create(item_code=item_code, item_name=item_name, stock_qty=stock_qty,valid_qr=True)
        return HttpResponse("Form submitted successfully!")

    all_items = Item.objects.all()

    # Generate QR codes for each item
    items_with_qr = []
    for item in all_items:
        for i in range(item.stock_qty):
            # print("i:",i)
            # items_with_qr.append({"sl_no",i+1})
            qr_data = f"Code: {item.item_code}, Name: {item.item_name}, Validity: {item.valid_qr} Sl.No: {i+1}"
            qr_img = qrcode.make(qr_data)

            buffer = BytesIO()
            qr_img.save(buffer, format="PNG")
            qr_base64 = base64.b64encode(buffer.getvalue()).decode()

            # print("item:", item.item_code, item.item_name)
            items_with_qr.append({
                "item": item,
                "sl_no": i + 1,
                "qr_code": qr_base64

            })

    return render(request, "myapp/index.html", {"items_with_qr": items_with_qr})

# views.py
from django.http import JsonResponse
import json

def process_scan(request):
    if request.method == "POST":
        data = json.loads(request.body)
        scanned_value = data.get("scanned_data")
        # print(f"Scanned QR value: {scanned_value}")

        # You can use scanned_value to look up your Item model
        # Example: item = Item.objects.filter(item_code=scanned_value).first()

        return JsonResponse({"status": "success", "received": scanned_value})
    return JsonResponse({"status": "error"}, status=400)

def process_final_scan(request):
    if request.method == "POST":
        scanned_value = request.POST.get("scanned_data")
        contract_no = request.POST.get("contract_no")
        party_name = request.POST.get("party_name")
        gear_box = request.POST.get("gear_box")
        actuator = request.POST.get("actuator")
        valve = request.POST.get("valve")

        # print(f"Scanned QR: {scanned_value}")
        # print(f"Contract No: {contract_no}")
        # print(f"Party Name: {party_name}")
        # print(f"Party Name: {party_name}")

        # Process/save data here
        return render(request, "myapp/index.html", {"scanned_value": scanned_value, "contract_no": contract_no, "party_name": party_name,"gear_box": gear_box, "actuator": actuator, "valve": valve})

    return HttpResponse("Invalid request", status=400)
