from django.shortcuts import render
from django.http import JsonResponse
import os
import shutil
from .utils import process_pdf, get_answer  # Import helper functions
from django.views.decorators.csrf import csrf_exempt

# Serve chat UI
def chat_view(request):
    return render(request, "qaback/chat.html") 


# Handle PDF Upload
@csrf_exempt
def upload_pdf(request):
    if request.method == "POST":
        # Clear session and previous messages
        request.session.flush()

        pdf_file = request.FILES.get("pdf")
        if not pdf_file:
            return JsonResponse({"message": "No file uploaded"}, status=400)

        # Ensure media directory exists
        media_dir = "media"
        os.makedirs(media_dir, exist_ok=True)

        # Clear old PDFs
        for file in os.listdir(media_dir):
            file_path = os.path.join(media_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

        # Save new file
        save_path = os.path.join(media_dir, pdf_file.name)
        with open(save_path, "wb") as f:
            for chunk in pdf_file.chunks():
                f.write(chunk)

        # Process PDF
        process_pdf(save_path)

        return JsonResponse({"message": "PDF uploaded and processed successfully! Chat history cleared.", "clear_chat": True})

    return JsonResponse({"message": "Invalid request"}, status=400)


# Handle Questions
@csrf_exempt
def ask_question(request):
    if request.method == "POST":
        question = request.POST.get("question")
        if not question:
            return JsonResponse({"answer": "Please provide a question."})

        answer = get_answer(question)
        return JsonResponse({"answer": answer})

    return JsonResponse({"answer": "Invalid request"}, status=400)

