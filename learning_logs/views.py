from django.shortcuts import render, redirect, get_object_or_404
from learning_logs.models import Topic, Entry
from django.contrib.auth.decorators import login_required
from .forms import TopicForm, EntryForm
from django.http import Http404


def check_topic_owner(topic, request):
    if topic.owner != request.user:
        raise Http404


def index(request):

    """  A página inicial de Learning log, sem usuário estar logado"""

    return render(request, 'learning_logs/index.html')


@login_required
def comunidade(request):
    topics = Topic.objects.order_by('date_added')  # somente para fazer funcionar até sexta

    context = {'topics': topics}
    return render(request, 'learning_logs/comunidade.html', context)


@login_required
def topics(request):
    """ Mostra todos os assuntos """
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


@login_required
def topic(request, topic_id):
    """ Mostra um único assunto e todas as suas entradas. """
    topic = get_object_or_404(Topic, id=topic_id)

    check_topic_owner(topic, request) # confere se o usário da requisição é o dono do tópico

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
    """ Adiciona um novo tópico."""
    if request.method != 'POST':
        # nenhum dado submetido, cria um formulário em branco
        form = TopicForm()
    else:
        # dados de um POST submetido, procesa os dados
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()

            return redirect('learning_logs:topics')

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """ Acrescenta uma nova entrada para um assunto em particular. """
    topic = Topic.objects.get(id=topic_id)

    check_topic_owner(topic, request)

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = EntryForm()
    else:
        # POST data submitted; process data.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)
    # Display a blank or invalid form.
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """ Edita uma entrada existente """
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    check_topic_owner(topic, request)

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)


@login_required
def registros_topico(request, topic_id):

    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/registros_topicos.html', context)

