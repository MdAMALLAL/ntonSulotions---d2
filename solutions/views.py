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
# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger()

## models
from accounts.models import User,Notification
from clients.models import Client
from .models import Question,Reponce, Categorie, SousCategorie
from .forms import ReponceForm, QuestionForm


####################################################
# QUESTION: CRUD

def add_notification_to_cosultant(description_en,description_fr, url):
    consultants = User.objects.filter(is_staff = True)
    for consultant in consultants:
        notification = Notification.objects.create(user=consultant,description_en = description_en, description_fr =description_fr, url=url)
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
        except Exception as e:
            logger.error(e)
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
            d['title'] = self.object.titre
            d['user'] = self.object.user.username
            d['client'] = self.object.user.client.name

            d['ticket_url'] = "http://{0}{1}".format(self.request.META['HTTP_HOST'],
                                reverse("solutions:questiondetail", kwargs={"pk": self.object.pk}))


            user_email = self.object.user.email
            dsi_email = self.object.user.client.email
            # text_content = plaintext.render(d)
            # html_content = htmly.render(d)
            text_content = render_to_string('email/email_client.txt',{'context':d})
            html_content = render_to_string('email/email_client.html',{'context':d})

            msg = EmailMultiAlternatives(subject, text_content, user_email, [dsi_email])
            msg.attach_alternative(html_content, "text/html")
            try:
                msg.send()
            except Exception as e:
                logger.error(e)

            #send_mail(subject, message, from_email, [to])

            ########################
            #  DSI EMAIl
            d = {}
            d['ref'] = self.object.get_ref
            d['title'] = self.object.titre
            d['user'] = self.object.user.username
            d['client'] = self.object.user.client.name


            d['ticket_url'] = "http://{0}{1}".format(self.request.META['HTTP_HOST'],
                            reverse("solutions:questiondetail", kwargs={"pk": self.object.pk}))

            text_content = render_to_string('email/email.txt',{'context':d})
            html_content = render_to_string('email/email.html',{'context':d})
            msg = EmailMultiAlternatives(subject, text_content, dsi_email, [user_email])
            msg.attach_alternative(html_content, "text/html")
            try:
                msg.send()
            except Exception as e:
                logger.error(e)
            add_notification_to_cosultant(
                description_en = "{0} {1}".format(self.object.user.username, 'Has opened a new ticket'),
                description_fr = "{0} {1}".format(self.object.user.username, 'A ouvert un nouveau ticket'),
                self.object.pk)



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
        active = {}
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
    if request.is_ajax() and request.POST.get('action') == "post":
        try:
            description = request.POST.get('description')
            status = request.POST.get('status')
            send_mail = request.POST.get('send_mail', False)

                # if status == 'FR':
                #     description = '{0} {1}'.format(_('Ticket status has charged to Closedd by'), request.user)

            reponce = Reponce(
                user = request.user,
                description = description,
                question = question,
                status = status,
                send_mail = send_mail ,
                )
            if  reponce.description == "" : reponce.description = 'Ticket status has changed to {0} by {1}'.format(reponce.get_status_display(), request.user)

            reponce.save()
            question.status = status
            if not question.first_react_at: question.first_react_at = timezone.now()
            if status == 'RS':
                question.resolved_at = timezone.now()
            if reponce.user.is_staff and not question.charged_by:
                question.charged_by = request.user

            question.save()
        except Exception as e:
            logger.error(e)
        else:
            ref = question.get_ref()
            if reponce.user.is_staff:
                question.user.add_notification(
                    description_en = '{0} {1} {2}'.format(reponce.user,'acted on ticket',ref),
                    description_fr = '{0} {1} {2}'.format(reponce.user,'agi on ticket',ref),
                    question.pk)
            else:
                question.charged_by.add_notification(
                description_en = '{0} {1} {2}'.format(reponce.user,'acted on ticket',ref),
                description_fr = '{0} {1} {2}'.format(reponce.user,'agi on ticket',ref),
                question.pk)
            if send_mail:
                #print(send_mail)

                d = {}

                d['description'] = description

                subject = _('novelty on ticket {}'.format(ref))
                text_content = render_to_string('email/email-report.txt',{'context':d})
                html_content = render_to_string('email/email-report.html',{'context':d})
                msg = EmailMultiAlternatives(subject, text_content, reponce.user.email, [question.user.email])
                msg.attach_alternative(html_content, "text/html")
                try:
                    msg.send()
                except Exception as e:
                    #print(e)
                    logger.error(e)
        data = {}
        data['html_content'] = render_to_string('solutions/action.html', {'reponce': reponce})
        #from django.core import serializers
        data['last_action'] = str(question.last_action.strftime('%m/%d/%Y %H:%m'))
        data['time_toreact'] = str(question.get_time_to_react())
        data['time_toresolv'] = str(question.get_time_to_resolv())
        data['resolved_at'] = question.get_resolved_at()
        data['status_display'] = str(question.get_status_display())



        #return render(request, 'solutions/action.html', {'reponce': reponce})
        return JsonResponse(data, safe=False)

    elif request.method == "POST":
        form = ReponceForm(request.POST)
        if form.is_valid():
            try:
                reponce = form.save(commit=False)
                if  reponce.description == "" : reponce.description = 'Ticket status has charged to {0} by {1}'.format(reponce.get_status_display(), request.user)

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
                    question.user.add_notification(
                        description_en = '{0} {1} {2}'.format(reponce.user,'acted on ticket',question.get_ref()),
                        description_fr = '{0} {1} {2}'.format(reponce.user,'agi on ticket',question.get_ref()),
                        question.pk)
                else:
                    question.charged_by.add_notification(
                        description_en = '{0} {1} {2}'.format(reponce.user,'acted on ticket',question.get_ref()),
                        description_fr = '{0} {1} {2}'.format(reponce.user,'agi on ticket',question.get_ref()),
                        question.pk)
            except Exception as e :
                logger.error(e)
                messages.warning(request,_("Warning, Something went wrong, please try again"))
            else:
                messages.success(request,_("Answere has been saved."))
                ref = question.get_ref()
                if reponce.user.is_staff:
                    question.user.add_notification(
                        description_en = '{0} {1} {2}'.format(reponce.user,'acted on ticket',question.get_ref()),
                        description_fr = '{0} {1} {2}'.format(reponce.user,'agi on ticket',question.get_ref()),
                        question.pk)
                else:
                    question.charged_by.add_notification(
                        description_en = '{0} {1} {2}'.format(reponce.user,'acted on ticket',question.get_ref()),
                        description_fr = '{0} {1} {2}'.format(reponce.user,'agi on ticket',question.get_ref()),
                        question.pk)
                if send_mail:
                    d = {}

                    d['description'] = description

                    subject = _('novelty on ticket {}'.format(ref))
                    text_content = render_to_string('email/email-report.txt',{'context':d})
                    html_content = render_to_string('email/email-report.html',{'context':d})
                    msg = EmailMultiAlternatives(subject, text_content, reponce.user.email, [question.user.email,])
                    msg.attach_alternative(html_content, "text/html")
                    try:
                        msg.send()
                    except Exception as e:
                        logger.error(e)

            return redirect('solutions:questiondetail', pk=question.pk)
    else:
        form = ReponceForm()
    return render(request, 'solutions/reponce_form.html', {'form': form})
