from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

# Create your views here.
from .models import Question, Choice

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

# Get Questions and display then
def index(request):
    template = get_template(request)
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    print(latest_question_list)
    context = {'title': 'Poll Questions', 'latest_question_list': latest_question_list, 'template': template }
    return render(request, f'{template}/polls/index.html', context)

# Show specific question and choices
def detail(request, question_id):
    try:
        template = get_template(request)
        # template = request.GET.get('use') if request.GET.get('use') == 'bulma' else 'bootstrap'
        question = Question.objects.get(pk=question_id)
        context = { 'title': 'Question Detail', 'question': question, 'template': template }
    except Question.DoesNotExistList:
        raise Http404("Question does not exists")

    return render(request, f'{template}/polls/detail.html', context)

# Get question and display results

def results(request, question_id):
    try:
        template = get_template(request)
        # template = request.GET.get('use') if request.GET.get('use') == 'bulma' else 'bootstrap'
        question = get_object_or_404(Question, pk=question_id)
        context = { 'title': 'Question Results', 'question': question, 'template': template }
    except Question.DoesNotExistList:
        raise Http404("Question does not exists")

    return render(request, f'{template}/polls/results.html', context)


def vote(request, question_id):
    # print(request.POST['choice'])
    question = get_object_or_404(Question, pk=question_id)
    try:
        template = get_template(request)
        # template = request.GET.get('use') if request.GET.get('use') == 'bulma' else 'bootstrap'
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, f'{template}/polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
