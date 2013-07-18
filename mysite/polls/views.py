from polls.models import Poll, Choice
from django.http import HttpResponse, Http404, HttpResponseRedirect
#from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

#def index(request):
#	latest_poll_list = Poll.objects.order_by('-pub_date')[:5]
#	#template = loader.get_template('polls/index.html')
#	#context = RequestContext(request, {
#	#		'latest_poll_list':latest_poll_list,
#	#})
#	context = {'latest_poll_list': latest_poll_list}
#	return render(request, 'polls/index.html', context)
#	#return HttpResponse(template.render(context))

class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_poll_list'

	def get_queryset(self):
		return Poll.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


#def detail(request, poll_id):
#	#try:
#	#	poll = Poll.objects.get(pk=poll_id)
#	#except Poll.DoesNotExist:
#	#	raise Http404
#	poll = get_object_or_404(Poll, pk=poll_id)
#	return render(request, 'polls/detail.html', {'poll':poll})

class DetailView(generic.DetailView):
	model = Poll
	template_name = 'polls/detail.html'
	
	def get_queryset(self):
		return Poll.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
	model = Poll
	template_name = 'polls/results.html'

#def results(request, poll_id):
	#poll = get_object_or_404(Poll, pk=poll_id)
	#return render(request,'polls/results.html',{'poll':poll})
#	return ResultsView.as_view()

def vote(request, poll_id):
	p = get_object_or_404(Poll, pk=poll_id)
	try:
		select_choice = p.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render(request,'polls/detail.html', {
			'poll': p,
			'error_message':"No has seleccionado ninguna Mr."
		})
	else:
		select_choice.votes += 1
		select_choice.save()
	return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))
