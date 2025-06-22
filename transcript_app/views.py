# transcript_app/views.py
from django.shortcuts import render, get_object_or_404
from .models import Student, Participation, AttributeStrengthMap
from collections import defaultdict
from datetime import date
from django.http import HttpResponse
from django.template.loader import get_template
import weasyprint
from django.shortcuts import render

def home(request):
        return render(request, 'transcript_app/home.html')

def transcript_view(request):
    roll_no = request.GET.get('roll_no')
    student = get_object_or_404(Student, roll_no=roll_no)
    participations = Participation.objects.filter(student=student)

    all_attributes = set()
    for part in participations:
        all_attributes.update(part.event.attributes.all())

    strength_scores = defaultdict(list)
    for attr in all_attributes:
        mappings = AttributeStrengthMap.objects.filter(attribute=attr)
        for map in mappings:
            strength_scores[map.strength.name].append(map.value)  # ✅


    strength_data = []
    for strength, values in strength_scores.items():
        avg = round(sum(values) / len(values), 2)
        if avg >= 2.5:
            category = "ESTD"
        elif avg >= 1.5:
            category = "DEV"
        else:
            category = "EMER"
        strength_data.append({
            'name': strength,
            'average': avg,
            'category': category
        })

    strength_data.sort(key=lambda x: x['name'])

    return render(request, 'transcript_app/transcript.html', {
        'student': student,
        'strength_data': strength_data,
        'today': date.today()
    })


def transcript_pdf(request, roll_no):
    student = get_object_or_404(Student, roll_no=roll_no)
    participations = Participation.objects.filter(student=student)

    all_attributes = set()
    for part in participations:
        all_attributes.update(part.event.attributes.all())

    strength_scores = defaultdict(list)
    for attr in all_attributes:
        mappings = AttributeStrengthMap.objects.filter(attribute=attr)
        for map in mappings:
            strength_scores[map.strength.name].append(map.weight)

    strength_data = []
    for strength, values in strength_scores.items():
        avg = round(sum(values) / len(values), 2)
        if avg >= 2.5:
            category = "ESTD"
        elif avg >= 1.5:
            category = "DEV"
        else:
            category = "EMER"
        strength_data.append({
            'name': strength,
            'average': avg,
            'category': category
        })

    strength_data.sort(key=lambda x: x['name'])

    template = get_template('transcript_app/transcript.html')
    html = template.render({
        'student': student,
        'strength_data': strength_data,
        'today': date.today()
    })

    pdf_file = weasyprint.HTML(string=html).write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'filename="transcript_{student.roll_no}.pdf"'
    return response



    