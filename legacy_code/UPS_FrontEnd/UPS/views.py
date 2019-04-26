# Create your views here.
from django.http import HttpResponse
from UPS.models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
'''
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
'''

from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import PIDForm
import pdb
@login_required
def index(request):
        # if this is a POST request we need to process the form data
        user = request.user
        packages = user.package_set.all()
        if request.method == 'POST':
                # create a form instance and populate it with data from the request:
                form = PIDForm(request.POST)
                # check whether it's valid:
                if form.is_valid():
                        #pdb.set_trace()
                        # process the data in form.cleaned_data as required
                        # ...
                        # redirect to a new URL:
                        packages = user.package_set.filter(packageid = form.cleaned_data['pid'])
                        products = [p.product_set.all() for p in packages]
                        # package_set = lambda truck : str([p.packageid for p in truck.package_set.all()])
                        output = request.user.username + '<br>'
                        #output += '<br>'.join(["truck_id : {} | status : {} | packages : {}".format(t.truck_id,t.status,package_set(t)) for t in trucks])
                        output += "<br><br>".join([pack.__str__() for pack in packages])
                        return render(request, 'home.html', {'form': form, 'output' : output})
                        return HttpResponseRedirect('/UPS/')
                # if a GET (or any other method) we'll create a blank form
        else:
                products = [p.product_set.all() for p in packages]
                # package_set = lambda truck : str([p.packageid for p in truck.package_set.all()])
                output = request.user.username + '<br>'
                #output += '<br>'.join(["truck_id : {} | status : {} | packages : {}".format(t.truck_id,t.status,package_set(t)) for t in trucks])
                output += "<br><br>".join([pack.__str__() for pack in request.user.package_set.order_by('packageid')])
                form = PIDForm()
        return render(request, 'home.html', {'form': form, 'output' : output})


from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

class SignUp(generic.CreateView):
        form_class = UserCreationForm
        success_url = reverse_lazy('login')
        template_name = 'signup.html'
