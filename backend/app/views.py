from django.shortcuts import render,HttpResponse,JsonResponse



def health_check(request):
    return HttpResponse('all okay')



def get_student_info(request):
    return JsonResponse({'name': 'John Doe', 'age': 21})    
# Create your views here.
