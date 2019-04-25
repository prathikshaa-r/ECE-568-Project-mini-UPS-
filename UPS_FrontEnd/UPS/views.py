# Create your views here.
from django.http import HttpResponse
from UPS.models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def index(request):
        trucks = Truck.objects.order_by("truck_id")
        user = request.user
        packages = user.package_set.all()
        products = [p.product_set.all() for p in packages]
         # package_set = lambda truck : str([p.packageid for p in truck.package_set.all()])
        output = request.user.username + '<br>'
        #output += '<br>'.join(["truck_id : {} | status : {} | packages : {}".format(t.truck_id,t.status,package_set(t)) for t in trucks])
        output += "<br><br>".join([pack.__str__() for pack in request.user.package_set.order_by('packageid')])
        return render(request, 'home.html',{'output' : output})
        return HttpResponse(output)
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import NameForm

def get_name(request):
        # if this is a POST request we need to process the form data
        if request.method == 'POST':
                # create a form instance and populate it with data from the request:
                form = NameForm(request.POST)
                # check whether it's valid:
                if form.is_valid():
                        # process the data in form.cleaned_data as required
                        # ...
                        # redirect to a new URL:
                        return HttpResponseRedirect('/thanks/')
                # if a GET (or any other method) we'll create a blank form
                else:
                        form = NameForm()
                        return render(request, 'name.html', {'form': form})


