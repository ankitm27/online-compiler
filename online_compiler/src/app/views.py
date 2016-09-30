from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password, make_password
from app.serializers import RegisterSerializer, LoginSerializer, ProfileSerializer, ChangePasswordSerializer, ContactSerializer, ForgetPasswordSerializer
import os

"""class Home(APIView):
	renderer_classes = [TemplateHTMLRenderer]
	template_name = 'home.html'

	def get(self,request,format=None):		
		user = request.user
		return Response({user:user})

	def post(self,request,format = None):
		data = request.data['code']
		domain = request.data['domain']
		ext = '.' + domain.split('|')[1]
		filename = str(request.user) + ext
		path="/tmp/upload"
		complete_path = os.path.join(path,filename)
		file_pointer = open(complete_path,"w")
		file_pointer.write(data)
		file_pointer.close()
		# # ftp upload
		# session=ftplib.FTP('127.0.0.1','userftp','ankit')
		# file = open(complete_path,'rb')
		# session.cwd("upload")
		# session.storbinary('STOR '+ filename,file)
		# file.close()
		# session.quit()
		# # ftp download
		# while True:
		# 	try:
		# 		ftp=ftplib.FTP('127.0.0.1')
		# 		ftp.login("userftp","ankit")
		# 		ftp.cwd('upload')        
		# 		ftp.retrbinary('RETR ' + filename,open('/tmp/download/' + filename,'wb').write)
		# 		ftp.quit()
		# 		file_pointer = open(complete_path,"rb")
		# 		output_data = file_pointer.read()                            
		# 		break
		# 	except:
		# 		time.sleep(0.50)
		return Response({'code':data,'ext':domain.split('|')[1]})
"""
class Home(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'home.html'
    def get(self,request,format=None):
		user = request.user
		return Response({user:user})

    def post(self,request,format = None):
		data = request.data['code']
		input_data = request.data['input_code']
		domain = request.data['domain']
		ext = '.' + domain.split('|')[1]
		path="/tmp/upload"
		input_fileext = '.input'
		filename = str(request.user) + ext
		input_filename=str(request.user) + input_fileext 
		complete_path = os.path.join(path,filename)   
		complete_inputpath = os.path.join(path,input_filename)
		file_pointer = open(complete_path,"w")
		file_pointer.write(data)
		file_pointer.close()
		file_inputpointer = open(complete_inputpath,"w")
		file_inputpointer.write(input_data)
		file_inputpointer.close()
		# #ftp upload
		# session=ftplib.FTP('127.0.0.1','userftp','ankit')
		# file = open(complete_path,'rb')
		# session.cwd("upload")
		# session.storbinary('STOR '+ filename,file)
		# file.close()
		# file = open(complete_inputpath,'rb')
		# session.storbinary('STOR '+ input_filename,file)
		# file.close()
		# session.quit()
		# #ftp download
		# ftp=ftplib.FTP('127.0.0.1')
		# ftp.login("userftp","ankit")
		# ftp.cwd('upload')
		# while True:
		# try:
		#     ftp.retrbinary('RETR ' + filename,open('/tmp/download/' + filename,'wb').write)
		#         file_pointer = open(complete_path,"rb")
		#         output_data = file_pointer.read()                            
		#         break
		#     except:
		#         time.sleep(0.50)
		# #ftp file deletion
		# ftp.delete(filename)
		# ftp.delete(input_filename)
		# ftp.cwd('/home/FTP-shared/download')
		# output_fileext = '.output'
		# output_filename = str(request.user) + output_fileext
		# #ftp.delete(output_filename)
		# ftp.quit()
		# #tmp file delete
		# os.remove(complete_path)
		# os.remove(complete_inputpath)
		# os.remove('/tmp/download/'+filename)
		return Response({'code':data,'output_code':output_data,'input_code':input_data,'ext':domain.split("|")[1]})
class Register(APIView):
	renderer_classes = [TemplateHTMLRenderer]
	template_name = 'register.html'

	def get(self, request, format=None):
		if request.user.is_authenticated():
			return redirect('home')
		else:
			serializer = RegisterSerializer()
			return Response({'serializer':serializer,'title':'Register'})

	def post(self, request, format=None):
		username = request.data['username']
		if User.objects.filter(username=username).count():
			serializer = RegisterSerializer()
			error = "username '"+ username +"' already exist."
			return Response({'serializer':serializer,'error':error,'title':'Register'})
		else:
			serializer = RegisterSerializer(data=request.data)
			if not serializer.is_valid():
				return Response({'serializer':serializer, 'title':'Register'})
			serializer.save()
			return redirect('home')


class Login(APIView):
	renderer_classes = [TemplateHTMLRenderer]
	template_name = 'login.html'

	def get(self, request, format=None):
		if request.user.is_authenticated():
			return redirect('home')
		else:
			serializer = LoginSerializer()
			send = {'serializer':serializer,'title':'Login'}
			send.update(csrf(request))
			return Response(send)

	def post(self, request, format=None):
		username = request.data.get('username', '')
		password = request.data.get('password', '')
		user = auth.authenticate(username=username, password=password)
		if user is not None:
			auth.login(request, user)
			return redirect('home')
		else:
			serializer = LoginSerializer(data=request.data)
			if not serializer.is_valid():
				return Response({'serializer':serializer,'title':'Login'})
			send = {'serializer':serializer,'error':'username or password is incorrect.','title':'Login'}
			send.update(csrf(request))
			return Response(send)

class Profile(APIView):
	renderer_classes = [TemplateHTMLRenderer]
	template_name = 'profile.html'

	def get_objects(self, pk):
		try:
			return User.objects.get(id=pk)
		except User.DoesNotExist:
			raise Http404

	def get(self, request, format=None):
		if request.user.is_authenticated():
			user = self.get_objects(request.user.id)
			serializer = ProfileSerializer(user)
			return Response({'serializer':serializer, 'user':user, 'title': 'Profile'})
		else:
			return redirect('home')

	def post(self, request, format=None):
		user = self.get_objects(request.user.id)
		serializer = ProfileSerializer(user, data=request.data)
		if not serializer.is_valid():
			return Response({'serializer':serializer, 'user':user, 'title': 'Profile'})
		serializer.save()
		user = self.get_objects(request.user.id)
		serializer = ProfileSerializer(user)
		return Response({'serializer':serializer, 'user':user, 'title': 'Profile'})

class ChangePassword(APIView):
	renderer_classes = [TemplateHTMLRenderer]
	template_name = 'change_password.html'

	def get(self, request, format=None):
		if request.user.is_authenticated():
			serializer = ChangePasswordSerializer
			return Response({'serializer':serializer,'title':'Change Password'})
		else:
			return redirect('home')

	def post(self, request, format=None):
		serializer = ChangePasswordSerializer
		if not serializer.is_valid():
			return Response({'serializer':serializer,'title':'Change Password'})
		current_password = request.data['current_password']
		new_password = request.data['new_password']
		hash_password = User.objects.filter(username=request.user).values()[0].get('password')
		if check_password(current_password, hash_password):
			serializer = ChangePasswordSerializer
			user = User.objects.get(username__exact=request.user)
			user.set_password(new_password)
			user.save()
			return redirect('home')
		else:
			error = "You entered wrong password."
			serializer = ChangePasswordSerializer
			return Response({'serializer':serializer,'error':error,'title':'Change Password'})

class Logout(APIView):
	renderer_classes = [TemplateHTMLRenderer]
	template_name = 'logout.html'

	def get(self, request, format=None):
		if request.user.is_authenticated():
			auth.logout(request)
			return redirect ('home')
		else:
			return redirect('home')

class Contact(APIView):
	renderer_classes = [TemplateHTMLRenderer]
	template_name = 'contact.html'

	def get(self, request, format=None):
		serializer = ContactSerializer
		return Response({'serializer':serializer,'title':'Contact'})

	def post(self, request, format=None):
		serializer = ContactSerializer(data=request.data)
		if not serializer.is_valid():
			return Response({'serializer':serializer,'title':'Contact'})
		subject = "Customer queries"
		from_email = "shubham199541@gmail.com"
		to_email = "shubham.agrawal1906@gmail.com"
		name = request.data['name']
		email = request.data['email']
		# message = request.data['message']
		body = "Name: "+name+"\n"+"From: "+email+"\n"+"Meassage: "+message
		send_mail(subject,body,from_email,[to_email],fail_silently=True)
		serializer = ContactSerializer
		return Response({'serializer':serializer,'title':'Contact'})


class About(APIView):
	renderer_classes = [TemplateHTMLRenderer]
	template_name = 'about.html'

	def get(self, request, format=None):
		return Response({'title':'About'})

class ForgetPassword(APIView):
	renderer_classes = [TemplateHTMLRenderer]
	template_name = 'forget_password.html'

	def get(self, request, format=None):
		if not request.user.is_authenticated():
			serializer = ForgetPasswordSerializer
			return Response({'serializer':serializer,'title':'Forget Password'})
		else:
			return redirect('home')

	def post(self, request, format=None):
		username = request.data['username']
		if User.objects.filter(username=username).count():
			email = User.objects.filter(username=username).values()[0].get('email')
			from_email = "shubham199541@gmail.com"
			to_email = email
			message = "Your new password is "
			body = "Hello "+username+"\n"+message
			send_mail(subject,body,from_email,[to_email],fail_silently=True)
			return redirect('home')
		else:
			serializer = ForgetPasswordSerializer
			error = "username '"+ username +"' not registered."
			return Response({'serializer':serializer,'error':error,'title':'Forget Password'})
