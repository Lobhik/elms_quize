from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Question, Quiz

@csrf_exempt
def bulk_create_questions(request):
    if request.method == 'POST':

        #return JsonResponse({'msg':'request comming url.'})
        try:
            data = json.loads(request.body)
            
            quiz_instance = Quiz.objects.get(id=2)

            questions = [
                Question(
                    quiz = quiz_instance,
                    question=item['question_text'],
                    option1=item['option_a'],
                    option2=item['option_b'],
                    option3=item['option_c'],
                    option4=item['option_d'],
                    answer=item['correct_option'],
                    explanation=item['explanation'],
                    difficulty=item['difficulty']
                )
                for item in data
            ]

            Question.objects.bulk_create(questions)
            return JsonResponse({'message': f'{len(questions)} questions added successfully'}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Only POST method allowed'}, status=405)


