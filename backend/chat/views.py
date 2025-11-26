from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from openai import OpenAI
from college.models import College


def get_college_db_summary(limit=20):
    """
    Summarize top `limit` colleges in DB as optional context for LLM.
    """
    colleges = College.objects.order_by("world_rank")[:limit]
    if not colleges.exists():
        return "College database is empty."

    summary = "Optional College Database (Top Records):\n"
    for c in colleges:
        summary += (
            f"Institution: {c.institution}, Country: {c.country}, "
            f"World Rank: {c.world_rank}, Score: {c.score}, Year: {c.year}\n"
        )
    return summary


class GeminiChatAPIView(APIView):
    """
    Hybrid LLM API: LLM answers directly or uses DB if needed.
    """
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]

    def post(self, request):
        user_message = request.data.get("message")
        if not user_message:
            return JsonResponse({"error": "Message is required"}, status=400)

        try:
            db_context = get_college_db_summary()  # optional context

            client = OpenAI(
                api_key="AIzaSyDpSFG82N4aVOlUq7bMorCeJ1Nb5fq9pZI",
                base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
            )

            response = client.chat.completions.create(
                model="gemini-2.5-flash",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a helpful assistant. You have access to the following optional "
                            f"college database context. Use it only if needed to answer queries.\n{db_context}"
                        )
                    },
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,
            )

            ai_message = response.choices[0].message.content

            return JsonResponse({"reply": ai_message})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
