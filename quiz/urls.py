from django.urls import path

from quiz.save_load_quize import bulk_create_questions
from . import views

urlpatterns = [
    path('quiz/<int:code>', views.quiz, name='quiz'),
    path('addQuestion/<int:code>/<int:quiz_id>', views.addQuestion, name='addQuestion'),
    path('allQuizzes/<int:code>', views.allQuizzes, name='allQuizzes'),
    path('quizSummary/<int:code>/<int:quiz_id>', views.quizSummary, name='quizSummary'),
    path('myQuizzes/<int:code>', views.myQuizzes, name='myQuizzes'),
    path('startQuiz/<int:code>/<int:quiz_id>', views.startQuiz, name='startQuiz'),
    path('studentAnswer/<int:code>/<int:quiz_id>', views.studentAnswer, name='studentAnswer'),
    path('quizResult/<int:code>/<int:quiz_id>', views.quizResult, name='quizResult'),
    path('guest_myQuizzes/<int:code>', views.guest_myQuizzes, name='guest_myQuizzes'),
    path('guest_startQuiz/<int:code>/<int:quiz_id>', views.guest_startQuiz, name='guest_startQuiz'),
    path('questions/bulk-create', bulk_create_questions, name='bulk_create_questions'),


  
]