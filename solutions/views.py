from django.db.models import Count,Q,Avg,Sum,F
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import(LoginRequiredMixin, PermissionRequiredMixin  )
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import BadHeaderError, send_mail, EmailMultiAlternatives
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views import generic
from django.template.loader import get_template, render_to_string
from django.template import Context
import json
import datetime, pytz
from datetime import timedelta

## models
from accounts.models import User,Notification
from clients.models import Client
from .models import Question,Reponce, Categorie, SousCategorie
from .forms import ReponceForm, QuestionForm


####################################################
# QUESTION: CRUD

def add_notification_to_cosultant(description, url):
    consultants = User.objects.filter(is_staff = True)
    for consultant in consultants:
        notification = Notification.objects.create(user=consultant, description = description, url=url)
        notification.save
class QuestionCreate(LoginRequiredMixin, generic.CreateView):
    model = Question
    form_class = QuestionForm
    def form_valid(self, form):
        try:
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            #
            self.object.save()
        except IntegrityError:
            messages.warning(self.request,_("Warning, Something went wrong, please try again"))
        else:
            messages.success(self.request,_("Question has been saved."))

            ########################
            #  USER EMAIl
            plaintext = get_template('email/email.txt')
            htmly     = get_template('email/email.html')
            subject = self.object.titre
            d = {}
            d['ref'] = self.object.get_ref
            d['user'] = self.object.titre
            d['user'] = self.object.user.username
            d['client'] = self.object.user.client.name

            d['ticket_url'] = "http://{0}{1}".format(self.request.META['HTTP_HOST'],
                                reverse("solutions:questiondetail", kwargs={"pk": self.object.pk}))


            user_email = self.object.user.email
            dsi_email = self.object.user.client.email
            # text_content = plaintext.render(d)
            # html_content = htmly.render(d)
            text_content = render_to_string('email/email.txt',{'context':d})
            html_content = render_to_string('email/email.html',{'context':d})
            msg = EmailMultiAlternatives(subject, text_content, user_email, [dsi_email])
            msg.attach_alternative(html_content, "text/html")
            try:
                msg.send()
            except Exception as e:
                raise

            #send_mail(subject, message, from_email, [to])

            ########################
            #  DSI EMAIl
            d = {}
            d['ref'] = self.object.get_ref
            d['user'] = self.object.titre
            d['user'] = self.object.user.username
            d['client'] = self.object.user.client.name


            d['ticket_url'] = "http://{0}{1}".format(self.request.META['HTTP_HOST'],
                            reverse("solutions:questiondetail", kwargs={"pk": self.object.pk}))


            text_content = render_to_string('email/email_client.txt',{'context':d})
            html_content = render_to_string('email/email_client.html',{'context':d})
            msg = EmailMultiAlternatives(subject, text_content, dsi_email, [user_email])
            msg.attach_alternative(html_content, "text/html")
            try:
                msg.send()
            except Exception as e:
                raise
            add_notification_to_cosultant("{0} {1}".format(self.object.user.username, _('Has opened a new ticket')), self.object.pk)

            # send_mail(subject, message, 'no_replay@ntonadvisory.com' , [from_email])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activePage']= 'new_ticket'
        context['notification'] = self.request.user.get_notification()
        return context

class QuestionEdit(LoginRequiredMixin, generic.UpdateView):
    fields = ("titre", "description","image")
    model = Question

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activePage']= 'ticket'
        return context
    #success_url = reverse_lazy("solutions:questiondetail ",kwargs={"pk": Question.pk})

class QuestionSingle(LoginRequiredMixin, generic.DetailView):
    model = Question

    def get_context_data(self, **kwargs):
        context = super(QuestionSingle, self).get_context_data(**kwargs)
        context['form'] = ReponceForm
        context['activePage']= 'ticket'
        return context

    def get_object(self):
        obj=super().get_object()
        # Record the last accessed dateobj.last_accessed=timezone.now()obj.save()
        if self.request.user.is_staff or self.request.user == obj.user:
            if not obj.viwed_at and self.request.user.is_staff :
                obj.viwed_at = timezone.now()
                obj.save()
            return obj
        else:
            raise Http404(_("ticket does not exist"))
            return

