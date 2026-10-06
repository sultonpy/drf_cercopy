import hmac

from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from apps.bookings.models import Booking
from .models import Payment
from . import octo

class OctoNotifyView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        n = request.data

        octo_uuid = str(n.get("octo_payment_UUID", ""))
        tx = str(n.get("shop_transaction_id", ""))



        with transaction.atomic():
            try:
                p = (Payment.objects.select_for_update(of=("self",))
                     .select_related("booking").get(octo_uuid=octo_uuid, booking_id=tx))
            except (Payment.DoesNotExist, DjangoValidationError, ValueError):
                return Response({"detail": "not found"}, status=404)
            unique_key = str(settings.OCTO_UNIQUE_KEY or "").strip()

            if unique_key:
                signature = str(n.get("signature", ""))


                if not octo.verify_callback_signature(
                        unique_key,
                        octo_uuid,
                        str(n.get("status", "")),
                        signature,
                ):
                    return Response(
                        {"detail": "bad signature"},
                        status=400,
                    )

                hash_key = str(n.get("hash_key", ""))


                if not octo.verify_callback_hash_key(
                        unique_key,
                        octo_uuid,
                        str(n.get("status", "")),
                        hash_key,
                ):
                    return Response(
                        {"detail": "bad hash_key"},
                        status=400,
                    )
            try:
                octo_data = octo.verify_payment_status(tx)
            except Exception:
                return Response(
                    {"detail": "OCTO statusini tekshirib bolmadi"},
                    status=502,
                )

            if str(octo_data.get("octo_payment_UUID", "")) != octo_uuid:
                return Response(
                    {"detail": "payment UUID mismatch"},
                    status=400,
                )

            verified_status = octo_data.get("status")

            if p.status != Payment.Status.CREATED:
                return Response({"ok": True})

            total_sum = n.get("total_sum")

            if total_sum is not None:
                try:
                    paid_sum = int(total_sum)
                except (TypeError, ValueError):
                    return Response({"detail": "invalid sum"}, status=400)

                if paid_sum != p.amount:
                    return Response({"detail": "sum mismatch"}, status=400)

            ok = verified_status == "succeeded"
            p.status = Payment.Status.SUCCEEDED if ok else Payment.Status.CANCELED
            p.raw_notify = dict(n)
            p.save(update_fields=["status", "raw_notify"])
            p.booking.status = Booking.Status.PAID if ok else Booking.Status.CANCELLED
            p.booking.save(update_fields=["status"])
        return Response({"ok": True})