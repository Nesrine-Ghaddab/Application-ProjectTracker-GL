from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from Gestion_Projects.models import Project
from Notes.models import Note
from Taches.models import Taches
from Reunion.models import Reunion
import requests
import json

@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message', '').lower()
            if not message:
                return JsonResponse({'error': 'No message provided'})

            user = request.user if request.user.is_authenticated else None
            if not user:
                return JsonResponse({'response': 'Please log in to access your work data.'})

            # Simple keyword-based responses
            if 'project' in message or 'projects' in message:
                projects = Project.objects.filter(user=user)
                if projects.exists():
                    response = "Here are your projects:\n" + "\n".join([f"- {p.title}: {p.description}" for p in projects])
                else:
                    response = "You have no projects yet."
            elif 'note' in message or 'notes' in message:
                notes = Note.objects.filter(user=user)
                if notes.exists():
                    response = "Here are your notes:\n" + "\n".join([f"- {n.title}: {n.content[:100]}..." for n in notes])
                else:
                    response = "You have no notes yet."
            elif 'task' in message or 'tasks' in message or 'tache' in message:
                tasks = Taches.objects.filter(projet__user=user)
                if tasks.exists():
                    response = "Here are your tasks:\n" + "\n".join([f"- {t.nom}: {t.description}" for t in tasks])
                else:
                    response = "You have no tasks yet."
            elif 'meeting' in message or 'meetings' in message or 'reunion' in message:
                meetings = Reunion.objects.filter(organizer=user)
                if meetings.exists():
                    response = "Here are your meetings:\n" + "\n".join([f"- {m.title}: {m.date}" for m in meetings])
                else:
                    response = "You have no meetings scheduled."
            else:
                # Fallback to local AI (Ollama)
                try:
                    ollama_response = requests.post('http://localhost:11434/api/generate', json={
                        "model": "mistral:latest",
                        "prompt": data.get('message', ''),
                        "stream": False
                    }, timeout=30)
                    if ollama_response.status_code == 200:
                        result = ollama_response.json()
                        response = result.get('response', 'Sorry, I couldn\'t generate a response.')
                    else:
                        response = "I'm your Work Assistant for PersonalTracker. For general questions, please ensure Ollama is running with 'ollama serve'."
                except requests.exceptions.RequestException:
                    response = "I'm your Work Assistant for PersonalTracker. I can help with your projects, notes, tasks, and meetings. For general AI answers, ensure Ollama is running locally."

            return JsonResponse({'response': response})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    return JsonResponse({'error': 'Invalid request method'})