"""Soxta Octo (faqat PAYMENT_MODE=mock): prepare_payment -> to'lov sahifasi -> webhook -> return_url."""
import logging
import uuid as uuidlib

import requests
from django.conf import settings
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from .models import MockOctoTransaction
from .octo import make_signature

log = logging.getLogger(__name__)


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def prepare_payment(request):
    b = request.data
    if b.get("octo_secret") != settings.OCTO_SECRET:
        return Response({"error": 1, "errMessage": "Invalid secret"})
    u = str(uuidlib.uuid4())
    MockOctoTransaction.objects.create(
        uuid=u, shop_transaction_id=b["shop_transaction_id"], total_sum=b["total_sum"],
        notify_url=b["notify_url"], return_url=b["return_url"],
    )
    return Response({"error": 0, "data": {
        "shop_transaction_id": b["shop_transaction_id"],
        "octo_payment_UUID": u,
        "status": "created",
        "octo_pay_url": f"{settings.PUBLIC_URL}/mock-octo/pay/{u}/",
        "total_sum": b["total_sum"],
    }})


PAGE = """<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>OCTO (test)</title>
<body style="font-family:system-ui;max-width:380px;margin:40px auto;padding:0 16px">
<h2>OCTO <small style="color:#888">test rejim</small></h2>
<p>Summa: <b>{total} so'm</b></p>
<form method="post">
  <input style="width:100%;padding:8px;margin:4px 0" value="8600 1234 5678 9012">
  <input style="width:100%;padding:8px;margin:4px 0" value="12/28">
  <button name="result" value="succeeded" style="width:100%;padding:10px;margin:8px 0;background:#16a34a;color:#fff;border:0">To'lash</button>
  <button name="result" value="canceled" style="width:100%;padding:10px;background:#ddd;border:0">Bekor qilish</button>
</form></body>"""


@csrf_exempt
def pay_page(request, uuid):
    try:
        t = MockOctoTransaction.objects.get(uuid=uuid)
    except MockOctoTransaction.DoesNotExist:
        raise Http404
    if request.method == "POST":
        result = "succeeded" if request.POST.get("result") == "succeeded" else "canceled"
        try:  # server -> server webhook, xuddi haqiqiy Octo kabi
            requests.post(t.notify_url, json={
                "octo_payment_UUID": t.uuid, "shop_transaction_id": t.shop_transaction_id,
                "status": result, "total_sum": t.total_sum,
                "signature": make_signature(t.uuid, t.shop_transaction_id),
            }, timeout=10)
        except requests.RequestException:
            log.exception("Mock Octo webhook yuborilmadi")
        return HttpResponseRedirect(t.return_url)  # brauzer -> return_url
    return HttpResponse(PAGE.format(total=f"{t.total_sum:,}".replace(",", " ")))