# Reunion/api_views.py
from django.http import JsonResponse, HttpResponseNotAllowed, Http404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

from .models import Reunion, ReminderLog


def _reunion_to_dict(reunion):
    return {
        "id": reunion.id,
        "title": reunion.title,
        "date": reunion.date.isoformat(),
        "start_time": reunion.start_time.isoformat(),
        "end_time": reunion.end_time.isoformat(),
        "reunion_type": reunion.reunion_type,
        "subject": reunion.subject,
        "description": reunion.description,
        "reminder_enabled": reunion.reminder_enabled,
        "reminder_timing": reunion.reminder_timing,
        "reminder_sent": reunion.reminder_sent,
        "reminder_sent_at": reunion.reminder_sent_at.isoformat() if reunion.reminder_sent_at else None,
    }


class ReunionListAPI(View):
    def get(self, request):
        qs = Reunion.objects.all().order_by("-date", "-start_time")
        data = [_reunion_to_dict(r) for r in qs]
        return JsonResponse({"results": data}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class ReunionDetailAPI(View):
    def get_object(self, pk):
        try:
            return Reunion.objects.get(pk=pk)
        except Reunion.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        reunion = self.get_object(pk)
        return JsonResponse(_reunion_to_dict(reunion), status=200)

    def post(self, request, pk=None):
        # create
        try:
            payload = json.loads(request.body.decode("utf-8"))
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        required = ("title", "date", "start_time", "end_time")
        if not all(k in payload for k in required):
            return JsonResponse({"error": f"Missing field; required: {required}"}, status=400)

        r = Reunion.objects.create(
            title=payload.get("title"),
            date=payload.get("date"),
            start_time=payload.get("start_time"),
            end_time=payload.get("end_time"),
            reunion_type=payload.get("reunion_type", "other"),
            subject=payload.get("subject", "other"),
            description=payload.get("description", ""),
            reminder_enabled=payload.get("reminder_enabled", True),
            reminder_timing=payload.get("reminder_timing", 30),
        )
        return JsonResponse(_reunion_to_dict(r), status=201)

    def put(self, request, pk):
        reunion = self.get_object(pk)
        try:
            payload = json.loads(request.body.decode("utf-8"))
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        for field in ("title", "date", "start_time", "end_time", "description", "reunion_type", "subject", "reminder_enabled", "reminder_timing"):
            if field in payload:
                setattr(reunion, field, payload[field])
        reunion.save()
        return JsonResponse(_reunion_to_dict(reunion), status=200)

    def delete(self, request, pk):
        reunion = self.get_object(pk)
        reunion.delete()
        return JsonResponse({"deleted": True}, status=204)


class ReminderLogListAPI(View):
    def get(self, request):
        qs = ReminderLog.objects.all().order_by("-sent_at")[:100]
        data = []
        for log in qs:
            data.append({
                "id": log.id,
                "reunion_id": log.reunion_id,
                "sent_at": log.sent_at.isoformat(),
                "reminder_type": log.reminder_type,
                "sent_via": log.sent_via,
                "status": log.status,
                "notes": log.notes,
            })
        return JsonResponse({"results": data}, status=200)
