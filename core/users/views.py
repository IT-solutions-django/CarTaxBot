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
    ClientCalculation,
)
from notifications.services import send_telegram_message_for_all


@method_decorator(csrf_exempt, name='dispatch')
class CreateClientView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            telegram_id = data.get('telegram_id')

            if not telegram_id:
                return JsonResponse({'error': 'Укажите telegram_id'}, status=400)
            
            status = ClientStatus.get_start_status()
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
            
            client = Client.objects.get(telegram_id=telegram_id) 
            client.name = name
            client.phone = phone 
            client.save()

            feedback_request = FeedbackRequest.objects.create(
                client=client,
                name=name,
                phone=phone
            )

            send_telegram_message_for_all(
                'Новая заявка из Telegram-бота:\n'
                f'Имя: {name}\n'
                f'Телефон: {phone}\n'
            )
            
            return JsonResponse({'message': 'Контактные данные клиента успешно добавлены', 'client_id': client.id}, status=201)
        
        except json.JSONDecodeError as e:
            print(str(e))
            return JsonResponse({'error': 'Некорректный JSON'}, status=400)
        except Exception as e:
            print(str(e))
            return JsonResponse({'error': str(e)}, status=500)
        

@method_decorator(csrf_exempt, name='dispatch')
class AddClientCalculationView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            telegram_id = data.get('telegram_id')
            price = data.get('price')
            age = data.get('age')
            volume = data.get('engine_volume')
            currency = data.get('currency')
            engine_type = data.get('engine_type')
            car_type = data.get('car_type') 
            power_kw = data.get('power_kw')

            if not telegram_id:
                return JsonResponse({'error': 'Укажите telegram_id'}, status=400)
            if not price:
                return JsonResponse({'error': 'Укажите price'}, status=400)
            if not age:
                return JsonResponse({'error': 'Укажите age'}, status=400)
            if not volume:
                return JsonResponse({'error': 'Укажите engine_volume'}, status=400)
            if not currency:
                return JsonResponse({'error': 'Укажите currency'}, status=400)
            if not engine_type:
                return JsonResponse({'error': 'Укажите engine_type'}, status=400)
            if not car_type:
                return JsonResponse({'error': 'Укажите car_type'}, status=400)

            client = Client.objects.filter(telegram_id=telegram_id).first()
            if not client:
                return JsonResponse({'error': 'Клиент с таким telegram_id не найден'}, status=404)
            client.status = ClientStatus.get_calc_status()
            client.save()

            calculation = ClientCalculation.objects.create(
                client=client,
                price=price,
                age=age,
                volume=volume,
                currency=currency,
                engine_type=engine_type, 
                car_type=car_type, 
                power_kw=power_kw
            )

            return JsonResponse({'message': 'Расчёт успешно добавлен', 'calculation_id': calculation.id}, status=201)

        except json.JSONDecodeError as e:
            print(str(e))
            return JsonResponse({'error': 'Некорректный JSON'}, status=400)
        except Exception as e:
            print(str(e))
            return JsonResponse({'error': str(e)}, status=500)