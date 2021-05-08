from django.shortcuts import render

# Create your views here.
import logging

logger = logging.getLogger(__name__)

# Error 
def page_not_found_view(request, exception, template_name='error/error_page.html'):
    if exception:
        logger.error(exception)
    url = request.get_full_path()
    return render(request, template_name,
                  {'message': 'Vaya, la dirección ' + url + ' que visitaste es un lugar desconocido.', 'statuscode': '404'}, status=404)


def server_error_view(request, template_name='error/error_page.html'):
    return render(request, template_name,
                  {'message': 'Vaya, algo salió mal, he recopilado la información incorrecta y me apresuraré a repararla más tarde.', 'statuscode': '500'}, status=500)


def permission_denied_view(request, exception, template_name='error/error_page.html'):
    if exception:
        logger.error(exception)
    return render(request, template_name,
                  {'message': 'Vaya, no tienes permiso para acceder a esta página.', 'statuscode': '403'}, status=403)
