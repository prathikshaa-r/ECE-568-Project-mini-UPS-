# Create your views here.
from django.http import HttpResponse
from UPS.models import *

def index(request):
        trucks = Truck.objects.order_by("truck_id")
        package_set = lambda truck : str([p.packageid for p in truck.package_set.all()])
        output = '<br>'.join(["truck_id : {} | status : {} | packages : {}".format(t.truck_id,t.status,package_set(t)) for t in trucks])
        return HttpResponse(output)



