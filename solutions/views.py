from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.mail import BadHeaderError, send_mail
from django.contrib.auth.mixins import(LoginRequiredMixin, PermissionRequiredMixin  )
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.db import IntegrityError
from django.views import generic
from .models import Question,Reponce, Categorie, SousCategorie
from .forms import ReponceForm, QuestionForm
from django.http import Http404
from django.utils.translation import gettext_lazy as _


# Create your views here.
class IndexView(generic.TemplateView):
    # Just set this Class Object Attribute to the template page.
    # template_name = 'app_name/site.html'
    template_name = 'index.html'



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
            message = self.object.description

            from_email = self.object.user.email
            #send_mail(subject, message, from_email, ['no_replay@ntonadvisory.com'])

            subject = self.object.titre
            message = self.object.description
            from_email = 'admin@example.com'
            #send_mail(subject, message, from_email, [self.object.user.email,])
            #return redirect('solutions:questiondetail', pk=self.object.pk)
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
            return obj
        else:
            raise Http404(_("ticket does not exist"))
            return

bypage = 3
class QuestionList(LoginRequiredMixin, generic.ListView):
    model = Question
    pagecounter = 0
    page = 0

    # def get(self, request, *args, **kwargs):
    #     if request.GET.get('page'):
    #         self.page = int(request.GET.get('page'))
    #     return super(QuestionList, self).get(request, *args, **kwargs)

    def get_queryset(self):
        questionlist = Question.objects.all()
        if self.request.user.is_staff:
            questionlist =  Question.objects.all()
        else:
            questionlist =  Question.objects.filter(user=self.request.user)

        #### filtre by priorite
        if self.request.GET.get('priorite'):
            questionlist = questionlist.filter(priorite = self.request.GET.get('priorite'))

        if self.request.GET.get('status'):
            questionlist = questionlist.filter(status = self.request.GET.get('status'))


        if self.request.GET.get('page'):
            self.page = int(self.request.GET.get('page'))
        #print(self.page)
        self.pagecounter = int(questionlist.count() / bypage - 0.5)
        #self.page = self.kwargs.get('page')
        #print(self.pagecounter)

        if self.page <= self.pagecounter:
            #print(self.page)
            return questionlist[self.page * bypage :(self.page + 1) * bypage]
        else:
            #self.page = self.pagecounter
            raise Http404





    def get_context_data(self,**kwargs):


        active = {}

        context=super().get_context_data(**kwargs)
        context['inpage']=self.page
        context['pagecounter']=self.pagecounter

        if self.request.GET.get('status'):
            context['status']= '&status='+(self.request.GET.get('status'))
            active[self.request.GET.get('status')] = "active"
        if self.request.GET.get('priorite'):
            context['priorite']= '&priorite='+(self.request.GET.get('priorite'))
            active[self.request.GET.get('priorite')] = "active"
        context['active'] = active
        context['preview']=0
        if self.page: context['preview']= self.page - 1
        context['next']=self.pagecounter
        if not self.page == self.pagecounter: context['next']=self.page + 1



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
                reponce.save()
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
