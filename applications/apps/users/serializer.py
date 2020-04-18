from apps.users.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import serializers



class RegisterUserSerializer(serializers.ModelSerializer):
	# import ipdb;ipdb.set_trace()

	class Meta:
		model=User
		fields=['username','email','first_name','last_name','password','mobile','gender','dob','profile_picture']
		# fields='__all__'
		# extra_kwargs = {'confirm_password'}
	def validate(self, data):
		confirm_password=self.context.get('confirm',None)
		if data['password']!= confirm_password:
			raise serializers.ValidationError(" password is not matched with confirm password")
		data['password']=make_password(data['password'])
		return data





class UserUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model=User
		fields='__all__'
