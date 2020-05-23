from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from solutions.models import Question




class HomePage(LoginRequiredMixin, TemplateView):
    template_name = "index.html"

    def get_context_data(self,**kwargs):

        context=super().get_context_data(**kwargs)
        questionlist =  Question.objects.filter(user=self.request.user)

        tickets_open = questionlist.filter(status = 'OV').count()
        tickets_resolved = questionlist.filter(status = 'RS').count()
        tickets_waiting = questionlist.filter(status = 'EA').count()
        tickets_closed = questionlist.filter(status = 'FR').count()
        tickets_canceled = questionlist.filter(status = 'AN').count()

        context['tickets_open']=tickets_open
        context['tickets_resolved']=tickets_resolved
        context['tickets_waiting']=tickets_waiting
        context['tickets_closed']=tickets_closed
        context['tickets_canceled']=tickets_canceled


        #context['pagecounter']=self.pagecounter


        return context

    # def get(self, request, *args, **kwargs):
    #     if request.user.is_authenticated:
    #         return HttpResponseRedirect(reverse("test"))
    #     return super().get(request, *args, **kwargs)