@login_required
def questioneResolved(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == "POST":
        try:
            description = 'Ticket status has changed to resolved by {}'.format(request.user)
            reponce = Reponce(
                user = request.user,
                description = description,
                question = question,
                status = 'RS',
                send_mail = False ,
                )
            reponce.save()
            question.status = 'RS'
            question.resolved_at = timezone.now()
            if not question.first_react_at: question.first_react_at = timezone.now()
            question.last_action = timezone.now()

            question.save()
        except Exception as e:
            logger.error(e)
            messages.warning(request,_("Warning, Something went wrong, please try again"))
        else:
            messages.success(request,_("ticket has been resolved, thanks for using owr platform."))
            ref = question.get_ref()
            if reponce.user.is_staff:
                question.user.add_notification(
                    description_en = 'Ticket ({0}) {1} {2}'.format(ref, _('marked as resolved by'),reponce.user),
                    description_fr = 'Ticket ({0}) {1} {2}'.format(ref, _('marqué comme résolu par'),reponce.user),
                    question.pk)
            else:
                question.charged_by.add_notification(
                    description_en = 'Ticket ({0}) {1} {2}'.format(ref, _('marked as resolved by'),reponce.user),
                    description_fr = 'Ticket ({0}) {1} {2}'.format(ref, _('marqué comme résolu par'),reponce.user),
                    question.pk)


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
    end_date = datetime.date.today()
    if request.GET.get('end_date'):
        end_date = datetime.datetime.strptime(request.GET.get('end_date', '{}'.format(end_date)), '%Y-%m-%d').date()
    if end_date > datetime.date.today():
        end_date = datetime.date.today()
    client = request.GET.get('client')
    if client : client = get_object_or_404(Client, slug=client)
    user = get_object_or_404(User, username= request.GET.get('user', request.user.username))
    type = request.GET.get('type')
    all = request.GET.get('all',False)

    if type =='pie':
        if all :
            dataset = Question.objects.all() \
                .values('status') \
                .exclude(status='') \
                .annotate(total=Count('status')) \
                .order_by('status')
        elif client:
            dataset = Question.objects.filter(user__client = client) \
                .values('status') \
                .exclude(status='') \
                .annotate(total=Count('status')) \
                .order_by('status')

        else:
            if user.is_staff:
                dataset = Question.objects.filter(charged_by = user) \
                    .values('status') \
                    .exclude(status='') \
                    .annotate(total=Count('status')) \
                    .order_by('status')
            else:
                dataset = Question.objects.filter(user = user) \
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
            'title': '',
            'series': [{
                'name': 'Tickets',
                'data': list(map(lambda row: {'name': port_display_name[row['status']], 'y': row['total']}, dataset))
            }]
        }
    if type == 'line':
        metrics = {
            'total': Count('created_at__date')
        }
        if all == True :
            dataset = Question.objects.all()\
                .values('created_at__date')\
                .annotate(**metrics)\
                .order_by('created_at__date')

        elif client:
            dataset = Question.objects.filter(user__client = client)\
                .values('created_at__date')\
                .annotate(**metrics)\
                .order_by('created_at__date')

        else:
            if user.is_staff:
                dataset = Question.objects.filter(charged_by = user) \
                    .values('created_at__date')\
                    .annotate(**metrics)\
                    .order_by('created_at__date')
            else:
                dataset = Question.objects.filter(user = user) \
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
    if type == 'colomn':
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

    return JsonResponse(chart)

