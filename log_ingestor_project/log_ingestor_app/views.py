from django.shortcuts import render
from .models import Log
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone
import re
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import logging
from django.core.exceptions import ValidationError



# View to query logs based on filtering criteria
def query_logs(request):
    # Retrieve logs sorted by timestamp (most recent first)
    logs = Log.objects.all().order_by('-timestamp')

    # Retrieve query parameters from request (for filtering)
    level = request.GET.get('level')
    message = request.GET.get('message')
    resourceId = request.GET.get('resourceId')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    traceId = request.GET.get('traceId')
    spanId = request.GET.get('spanId')
    commit = request.GET.get('commit')
    parentResourceId = request.GET.get('metadata__parentResourceId')

    # Apply filters based on query parameters
    if level:
        logs = logs.filter(level=level)
    if message:
        try:
            logs = logs.filter(message__regex=message)
        except re.error:
            pass  # Handle invalid regex pattern

    if resourceId:
        logs = logs.filter(resourceId=resourceId)
    if start_date and end_date:
        logs = logs.filter(timestamp__range=(start_date, end_date))

    if traceId:
        logs = logs.filter(traceId=traceId)
    if spanId:
        logs = logs.filter(spanId=spanId)
    if commit:
        logs = logs.filter(commit=commit)
    if parentResourceId:
        logs = logs.filter(metadata__parentResourceId=parentResourceId)

    # Pagination
    paginator = Paginator(logs, 10)  # Display 10 logs per page
    page = request.GET.get('page')
    try:
        paginated_logs = paginator.page(page)
    except PageNotAnInteger:
        paginated_logs = paginator.page(1)
    except EmptyPage:
        paginated_logs = paginator.page(paginator.num_pages)

    context = {
        'logs': paginated_logs,
    }
    return render(request, 'query_logs.html', context)


# Logger for ingestion
logger = logging.getLogger('ingestion')

# View to ingest logs
@csrf_exempt
def ingest_log(request):
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            log = Log.objects.create(
                level=data.get('level'),
                message=data.get('message'),
                resourceId=data.get('resourceId'),
                timestamp=data.get('timestamp'),
                traceId=data.get('traceId'),
                spanId=data.get('spanId'),
                commit=data.get('commit'),
                parentResourceId=data['metadata'].get('parentResourceId')
            )
            
            logger.info('Log ingested successfully')  # Logging successful ingestion
            return JsonResponse({'message': 'Log ingested successfully'})
        except KeyError as e:
            logger.error(f'Missing key in log data: {str(e)}')  # Log specific error
            return JsonResponse({'message': f'Missing key in log data: {str(e)}'}, status=400)
        except ValueError as e:
            logger.error(f'Invalid value in log data: {str(e)}')  # Log specific error
            return JsonResponse({'message': f'Invalid value in log data: {str(e)}'}, status=400)
        except ValidationError as e:
            logger.error(f'Invalid log data format: {str(e)}')  # Log specific error
            return JsonResponse({'message': 'Invalid log data format'}, status=400)
        except Exception as e:
            logger.error(f'Error during ingestion: {str(e)}')  # Log general error
            return JsonResponse({'message': 'An error occurred while ingesting the log'}, status=500)
        
      


    else:
        return JsonResponse({'message': 'Only POST requests are allowed'}, status=405)


# Temporary view for testing
def temporary(request):
    return HttpResponse("Hello World")
