from django.shortcuts import render
from .models import Employee
from .serializer import Eserializer
from django.views.generic import View
from django.http import HttpResponse,JsonResponse
import io
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt,name='dispatch')
class Home(View):
    def get(self,r,*args,**kwargs):
        try:
            data = r.body
            # this in the json format
            stream = io.BytesIO(data)
            p_d=JSONParser().parse(stream)
            # python data
            id = p_d.get('id')
        except:
            id=None
        finally:
            if id is None:
                obj = Employee.objects.all()
                # now we have to convert this to python data and then to python using serializer
                s = Eserializer(obj,many=True)
                # now we have serializer.data which is in the python format and now we have to convert this to json using renderer
                j_data=JSONRenderer().render(s.data)
            else:
                try:
                    obj = Employee.objects.get(id=id)
                    s=Eserializer(obj,many=False)
                    j_data = JSONRenderer().render(s.data)
                except Exception as e:
                    j_data="something went wrong"
                    return JsonResponse(j_data,safe=False)
        return HttpResponse(j_data,content_type='application/json')
    def post(self,r,*args,**kwargs):
        # we have to get the data from the partner application
        data = r.body # this will be in the json format we have to convert this to python and access the data
        stream = io.BytesIO(data) # this is in the object form we have to convet this to python
        p_data=JSONParser().parse(stream)
        # now this is in the python format from here we can get the p_data
        # since we have python data we cannot create object directly with so we to convert this into model type for that we deserialize
        s = Eserializer(data=p_data)
        # we can get the validated data
        if s.is_valid():
            print(s.validated_data)
            s.save()
        else:
            print(s.errors)
            return HttpResponse(JSONRenderer().render(s.errors),content_type='application/json')
        return JsonResponse("done ",safe=False)

    def put(self,r,*args,**kwargs):
        data = r.body
        # print(data)
        # now this is in the form of json
        stream = io.BytesIO(data)
        # now we have obj from here we can getour python data
        p_data=JSONParser().parse(stream)
        # now this is in the form of python we get  the id from here and then we update
        id = p_data.get('id')
        # we now have id
        obj = Employee.objects.get(id=id)
        ds = Eserializer(obj,data=p_data)
        # we hvae model data in the form of ds.validated_data
        if ds.is_valid():
            ds.save(instance=id)
            print("its valid")
        else:
            print(ds.errors)
            return JsonResponse(ds.errors)

        return JsonResponse("this is from the put method",safe=False)

# Create your views here.
