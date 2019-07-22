from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.views.generic import ArchiveIndexView
from django.core.paginator import Paginator

from basicapp.forms import TestSessionForm, AnswerForm, AnswerFormSet, UserRegisterForm
from basicapp.models import Question, TestSession, UserProfileInfo


def index(request):
    return render(request, 'basicapp/index.html')



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfileInfo.objects.create(profile_image=request.POST.get('profile_image', 'default.jpg'), user=user)
            username = form.cleaned_data.get('username')
            messages.success(request, f'{username} Your Account was created successfully! Please Login')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'basicapp/registration.html', {'form': form})


@login_required()
def test_session(request):
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
            formset_class = formset_factory(AnswerForm, AnswerFormSet)
            formset = formset_class(questions=questions, initial=[
                {
                    'user': request.user.id,
                    'session': session.id,
                    'question': question.id,
                } for question in questions])
            return render(request, 'basicapp/test.html', {'formset': formset, 'time_for': n * 10})

    return HttpResponseRedirect(reverse('index'))


@login_required()
def submit_test_session(request):
    if request.method == 'POST':
        AnswerFormSet = formset_factory(AnswerForm, extra=0, max_num=0)
        formset = AnswerFormSet(data=request.POST)
        answers = []
        now = timezone.now()
        session = None
        if formset.is_valid():
            for form in formset:
                if len(form.cleaned_data) != 0:
                    if session is None:
                        session = form.cleaned_data['session']
                        session.finished_at = now
                        session.save()
                        if now - session.created_at - timezone.timedelta(
                                seconds=session.no_of_questions * 10) > timezone.timedelta(seconds=0):
                            messages.warning(request, f'Time is up')
                        else:
                            messages.success(request, f'You have passed successfully')

                    answers.append(form.save(commit=True))
        data = list(map(lambda answer: {'choice': answer.choice, 'word': answer.question.word}, answers))
        correct_answers = sum(list(map(lambda answer: answer.is_correct, answers)))
        return render(request, 'basicapp/result_page.html',
                      {'data': data,
                       'correct': correct_answers,
                       'wrong': len(answers) - correct_answers, })
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
        data['correct_answers'] = UserProfileInfo.objects.filter(user=self.request.user)[0].correct_answers()
        data['incorrect_answers'] = UserProfileInfo.objects.filter(user=self.request.user)[0].incorrect_answers()
        data['total_answers'] = UserProfileInfo.objects.filter(user=self.request.user)[0].total_answers()

        count_success = 0
        test_sessions = TestSession.objects.filter(answers__user=self.request.user).distinct()
        for test_session in test_sessions:
            if test_session.finished_at < test_session.created_at + \
                    timezone.timedelta(seconds=test_session.no_of_questions * 10):
                count_success += 1
        data['success'] = count_success
        data['fail'] = len(test_sessions) - count_success

        return data

