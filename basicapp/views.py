from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.views.generic import ArchiveIndexView, UpdateView

from basicapp.forms import TestSessionForm, AnswerForm, AnswerFormSet, UserRegisterForm, UserProfileInfoForm
from basicapp.models import Question, TestSession, UserProfileInfo, Answer


def index(request):
    return render(request, 'basicapp/index.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfileInfo.objects.create(user=user)
            username = form.cleaned_data.get('username')
            messages.success(request, f'{username} Your Account was created successfully! Please Login')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'basicapp/registration.html', {'form': form})


@login_required()
def test_session(request, pk=None):
    if request.method == 'POST':
        form = TestSessionForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            n = data['no_of_questions']
            q_nums = Question.objects.count()
            if q_nums < n:
                return HttpResponseRedirect(reverse('index'))
            session = TestSession.objects.create(no_of_questions=n)
            questions = Question.objects.order_by('?')[:n]
            answers = []
            for question in questions:
                answers.append(Answer.objects.create(session=session, user=request.user, question=question))
            formset_class = formset_factory(AnswerForm, AnswerFormSet)
            formset = formset_class(questions=questions, initial=[
                {

                    'id': answer.id,
                } for answer in answers])
            return render(request, 'basicapp/test.html', {'formset': formset, 'time_for': n * 10})

    if request.method == 'GET':

        if request.user:
            questions = Question.objects.filter(answers__session_id=pk, answers__user=request.user).distinct()
            if questions.count() == 0:
                messages.warning(request, f'Invalid request')
                return redirect('/')
            answers = Answer.objects.filter(question__in=questions, session=pk)
            n = TestSession.objects.get(id=pk).no_of_questions

            formset_class = formset_factory(AnswerForm, AnswerFormSet)
            formset = formset_class(questions=questions, initial=[{'id': answer.id} for answer in answers])

            return render(request, 'basicapp/test.html', {'formset': formset, 'time_for': n * 10})
        else:
            return redirect('/')
    return HttpResponseRedirect(reverse('index'))


@login_required()
def submit_test_session(request):
    if request.method == 'POST':
        AnswerFormSet = formset_factory(AnswerForm, extra=0, max_num=0)
        formset = AnswerFormSet(data=request.POST)
        answers = []
        now = timezone.now()
        sess_created_at = None
        sess_no_questions = None
        session = None
        if formset.is_valid():
            for form in formset.forms:
                if len(form.cleaned_data) != 0:
                    if session is None:
                        answer_id = form.cleaned_data['id']
                        answer = Answer.objects.get(pk=answer_id)
                        answer.choice = form.cleaned_data['choice']
                        sess_created_at = answer.session.created_at
                        sess_no_questions = answer.session.no_of_questions
                        answer.session.finished_at = timezone.now()
                        answer.session.save()

                        answer.save()
                        answers.append(answer)

        if now - sess_created_at > timezone.timedelta(
                seconds=sess_no_questions * 10):
            messages.warning(request, f'Time is up')
            return redirect('/')
        else:
            messages.success(request, f'On time')

        data = list(map(lambda answer: {'choice': answer.choice, 'word': answer.question.word}, answers))
        correct_answers = sum(list(map(lambda answer: answer.is_correct, answers)))
        return render(request, 'basicapp/result_page.html',
                      {'data': data,
                       'correct': correct_answers,
                       'wrong': len(formset.forms) - correct_answers})
    else:
        return HttpResponseRedirect(reverse('index'))


class TestSessionArchiveView(ArchiveIndexView):
    template_name = 'basicapp/snippet_archive.html'
    queryset = TestSession.objects.all()
    paginate_by = 5

    def get_queryset(self):
        if self.request and self.request.user:
            self.queryset = TestSession.objects.filter(answers__user=self.request.user).distinct()

        return super().get_queryset()

    def get_template_names(self):
        return [self.template_name]


class ProfileView(ArchiveIndexView):
    template_name = 'basicapp/profile.html'
    queryset = TestSession.objects.all()
    paginate_by = 5

    def get_queryset(self):
        if self.request and self.request.user:
            self.queryset = TestSession.objects.filter(answers__user=self.request.user).distinct()

        return super().get_queryset()

    def get_template_names(self):
        return [self.template_name]

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        count_success = 0
        test_sessions = TestSession.objects.filter(answers__user=self.request.user, finished_at__isnull=False).order_by(
            '-created_at')
        not_finished = TestSession.objects.filter(answers__user=self.request.user, finished_at__isnull=True).last()

        for session in test_sessions:

            if session.finished_at < session.created_at + \
                    timezone.timedelta(seconds=session.no_of_questions * 10):
                count_success += 1
        data['correct_answers'] = UserProfileInfo.objects.get(user=self.request.user).correct_answers()
        data['incorrect_answers'] = UserProfileInfo.objects.get(user=self.request.user).incorrect_answers()
        data['not_finished'] = not_finished

        data['success'] = count_success
        data['fail'] = test_sessions.count() - count_success
        data['test'] = test_sessions
        return data


class ProfileUpdateView(UpdateView):
    template_name = 'basicapp/profile_update.html'
    form_class = UserProfileInfoForm
    success_url = '/profile'

    def get_object(self, **kwargs):
        return self.request.user.userprofileinfo
