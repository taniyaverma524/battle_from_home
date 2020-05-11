from apps.users.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import serializers



class RegisterUserSerializer(serializers.ModelSerializer):


	class Meta:
		model=User
		fields=['email','first_name','last_name','password','mobile','gender','dob','account_number','ifsc_code','upi_id','paytm_number']
		# fields='__all__'
		# extra_kwargs = {'confirm_password'}
		required_fields=['email','first_name','last_name','password','mobile','gender','dob']

	def validate_password(self, data):
		confirm_password=self.context.get('confirm',None)
		if len(data) >= 8 and len(data) <= 15:
			if data!= confirm_password:
				raise serializers.ValidationError(" password is not matched with confirm password")
			data=make_password(data)
		else:
			raise serializers.ValidationError('new password must be between 8 to 15 characters long')
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
	def validate_paytm_number(self,value):
		if value:
			paytm_number=value
			if len(paytm_number) != 10:
				raise serializers.ValidationError('Paytm number must be 10 digit long ')
			elif not paytm_number.isdigit():
				raise serializers.ValidationError('Only digits are allowed for mobile')
			return paytm_number
		return value

	def validate_account_number(self,data):
		if data:
			confirm_account_number = self.context.get('confirm_account_number', None)
			if data != confirm_account_number:
				raise serializers.ValidationError(" account number is not matched with  account number")
			return data
		return data

	def validate_email(self, value):
		if not value:
			raise serializers.ValidationError('email is required field.')
		else:
			try:
				if not User.objects.filter(email=value).exists():
					return value.lower()
				else:
					raise serializers.ValidationError('email id is already registered.')
			except Exception as error:
				raise error
	def validate(self, data):
		email=data['email']
		data['username']=email.lower()
		return data

class UserUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model=User
		fields = ('id', 'email', 'first_name', 'last_name',
				  'is_active', 'is_staff', 'is_superuser', 'date_joined',)
		read_only_fields = ( 'date_joined',)




