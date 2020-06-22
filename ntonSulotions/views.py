from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from solutions.models import Question
from accounts.models import User
from clients.models import Client
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.db.models import Count,Q,Avg,Sum,F,FloatField
from django.db.models.functions import Cast



active = {}
active['dashboard']='active'
from djqscsv import render_to_csv_response,  write_csv
def csv_view(request):
    qs = Client.objects.all()
    with open('client.csv', 'wb') as csv_file:
      write_csv(qs, csv_file)
    #render_to_csv_response(qs)
    qs = User.objects.all()
    with open('user.csv', 'wb') as csv_file:
        write_csv(qs, csv_file)
    #render_to_csv_response(qs)
    qs = Question.objects.all()
    with open('question.csv', 'wb') as csv_file:
        write_csv(qs, csv_file)




    return render_to_csv_response(qs)

class HomePage(LoginRequiredMixin, TemplateView):
    template_name = "index.html"

    def get_context_data(self,**kwargs):

        context=super().get_context_data(**kwargs)
        if self.request.user.is_staff:
            questionlist =  Question.objects.values('status').filter(charged_by=self.request.user)
        else:
            questionlist =  Question.objects.values('status').filter(user=self.request.user)

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

        context['activePage']= 'dashboard'
        #context['pagecounter']=self.pagecounter

        usersStatics  = User.objects\
            .values('username','email')\
            .filter(is_staff=True)\
            .annotate(total=Count(F('charged_tickets'),output_field=FloatField()),
                resolved=Count('charged_tickets__status', filter=Q(charged_tickets__status='RS')),
                avg = Cast('resolved', FloatField()) / Cast('total', FloatField())    * 100,
                avgTime = Avg('charged_tickets__time_to_resolv', filter=Q(charged_tickets__status='RS')),# / Count('charged_tickets__status', filter=Q(charged_tickets__status='RS')),
                #avgTime = Sum(F('charged_tickets__time_to_resolv')) / Count('charged_tickets__status', filter=Q(charged_tickets__status='RS')),
                )
        #print(usersStatics)
        context['usersStatics']= usersStatics


        return context



def handler400(request, exception, template_name="400.html"):
    response = render_to_response(template_name)
    response.status_code = 400
    return response
def handler403(request, exception, template_name="403.html"):
    response = render_to_response(template_name)
    response.status_code = 403
    return response
def handler404(request, exception, template_name="404.html"):
    response = render_to_response(template_name)
    response.status_code = 404
    return response
def handler500(request, *args, **argv):
    response = render_to_response('500.html', {},)
    response.status_code = 500
    return response
