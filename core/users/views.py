import json
from django.shortcuts import render
from django.views import View 
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import (
    Client, 
    ClientStatus, 
    FeedbackRequest, 
)


@method_decorator(csrf_exempt, name='dispatch')
class CreateClientView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            telegram_id = data.get('telegram_id')

            if not telegram_id:
                return JsonResponse({'error': 'Укажите telegram_id'}, status=400)
            
            status = ClientStatus.get_primary_contact_status()
            client, created = Client.objects.get_or_create(
                telegram_id=telegram_id,
                defaults={
                    'status': status,
                }
            )

            if not created:
                return JsonResponse({'message': 'Клиент с таким Telegram ID уже существует', 'client_id': client.id}, status=200)
            
            return JsonResponse({'message': 'Клиент успешно добавлен', 'client_id': client.id}, status=201)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Некорректный JSON'}, status=400)
        except Exception as e:
            print(str(e))
            return JsonResponse({'error': str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class SetContactDataView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            telegram_id = data.get('telegram_id')
            name = data.get('name')
            phone = data.get('phone')

            print(telegram_id, name, phone)

            if not name:
                return JsonResponse({'error': 'Укажите name'}, status=400)
            if not phone:
                return JsonResponse({'error': 'Укажите phone'}, status=400)
            
            status = ClientStatus.get_left_contacts_status()
            client = Client.objects.get(telegram_id=telegram_id) 
            client.name = name
            client.phone = phone 
            client.status = status 
            client.save()

            feedback_request = FeedbackRequest.objects.create(
                client=client,
                name=name,
                phone=phone
            )
            
            return JsonResponse({'message': 'Контактные данные клиента успешно добавлены', 'client_id': client.id}, status=201)
        
        except json.JSONDecodeError as e:
            print(str(e))
            return JsonResponse({'error': 'Некорректный JSON'}, status=400)
        except Exception as e:
            print(str(e))
            return JsonResponse({'error': str(e)}, status=500)