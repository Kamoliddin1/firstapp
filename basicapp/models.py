from PIL import Image
from django.db import models
from django.contrib.auth.models import User, AbstractUser

from itertools import product

from django.utils import timezone


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    portfolio_site = models.URLField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_pics', default='default.jpg')

    def __str__(self):
        return self.user.username

    def correct_answers(self):
        return sum(list(map(lambda answer: answer.is_correct, self.user.answers.all())))

    def incorrect_answers(self):
        return self.user.answers.filter(session__finished_at__isnull=False).count() - self.correct_answers()
        # return sum(list(map(lambda answer: not answer.is_correct, self.user.answers.all())))

    def total_answers(self):
        return self.user.answers.all().count()


class TestSession(models.Model):
    no_of_questions = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    @property
    def questions(self):
        return list(map(lambda answer: answer.question, self.answers.all()))


class Question(models.Model):
    word = models.CharField(max_length=20)

    @property
    def alternatives(self):
        word = self.word
        result = []
        for index, letter in enumerate(word):
            if letter == 'h' and index == 0 or \
                    letter == 'h' and index != 0 and (word[index - 1] != 'c' and word[index - 1] != 's') or \
                    letter == 'x':
                result.append({'index': index, 'key': letter})

        perms = list(product('xh', repeat=len(result)))
        words = []
        for perm in perms:
            s = ""
            count = 0
            for row_index, row in enumerate(result):
                s += word[count:row['index']]
                s += perm[row_index]
                count = row['index'] + 1
            s += word[count:len(word)]
            words.append(s)
            words = sorted(words)
        return words

    def __str__(self):
        return self.word


class Answer(models.Model):
    user = models.ForeignKey(User, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    session = models.ForeignKey(TestSession, related_name='answers', on_delete=models.CASCADE)
    choice = models.CharField(max_length=20, null=True, default=None)

    @property
    def is_correct(self):
        if self.session.finished_at and self.session.finished_at < self.session.created_at + \
                        timezone.timedelta(seconds=self.session.no_of_questions * 10):
            if self.choice == self.question.word:
                return True
            return False
        return False
