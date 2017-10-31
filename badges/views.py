from django.shortcuts import render

from .forms import ButtonForm
from .badges import render_to_tag


PALLATES = {
    'nyc': ['#0039A6', '#FF6319', '#6CBE45', '#996633', '#A7A9AC', '#FCCC0A',
            '#808183', '#EE352E', '#00933C', '#B933AD'],
    'lirr': ['#00985F', '#4D5357', '#6E3219', '#CE8E00', '#FF6319', '#006983',
             '#00AF3F', '#0039A6', '#C60C30' '#A626AA', '#00A1DE']
}


def home(request):
    img = None
    if 'text' in request.GET:
        form = ButtonForm(request.GET)
        if form.is_valid():
            img = render_to_tag(form.cleaned_data['text'], theme=form.cleaned_data['theme'])
    else:
        form = ButtonForm()
    return render(request, "home.html", dict(form=form, img=img))
