from django import forms
from django.forms import ModelForm, BaseFormSet
from django.utils.functional import cached_property
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from basicapp.models import Question, Answer, UserProfileInfo


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class UserProfileInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfileInfo
        fields = ['portfolio_site', 'profile_image']


class TestSessionForm(forms.Form):
    no_of_questions = forms.IntegerField()

    def clean_no_of_questions(self):
        data = self.cleaned_data['no_of_questions']
        if data <= 0:
            raise forms.ValidationError("no_of_questions field should be bigger than 0")

        return data


class AnswerForm(ModelForm):
    choice = forms.ChoiceField()
    id = forms.IntegerField()

    class Meta:
        model = Answer
        fields = ('id', 'choice')

    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices', None)
        super(AnswerForm, self).__init__(*args, **kwargs)
        if choices:
            self.fields['choice'].choices = [(choice, choice) for choice in choices]
        else:
            self.fields['choice'] = forms.CharField(max_length=20)


class AnswerFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        self.questions = kwargs.pop('questions', None)
        super(AnswerFormSet, self).__init__(*args, **kwargs)

    @cached_property
    def forms(self):
        if self.questions:
            fs = [self._construct_form(i, **{'choices': question.alternatives})
                  for i, question in enumerate(self.questions)]
        else:
            fs = super(AnswerFormSet, self).forms()
        return fs


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ('word',)
