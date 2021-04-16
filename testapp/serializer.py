from rest_framework import serializers
from .models import Employee

def name(value):
    if value== "venu":
        validated_data['ename'] = "venu gopal reddy"
    return value

class Eserializer(serializers.Serializer):
    eno = serializers.IntegerField()
    ename = serializers.CharField(max_length=20,validators=[name,])
    esal = serializers.FloatField()
    eadd = serializers.CharField(max_length=20)
    def create(self,validated_data):
        print(validated_data['ename'])
        return Employee.objects.create(**validated_data)
    def update(self,instance,validated_data):
        print("this is the validated_data",validated_data)
        instance.eno=validated_data.get('eno',instance.eno)
        instance.ename = validated_data.get('ename',instance.ename)
        instance.esal = validated_data.get('esal',instance.esal)
        instance.eadd = validated_data.get('eadd',instance.eadd)
        instance.save()
        return instance

    # def validate_esal(self,value):
    #     if value<5000:
    #         print("its in this block")
    #         raise serializers.ValidationError("plz enter atleast 5000")
    #     return value
    # def validate(self,data):
    #     ename=data.get('ename')
    #     esal = data.get('esal')
    #     if ename == "venu":
    #         if esal < 10000:
    #             raise serializers.ValidationError("venu should have more")
    #     else:
    #         return data
