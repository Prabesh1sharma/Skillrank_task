from django.shortcuts import render
from django.http import HttpResponse
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO
import os

def home(request):
    return render(request, "home_new.html")

from django.shortcuts import render
from django.http import HttpResponse
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO
import base64


def split_pdf(request):
    context = {}
    
    # Handle PDF upload
    if request.method == "POST" and request.POST.get("action") == "upload":
        if "pdf_file" not in request.FILES:
            context["error"] = "No file uploaded"
            return render(request, "split_pdf.html", context)
            
        uploaded_file = request.FILES["pdf_file"]
        
        # Validate file type
        if not uploaded_file.name.endswith('.pdf'):
            context["error"] = "Please upload a PDF file"
            return render(request, "split_pdf.html", context)
            
        try:
            # Read PDF and store in session
            pdf_bytes = uploaded_file.read()
            pdf = PdfReader(BytesIO(pdf_bytes))
            num_pages = len(pdf.pages)
            
            request.session["pdf_file"] = base64.b64encode(pdf_bytes).decode("utf-8")
            request.session["num_pages"] = num_pages
            
            context["num_pages"] = num_pages
            context["pages"] = list(range(1, num_pages + 1))
            
        except Exception as e:
            context["error"] = f"Error processing PDF: {str(e)}"
            
    # Handle PDF splitting
    elif request.method == "POST" and request.POST.get("action") == "split":
        if "pdf_file" not in request.session:
            context["error"] = "No PDF found. Please upload again."
            return render(request, "split_pdf.html", context)
            
        selected_pages = request.POST.getlist("selected_pages")
        
        try:
            selected_pages = [int(p) for p in selected_pages]
        except ValueError:
            context["error"] = "Invalid page selection"
            return render(request, "split_pdf.html", context)
            
        try:
            # Get PDF from session and create new PDF with selected pages
            pdf_bytes = base64.b64decode(request.session["pdf_file"])
            pdf = PdfReader(BytesIO(pdf_bytes))
            writer = PdfWriter()
            
            for page_num in selected_pages:  # Keep the order as selected by user
                if 1 <= page_num <= len(pdf.pages):
                    writer.add_page(pdf.pages[page_num - 1])
                    
            # Create response with new PDF
            output = BytesIO()
            writer.write(output)
            output.seek(0)
            
            response = HttpResponse(output.getvalue(), content_type="application/pdf")
            response["Content-Disposition"] = f"attachment; filename=split_pages.pdf"
            return response
            
        except Exception as e:
            context["error"] = f"Error splitting PDF: {str(e)}"
            
    return render(request, "split_pdf.html", context)


def merge_pdfs(request):
    if request.method == "POST" and request.FILES.getlist("pdf_files"):
        uploaded_files = request.FILES.getlist("pdf_files")
        writer = PdfWriter()
        
        for file in uploaded_files:
            pdf = PdfReader(file)
            for page in pdf.pages:
                writer.add_page(page)
        
        output = BytesIO()
        writer.write(output)
        output.seek(0)
        
        response = HttpResponse(output.read(), content_type="application/pdf")
        response["Content-Disposition"] = "attachment; filename=merged.pdf"
        return response
    
    return render(request, "merge_pdf.html")
