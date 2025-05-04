

import os
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from eLMS import settings
from .models import Question, Quiz

# @csrf_exempt
# def bulk_create_questions(request):
#     if request.method == 'POST':

#         #return JsonResponse({'msg':'request comming url.'})
#         try:
#             data = json.loads(request.body)
            
#             quiz_instance = Quiz.objects.get(id=2)

#             questions = [
#                 Question(
#                     quiz = quiz_instance,
#                     question=item['question_text'],
#                     option1=item['option_a'],
#                     option2=item['option_b'],
#                     option3=item['option_c'],
#                     option4=item['option_d'],
#                     answer=item['correct_option'],
#                     explanation=item['explanation'],
#                     difficulty=item['difficulty']
#                 )
#                 for item in data
#             ]

#             Question.objects.bulk_create(questions)
#             return JsonResponse({'message': f'{len(questions)} questions added successfully'}, status=201)

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)

#     return JsonResponse({'error': 'Only POST method allowed'}, status=405)













from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Question, Quiz
from main.models import Course



def create_quize(postdata):
    try:
        course_instance = Course.objects.get(id=2)
        print(course_instance)
        courses = []
        quize_obj = Quiz(
            course = course_instance,
            # title = 
        )
    except Exception as e:
        return False
    



@csrf_exempt
def bulk_create_questions(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)


            folder_path = os.path.join(settings.BASE_DIR, 'questions_folder')  # Adjust as needed

            total_created = 0
            failed_files = []

            for filename in os.listdir(folder_path):
                if not filename.endswith('.json'):
                    continue

                quiz_file_name = os.path.splitext(filename)[0]  # Assume filename is quiz ID like "17.json"
                quiz_id = quiz_file_name.split('_')[-1]  # Extract quiz ID from filename
                try:
                    quiz = Quiz.objects.get(id=quiz_id)
                except Quiz.DoesNotExist:
                    failed_files.append(filename)
                    continue

                with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as f:
                    try:
                        data = json.load(f)
                    except json.JSONDecodeError:
                        failed_files.append(filename)
                        continue

                ####
                quiz_instance = Quiz.objects.get(id=quiz_id)  # or get quiz ID dynamically

                print(quiz_instance)
                #exit()
                questions = []
                for item in data:
                    options = item.get("options", [])

                    # Ensure all 4 options are present
                    if len(options) != 4:
                        print("Q.",item.get('question',''))
                        # print(options)
                        if len(options) < 4:
                            return JsonResponse({'error': 'Each question must have exactly 4 options.'}, status=400)

                    question_obj = Question(
                        quiz=quiz_instance,
                        question=item.get('question'),
                        option1=options[0].get('option_text', ''),
                        option2=options[1].get('option_text', ''),
                        option3=options[2].get('option_text', ''),
                        option4=options[3].get('option_text', ''),
                        html_option1=options[0].get('option_html', ''),
                        html_option2=options[1].get('option_html', ''),
                        html_option3=options[2].get('option_html', ''),
                        html_option4=options[3].get('option_html', ''),
                        answer=item.get('answer', 'A'),
                        explanation=None,  # Plain text explanation (not available in input)
                        html_explanation=item.get('html_desc_answer', ''),
                        difficulty=item.get('difficulty', 'moderate')  # Default to easy if not specified
                    )

                    questions.append(question_obj)

                Question.objects.bulk_create(questions)

            return JsonResponse({'message': f'{len(questions)} questions added successfully'}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Only POST method allowed'}, status=405)
