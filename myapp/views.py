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
        Item.objects.create(item_code=item_code, item_name=item_name, stock_qty=stock_qty)
        return HttpResponse("Form submitted successfully!")

    all_items = Item.objects.all()

    # Generate QR codes for each item
    items_with_qr = []
    for item in all_items:
        for i in range(item.stock_qty):
            # print("i:",i)
            # items_with_qr.append({"sl_no",i+1})
            qr_data = f"Code: {item.item_code}, Name: {item.item_name}, Qty: {item.stock_qty} Sl.No: {i+1}"
            qr_img = qrcode.make(qr_data)

            buffer = BytesIO()
            qr_img.save(buffer, format="PNG")
            qr_base64 = base64.b64encode(buffer.getvalue()).decode()

            print("item:", item.item_code, item.item_name)
            items_with_qr.append({
                "item": item,
                "sl_no": i + 1,
                "qr_code": qr_base64
            })

    return render(request, "myapp/index.html", {"items_with_qr": items_with_qr})