@login_required
def questioneCharged(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.is_ajax():
        try:
            description = 'Ticket status has been taked into account by {}'.format(request.user)
            reponce = Reponce(
                user = request.user,
                description = description,
                question = question,
                status = 'EA',
                send_mail = False ,
                )
            reponce.save()
            question.status = 'EA'
            if not question.first_react_at: question.first_react_at = timezone.now()
            question.last_action = timezone.now()
            question.charged_by = request.user
            question.save()
        except Exception as e:
            logger.error(e)
        else:
            ref = question.get_ref()
            if reponce.user.is_staff:
                question.user.add_notification(
                    description_en = 'Ticket ({0}) {1} {2}'.format(ref, _('has been taked into account by'),reponce.user),
                    description_fr = 'Ticket ({0}) {1} {2}'.format(ref, _('a été pris en charge par'),reponce.user),
                    question.pk)
            else:
                question.charged_by.add_notification(
                    description_en = 'Ticket ({0}) {1} {2}'.format(ref, _('has been taked into account by'),reponce.user),
                    description_fr = 'Ticket ({0}) {1} {2}'.format(ref, _('a été pris en charge par'),reponce.user),
                    question.pk)

        data = {}
        data['html_content'] = render_to_string('solutions/action.html', {'reponce': reponce})
        #from django.core import serializers
        data['last_action'] = str(question.last_action.strftime('%m/%d/%Y %H:%m'))
        data['time_toreact'] = str(question.get_time_to_react())
        data['time_toresolv'] = str(question.get_time_to_resolv())
        data['resolved_at'] = question.get_resolved_at()
        data['status_display'] = str(question.get_status_display())

        return JsonResponse(data)

    elif request.method == "POST":
        try:
            description = 'Ticket status has been taked into account by {}'.format(request.user)
            reponce = Reponce(
                user = request.user,
                description = description,
                question = question,
                status = 'EA',
                send_mail = False ,
                )
            reponce.save()
            question.status = 'EA'
            if not question.first_react_at: question.first_react_at = timezone.now()
            question.last_action = timezone.now()
            question.charged_by = request.user
            question.save()
        except Exception as e:
            logger.error(e)
            messages.warning(request,_("Warning, Something went wrong, please try again"))
        else:
            messages.success(request,_("Ticket has been taked into account."))
            ref = question.get_ref()
            if reponce.user.is_staff:
                question.user.add_notification(
                    description_en = 'Ticket ({0}) {1} {2}'.format(ref, _('has been taked into account by'),reponce.user),
                    description_fr = 'Ticket ({0}) {1} {2}'.format(ref, _('a été pris en charge par'),reponce.user),
                    question.pk)
                question.charged_by.add_notification(
                    description_en = 'Ticket ({0}) {1} {2}'.format(ref, _('has been taked into account by'),reponce.user),
                    description_fr = 'Ticket ({0}) {1} {2}'.format(ref, _('a été pris en charge par'),reponce.user),
                    question.pk)

        return redirect('solutions:questiondetail', pk=question.pk)
