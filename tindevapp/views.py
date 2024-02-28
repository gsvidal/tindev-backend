from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from django.db import IntegrityError
from .models import User, Dev, Recruiter
from django.contrib.auth import login, logout
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def index(request):
  return HttpResponse('Hello tindev')

# @csrf_exempt
def register(request):
  if request.method == "POST":
    # Validate fields
    data = json.loads(request.body)

    first_name = data.get("firstName")
    if first_name.strip() == "":
      return JsonResponse({'error': "First name can't be empty"}, status=400)

    last_name = data.get("lastName")
    if last_name.strip() == "":
      return JsonResponse({'error': "Last name can't be empty"}, status=400)

    email = data.get("email")
    if email.strip() == "":
      return JsonResponse({'error': "Email can't be empty"}, status=400)

    password = data.get("password")
    if len(password) < 6:
      return JsonResponse({'error': "Password length must be greater than or equal to 6"}, status=400)

    confirm_password = data.get("confirmPassword")
    if confirm_password != password:
      return JsonResponse({'error': "Passwords must match"}, status=400)

    role = data.get("role")
    if role != "Dev" and role != "Recruiter" :
      return JsonResponse({'error': "This role doesn't exist"}, status=400)

    try:
      user = User.objects.create_user(username=email, email=email, password=password, first_name=first_name, last_name=last_name) 
      user.role = role
      user.save()

      if role == "Dev":
        Dev.objects.create(user=user)

      elif role == "Recruiter":
        isIndependent = data.get("isIndependent")
        company_name = data.get("companyName")

        recruiter = Recruiter.objects.create(user=user)
        recruiter.isIndependent = isIndependent
        recruiter.company_name = company_name
        recruiter.save()

    except IntegrityError as e:
      if "unique constraint" in str(e).lower():
        return JsonResponse({"error": "A user is already created with this email."}, status=400)
      else:
        # Handle other integrity errors
        return JsonResponse(
            {"error": "An error occurred while creating the user."}, status=400
        )
        
    # token 
    token = Token.objects.create(user=user)

    # login
    login(request, user)

    response_data = {
      'message': 'User registered successfully',
      'user': {
          'id': user.id,
          'first_name': user.first_name,
          'last_name': user.last_name,
          'email': user.email,
          'role': user.role,
      },
      'token': token.key
    }

    if user.role == 'recruiter':
        response_data['user']['is_independent'] = user.is_independent
        response_data['user']['company_name'] = user.company_name

    return JsonResponse(response_data)

  else:
    return JsonResponse({'error': 'Invalid method'}, status=405)