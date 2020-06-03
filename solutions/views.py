from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.mail import BadHeaderError, send_mail
from django.contrib.auth.mixins import(LoginRequiredMixin, PermissionRequiredMixin  )
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.db import IntegrityError
from django.views import generic
from clients.models import Client
from .models import Question,Reponce, Categorie, SousCategorie
from .forms import ReponceForm, QuestionForm
from django.http import Http404
from django.utils import timezone
from django.db.models import Count,Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from django.utils.translation import gettext_lazy as _
import datetime, pytz
from datetime import timedelta
#from django.utils.timezone import make_aware
#### send email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context




####################################################
# QUESTION: CRUD


class QuestionCreate(LoginRequiredMixin, generic.CreateView):
    model = Question
    form_class = QuestionForm
    print('in view')
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
            subject = self.object.titre
            message = """Nouvuou ticket a ete ouvert
            sous id : {0} et titre : {1};
            par : {2};
            (http://{3}{4})
            """.format(self.object.id,
                        self.object.titre,
                        self.object.user,
                        #self.object.Priorite([self.object.priorite]),
                        self.request.META['HTTP_HOST'],
                        reverse("solutions:questiondetail", kwargs={"pk": self.object.pk})
                        )
            from_email = self.object.user.email
            to = self.object.user.client.email
            send_mail(subject, message, from_email, [to])

            message = """Votre ticket a ete ouvert
            sous id : {0} et titre : {1};
            Suivi le a (http://{2}{3})
            """.format(self.object.id,
                        self.object.titre,
                        #self.object.Priorite([self.object.priorite]),
                        self.request.META['HTTP_HOST'],
                        reverse("solutions:questiondetail", kwargs={"pk": self.object.pk})
                        )
            from_email = self.object.user.email
            to = self.object.user.client.email
            send_mail(subject, message, '' , [from_email])
        return super().form_valid(form)

class QuestionEdit(LoginRequiredMixin, generic.UpdateView):
    fields = ("titre", "description","image")
    model = Question
    #success_url = reverse_lazy("solutions:questiondetail ",kwargs={"pk": Question.pk})

class QuestionSingle(LoginRequiredMixin, generic.DetailView):
    model = Question
    def get_context_data(self, **kwargs):
        context = super(QuestionSingle, self).get_context_data(**kwargs)
        context['form'] = ReponceForm
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
    paginate_by = 10


    def get_queryset(self):
        query = self.request.GET.get('q')
        self.paginate_by =  int(self.request.GET.get('paginate_by', 10))


        if self.request.user.is_staff:
            questionlist =  Question.objects.all()
        else:
            questionlist =  Question.objects.filter(user=self.request.user)
        print(questionlist)
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
        active = {}
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
        context['active'] = active

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
                reponce.user= request.user
                question.last_action = timezone.now()
                question.status = reponce.status
                if not question.first_react_at: question.first_react_at = timezone.now()
                if reponce.status == 'RS':
                    question.resolved_at = timezone.now()

                reponce.save()
                question.save()
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

    else:
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
        dataset = Question.objects \
            .values('status') \
            .exclude(status='') \
            .annotate(total=Count('status')) \
            .order_by('status')

        port_display_name = dict()
        for port_tuple in Question.Status:
            port_display_name[port_tuple[0]] = port_tuple[1]

        chart = {
            'chart': {'type': 'pie'},
            'title': {'text': _("Ticket's Status - Total ({})".format(Question.objects.count()) )},
            'series': [{
                'name': 'Status',
                'data': list(map(lambda row: {'name': port_display_name[row['status']], 'y': row['total']}, dataset))
            }]
        }

    if request.GET.get('type')=='line':
        metrics = {
            'total': Count('created_at__date')
        }
        dataset = Question.objects.all()\
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
            'title': {'text': ''},
            'xAxis': {'categories': dates,},
            'series': [survived_series, action_series]
        }

    return JsonResponse(chart)
