from django.shortcuts import render

# Identify which css framework to use
def get_template(request):
    if request.GET.get('use') in ['bulma', 'bootstrap']:
        request.session['template'] = request.GET.get('use')
        return request.GET.get('use')
    elif 'template' in request.session:
        return request.session['template']
    else:
        request.session['template'] = 'bootstrap'
        return 'bootstrap'

# Create your views here.
def index(request):
    template = get_template(request)
    return render(request, f'{template}/pages/index.html')