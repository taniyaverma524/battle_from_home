from apps.users.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import serializers



class RegisterUserSerializer(serializers.ModelSerializer):
	# import ipdb;ipdb.set_trace()

	class Meta:
		model=User
		fields=['email','first_name','last_name','password','mobile','gender','dob','profile_picture']
		# fields='__all__'
		# extra_kwargs = {'confirm_password'}

	def validate_password(self, data):
		confirm_password=self.context.get('confirm',None)
		if data!= confirm_password:
			raise serializers.ValidationError(" password is not matched with confirm password")
		data=make_password(data)
		return data
	def validate_mobile(self,data):
		mobile=data
		if not mobile:
			raise serializers.ValidationError('Mobile no is required.')
		elif len(mobile) != 10:
			raise serializers.ValidationError('Mobile must be 10 digit long ')
		elif not mobile.isdigit():
			raise serializers.ValidationError('Only digits are allowed for mobile')
		elif mobile:
			try:
				if not User.objects.filter(mobile=mobile).exists():
					return mobile
				else:
					raise serializers.ValidationError('mobile is already registered.')
			except Exception as error:
				raise error


	def validate_email(self, value):
		if not value:
			raise serializers.ValidationError('email is required field.')
		else:
			try:
				if not User.objects.filter(email=value).exists():
					return value
				else:
					raise serializers.ValidationError('email id is already registered.')
			except Exception as error:
				raise error
	def validate(self, data):
		email=data['email']
		data['username']=email
		return data

class UserUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model=User
		fields='__all__'
