import base64
import re
from venv import create
from django.db import models
from main.models import Student, Course


# Create your models here.


class Quiz(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    publish_status = models.BooleanField(default=False, null=True, blank=True)
    started = models.BooleanField(default=False, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Quizzes"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def duration(self):
        return self.end - self.start
        
    def duration_in_seconds(self):
        return (self.end - self.start).total_seconds()

    def total_questions(self):
        return Question.objects.filter(quiz=self).count()

    def question_sl(self):
        return Question.objects.filter(quiz=self).count() + 1

    def total_marks(self):
        return Question.objects.filter(quiz=self).aggregate(total_marks=models.Sum('marks'))['total_marks']

    def starts(self):
        return self.start.strftime("%a, %d-%b-%y at %I:%M %p")

    def ends(self):
        return self.end.strftime("%a, %d-%b-%y at %I:%M %p")

    def attempted_students(self):
        return Student.objects.filter(studentanswer__quiz=self).distinct().count()


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.TextField()
    marks = models.IntegerField(default=0, null=False)
    option1 = models.TextField(null=False, blank=False, default='',)
    option2 = models.TextField(null=False, blank=False, default='')
    option3 = models.TextField(null=False, blank=False, default='')
    option4 = models.TextField(null=False, blank=False, default='')
    answer = models.CharField(max_length=1, choices=(
        ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')), default='A')
    explanation = models.TextField(null=True, blank=True)
    difficulty = models.CharField(max_length=20, choices=[('easy', 'Easy'), ('moderate', 'Moderate'), ('hard','Hard')], default='hard')
    #for storing html content
    html_option1 = models.TextField(null=True, blank=True)
    html_option2 = models.TextField(null=True, blank=True)
    html_option3 = models.TextField(null=True, blank=True)
    html_option4 = models.TextField(null=True, blank=True)
    html_explanation = models.TextField(null=True, blank=True)
    status = models.IntegerField(choices=[
        (1, 'Active'),(2, 'Inactive'),(3, 'Deleted')], default=1)
    created_date = models.DateTimeField(auto_now_add=True)  # set once at creation
    updated_date = models.DateTimeField(auto_now=True)      # updated every save

    def __str__(self):
        return self.question

    def get_answer(self):
        case = {
            'A': self.option1,
            'B': self.option2,
            'C': self.option3,
            'D': self.option4,
        }
        return case[self.answer]

    def total_correct_answers(self):
        return StudentAnswer.objects.filter(question=self, answer=self.answer).count()

    def total_wrong_answers(self):
        return StudentAnswer.objects.filter(question=self).exclude(answer=self.answer).count()

    def decode_html(self, html_value):
        if html_value:
            html_text = base64.b64decode(html_value).decode('utf-8')
            html_text=  html_text.replace('src="/_files', 'src="https://www.indiabix.com/_files')
            html_text= re.sub(r'<p class="mx-bold mx-green">Video Explanation: <a href="https:\/\/youtu\.be\/[^"]+" target="_blank">[^<]+<\/a><\/p>', '', html_text)
            return html_text
        return ''

    @property
    def html_decoded(self):
        return self.decode_html(self.html_explanation)

class StudentAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=1, choices=(
        ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')), default='', null=True, blank=True)
    marks = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.student.name + ' ' + self.quiz.title + ' ' + self.question.question

    class Meta:
        unique_together = ('student', 'quiz', 'question')
