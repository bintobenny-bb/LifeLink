import json

from django.http import JsonResponse
from django.views.decorators.http import require_POST

from ai_assistant.services.gemini_service import generate_response


@require_POST
def chat_api(request):
    try:
        data = json.loads(request.body)
        message = data.get("message", "").strip()

        if not message:
            return JsonResponse(
                {"error": "Message cannot be empty."},
                status=400
            )

        if len(message) > 2000:
            return JsonResponse(
                {"error": "Message is too long. Maximum 2000 characters."},
                status=400
            )

        ai_response = generate_response(message)

        return JsonResponse({
            "success": True,
            "message": message,
            "response": ai_response
        })

    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON request."},
            status=400
        )

    except Exception as e:
        print(f"Chat API Error: {e}")

        return JsonResponse(
            {"error": "Something went wrong. Please try again later."},
            status=500
        )
