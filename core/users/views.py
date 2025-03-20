import json
from django.shortcuts import render
from django.views import View 
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Client, ClientStatus


@method_decorator(csrf_exempt, name='dispatch')
class CreateClientView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            telegram_id = data.get('telegram_id')
            name = data.get('name', '')
            phone = data.get('phone', '')

            if not telegram_id:
                return JsonResponse({'error': 'Укажите telegram_id'}, status=400)
            
            status = ClientStatus.get_primary_contact_status()
            client, created = Client.objects.get_or_create(
                telegram_id=telegram_id,
                defaults={
                    'name': name, 
                    'phone': phone, 
                    'status': status,
                }
            )

            if not created:
                return JsonResponse({'error': 'Клиент с таким Telegram ID уже существует'}, status=400)
            
            return JsonResponse({'message': 'Клиент успешно добавлен', 'client_id': client.id}, status=201)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Некорректный JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
