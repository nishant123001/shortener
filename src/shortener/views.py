from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from shortener import controller
from shortener import exceptions

@csrf_exempt
def create_short(request):
	if request.method == "GET":
		return HttpResponse(status=405)

	url = request.POST.get('url')
	if not url:
		HttpResponse(status=400)

	shortner_ctrl = controller.Shortner()
	shortner_code = None
	try:
		shortner_code = shortner_ctrl.get_code(url)
	except exceptions.ServerError as err:
		return HttpResponse(status=500)
	return JsonResponse({"code": shortner_code})

def go(request, code):
	if request.method == "POST":
		return HttpResponse(status=405)

	shortner_ctrl = controller.Shortner()
	url = shortner_ctrl.get_url(code)
	if url is None:
		return HttpResponse(status=404)
	return JsonResponse({"url": url})
