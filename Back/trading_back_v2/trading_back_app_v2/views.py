from django.shortcuts import render
from django.http import JsonResponse
from django.core.management import call_command

def execute_run_back(request, interval):
    try:
        # Exécuter la commande avec l'intervalle donné
        call_command('run_back', interval)
        return JsonResponse({'status': 'success', 'message': f'Command run_back with interval {interval} executed successfully.'})
    except Exception as e:
        # Retourner une erreur en cas de problème
        return JsonResponse({'status': 'error', 'message': str(e)})
