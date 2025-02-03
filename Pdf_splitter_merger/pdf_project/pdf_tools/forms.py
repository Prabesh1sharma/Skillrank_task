from django import forms

class SplitPdfForm(forms.Form):
    pdf_file = forms.FileField(label='Select PDF file')

class MergePdfsForm(forms.Form):
    pdf_files = forms.FileField(
        label='Select PDF files',
        widget=forms.ClearableFileInput(attrs={'multiple': True})
    )