class QuestionList(LoginRequiredMixin, generic.ListView):
    model = Question
    paginate_by = 100

    def get_queryset(self):
        query = self.request.GET.get('q')
        self.paginate_by =  int(self.request.GET.get('paginate_by', 10))


        if self.request.user.is_staff:
            questionlist =  Question.objects.all()
        else:
            questionlist =  Question.objects.filter(user=self.request.user)
        # print(questionlist)
        #### filtre by priorite
        if self.request.GET.get('priorite'):
            questionlist = questionlist.filter(priorite = self.request.GET.get('priorite'))

        if self.request.GET.get('status'):
            questionlist = questionlist.filter(status = self.request.GET.get('status'))
        if query:
            questionlist = questionlist.filter(
                            Q(description__icontains=query) | Q(titre__icontains=query)
                            )

        return questionlist


    def get_context_data(self, **kwargs):
        context = super(QuestionList, self).get_context_data(**kwargs)
        page = int(self.request.GET.get('page', 1))
        context['pages'] = [val for val in range(page - 5 , page + 5) if val > 0]
        if self.request.GET.get('q') : context['query'] = '&q='+self.request.GET.get('q')

        if self.request.GET.get('status'):
            context['status']= '&status='+(self.request.GET.get('status'))
            active[self.request.GET.get('status')] = "selected"
        if self.request.GET.get('priorite'):
            context['priorite']= '&priorite='+(self.request.GET.get('priorite'))
            active[self.request.GET.get('priorite')] = "selected"
        context['activePage']= 'ticket'



        return context



@login_required
def add_reponce_to_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == "POST":
        form = ReponceForm(request.POST)
        if form.is_valid():
            try:
                reponce = form.save(commit=False)
                reponce.question = question
                reponce.user = request.user
                question.last_action = timezone.now()
                question.status = reponce.status
                if not question.first_react_at: question.first_react_at = timezone.now()
                if reponce.status == 'RS':
                    question.resolved_at = timezone.now()

                reponce.save()
                question.save()
                if reponce.user.is_staff:
                    question.user.add_notification('{0} {1} {2}'.format(reponce.user,_('acted on ticket'),question.ref),question.pk)
                else:
                    question.charged_by.add_notification('{0} {1} {2}'.format(reponce.user,_('acted on ticket'),question.ref),question.pk)
            except IntegrityError:
                messages.warning(request,_("Warning, Something went wrong, please try again"))
            else:
                messages.success(request,_("Answere has been saved."))


            return redirect('solutions:questiondetail', pk=question.pk)

    else:
        form = ReponceForm()
    return render(request, 'solutions/reponce_form.html', {'form': form})

@login_required
def questioneResolved(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == "POST":
        try:
            question.status = 'RS'
            question.resolved_at = timezone.now()
            if not question.first_react_at: question.first_react_at = timezone.now()
            question.last_action = timezone.now()

            question.save()
        except IntegrityError:
            messages.warning(request,_("Warning, Something went wrong, please try again"))
        else:
            messages.success(request,_("ticket has been resolved, thanks for using owr platform."))

    return redirect('solutions:questiondetail', pk=question.pk)

def load_categories(request):
    categorieId = request.GET.get('categorie')
    souscategorie = SousCategorie.objects.filter(categorie=categorieId).order_by('name')
    return render(request, 'solutions/categorie_dropdown_list_options.html', {'souscategorie': souscategorie})

def load_chart(request):
    chart = {}
    start_date = datetime.date.today() - timedelta(days=20)
    if request.GET.get('start_date'):
        start_date = datetime.datetime.strptime(request.GET.get('start_date', '{}'.format(start_date)), '%Y-%m-%d').date()
    #timezone.make_aware(start_date)

    end_date = datetime.date.today()
    if request.GET.get('end_date'):
        end_date = datetime.datetime.strptime(request.GET.get('end_date', '{}'.format(end_date)), '%Y-%m-%d').date()
    if end_date > datetime.date.today():
        end_date = datetime.date.today()
        #request.GET['end_date'] = end_date

    #timezone.make_aware(end_date)


    if request.GET.get('type')=='pie':
        if request.user.is_staff:
            dataset = Question.objects \
                .values('status') \
                .exclude(status='') \
                .annotate(total=Count('status')) \
                .order_by('status')
        else:
            dataset = Question.objects.filter(user = request.user) \
                .values('status') \
                .exclude(status='') \
                .annotate(total=Count('status')) \
                .order_by('status')

        port_display_name = dict()
        for port_tuple in Question.Status:
            port_display_name[port_tuple[0]] = port_tuple[1]

        chart = {
            'chart': {'type': 'pie'},
            'backgroundColor': 'transparent',
            'title': {'text': _("Ticket's Status - Total ({})".format(dataset.count()) )},
            'series': [{
                'name': 'Tickets',
                'data': list(map(lambda row: {'name': port_display_name[row['status']], 'y': row['total']}, dataset))
            }]
        }

    if request.GET.get('type')=='line':
        metrics = {
            'total': Count('created_at__date')
        }

        if request.user.is_staff:
            dataset = Question.objects.all()\
                .values('created_at__date')\
                .annotate(**metrics)\
                .order_by('created_at__date')
        else:
            dataset = Question.objects.filter(user = request.user)\
                .values('created_at__date')\
                .annotate(**metrics)\
                .order_by('created_at__date')


        datasetAction = Reponce.objects.filter(created_at__gte=start_date,\
                    created_at__lte=end_date)\
            .values('created_at__date')\
            .annotate(**metrics)\
            .order_by('created_at__date')

        dates = list()
        action_series_data = list()
        survived_series_data = list()

        dateT = start_date
        while dateT <= end_date:
            # print(entry)
            dates.append('%s' % dateT)
            # print(entry['created_at__date'])
            try:
                survived_series_data.append(dataset.get(created_at__date = dateT).get('total'))
            except Exception as e:
                survived_series_data.append(0)
            try:
                action_series_data.append(datasetAction.get(created_at__date = dateT).get('total'))
            except Exception as e:
                action_series_data.append(0)

            #survived_series_data.append(entry['total'])
            dateT = dateT + timedelta(days=1)

        action_series = {
            'name': 'Action',
            'data': action_series_data,
            'color': 'green'
        }
        survived_series = {
            'name': 'Tickets',
            'data': survived_series_data,
            'color': 'blue'
        }
        chart = {
            'chart': {'type': 'line'},
            'backgroundColor': 'transparent',
            'title': {'text': ''},
            'xAxis': {'categories': dates,},
            'series': [survived_series, ]
        }
    if request.GET.get('type')=='colomn':
        #client = request.GET.get('client')
        dataset = Question.objects \
            .values('user__client__name') \
            .annotate(total=Count('user__client__name')) \
            .order_by('user__client__name')

        categories = list()
        tickets_series = list()

        for entry in dataset:
            categories.append('%s' % entry['user__client__name'])
            tickets_series.append(entry['total'])

        tickets_series_data = {
            'name': 'Tickets',
            'data': tickets_series,
            'color': 'green'
        }


        chart = {
            'chart': {'type': 'column'},
            'backgroundColor': 'transparent',
            'title': {'text': ''},
            'xAxis': {'categories': categories,},
            'series': [tickets_series_data, ]
        }

    if request.GET.get('type')=='users':
                #\
            # dataset = User.objects\
            #     .filter(is_staff=True)\
            #     .annotate(total=Count('charged_tickets'))\
            #     .annotate(status=Count('charged_tickets__status'=='RS'))\
            #     .annotate(avg = Avg('charged_tickets__time_to_resolv'))
            dataset = User.objects\
                .values('username','email')\
                .filter(is_staff=True)\
                .annotate(total=Count(F('charged_tickets'),output_field=FloatField()),
                    resolved=Count('charged_tickets__status', filter=Q(charged_tickets__status='RS')),
                    avg = Cast('resolved', FloatField()) / Cast('total', FloatField())    * 100,
                    avgTime = Avg('charged_tickets__time_to_resolv', filter=Q(charged_tickets__status='RS')),# / Count('charged_tickets__status', filter=Q(charged_tickets__status='RS')),
                    #avgTime = Sum(F('charged_tickets__time_to_resolv')) / Count('charged_tickets__status', filter=Q(charged_tickets__status='RS')),
                    )

            # avg = dataset
            print(dataset)
            # for entry in dataset:
            #     print(entry.avg)

            #ds = json.dumps(dataset)
            # data = list(dataset)  # wrap in list(), because QuerySet is not JSON serializable
            # return JsonResponse({'data': data})
            from django.core import serializers
            from django.http import HttpResponse


            dataset=''
            qs_json = serializers.serialize('json', dataset)
            return HttpResponse(qs_json, content_type='application/json')




    return JsonResponse(chart)

@login_required
def questioneCharged(request, pk):
    question = get_object_or_404(Question, pk=pk)
    try:
        question.charged_by = request.user
        question.resolved_at = timezone.now()
        if not question.first_react_at: question.first_react_at = timezone.now()
        question.last_action = timezone.now()
        question.save()
    except IntegrityError:
        messages.warning(request,_("Warning, Something went wrong, please try again"))
    else:
        messages.success(request,_("ticket has been taked in charge."))
        question.user.add_notification(_("ticket has been taked in charge."), question.pk)

    return JsonResponse({'ok':'ok'}, status=200)
