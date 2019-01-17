from django.shortcuts import render
from django.http import HttpResponse
import pyrebase
from django.contrib import messages
import csv

#Package for model

from statsmodels.tsa.arima_model import ARIMA,ARIMAResults
from scipy.stats import boxcox
import numpy
from sklearn.metrics import mean_squared_error
from math import sqrt

from matplotlib import pyplot

import pandas
from pandas import Series

from matplotlib import pyplot
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter
import io

# installed pillow but for old compatibility they use PIL only
import PIL
import PIL.Image

import base64

# connecting to firebase

#configuration setting 
config = {
    "apiKey": "AIzaSyDJQ46f0iVp_ldrx5Y_AgZ5HWtyI9dfYd8",
    "authDomain": "lbswater.firebaseapp.com",
    "databaseURL": "https://lbswater.firebaseio.com",
    "projectId": "lbswater",
    "storageBucket": "lbswater.appspot.com",
    "messagingSenderId": "1065042380223"
  };

firebase = pyrebase.initialize_app(config);
db = firebase.database()

#Rendering Home Page
def index(request):
	return render(request,'index.html')

# Registeration storing data in firebase
def signup(request):

	if request.method == "POST":
		name = request.POST.get('username')
		email = request.POST.get('email')
		phone = request.POST.get('phone')
		address = request.POST.get('address')
		country = request.POST.get('country')
		city = request.POST.get('city')
		state = request.POST.get('state')
		pincode = request.POST.get('pincode')
		password = request.POST.get('password')
		sensor = request.POST.get('sensor')
		#getting db instance
		uniqueid = "1000"+pincode+sensor
		#endid = endid+1
		print(uniqueid)
		print(name)
		print(email)

		data = {"name": name , "email": email,"phoneNo":phone,"address":address,
		"country":country,"city":city,"state":state,"pincode":pincode ,"password":password,"sensorId":sensor}
		db.child("1000").child(uniqueid).set(data)

	return render(request,'sign_up.html')

# signing as admin
def signinadmin(request):

	if request.method == "POST":
		email = request.POST.get('email')
		password = request.POST.get('password')

		#val = db.child('1000400074').order_by_child('email').equal_to('2016.megha.sahu@ves.ac.in').get()
		#print(val.order_by_child('password').get())

		# fetching data where email id is equals to email
		val = db.child('admin').order_by_child('email').equal_to(email).get()
		print("in")

		#print(val.val())
		
		# accessing fetched data 
		for val1 in val.each():
			print("hey")

			# getting value from pyrebase object
			value = val1.val()

			print(value["password"])

			# comparing fetched password and entered password
			if(value["password"] == password):
				print("rendering")
				messages.success(request,"Login successful")
				return render(request,'admin.html')

			else:
				messages.warning(request,"Login Failed")
				return render(request,'sign_in_admin.html')


	return render(request,'sign_in_admin.html')

#signing in as user
def signin_user(request):

	if request.method == "POST":
		email = request.POST.get('username')
		password = request.POST.get('password')

		#val = db.child('1000400074').order_by_child('email').equal_to('2016.megha.sahu@ves.ac.in').get()
		#print(val.order_by_child('password').get())

		# fetching data where email id is equals to email
		val = db.child('1000').order_by_child('email').equal_to(email).get()
		
		# accessing fetched data 
		for val1 in val.each():

			# getting value from pyrebase object
			value = val1.val()

			print(value["password"])

			# comparing fetched password and entered password
			if(value["password"] == password):
				print("rendering")
				request.session['username'] = email
				messages.success(request,"Login successful")
				return render(request,'user.html')

			else:
				messages.warning(request,"Login Failed")
				return render(request,'sign_in_user.html')

	return render(request,'sign_in_user.html')

def aboutUs(request):
	return render(request,'about_us.html')

def contact(request):
	return render(request,'contact_us.html')

def adminland(request):

	if request.method == "POST":
		startdate = request.POST.get('startingyear')
		enddate = request.POST.get('endingyear')

		data = list()

		print(startdate)
		print(enddate)

		# fetching data from start date to end date
		#val = db.child('consumption').order_by_child('date').equal_to('13-01-2019').get()

		val = db.child('consumption').get().val()


		#print(val.key())

		"""
		for vibe_dict in val.items(): # dict is a Python keyword, so it's a bad choice for a variable!
			print(vibe_dict[0])
			result = db.child('consumption').child(vibe_dict[0]).order_by_child('date').equal_to('13-01-2019').get().val()

			for consumption in val.each():
				v = consumption.val()
				data.append([v])
				print("printing v")
				print(data)

		
		#start_at('13-01-2019').end_at('14-01-2019')

		
		

		
		# creating csv file and saving fetched data into it
		with open('new.csv','w',newline='') as file1:
			writer = csv.writer(file1)
			writer.writerows(data)

		print(val)
		"""		
		return render(request,'modelResult.html')
	else:
		return render(request,'admin.html')


def userland(request):
	if request.session.has_key('username'):
		return render(request,'user.html')

	else:
		return render(request,'sign_in_user.html')

def modelResult(request):

	print("in")

	series = Series.from_csv('water.csv', header=0)
	split_point = len(series) - 10
	dataset, validation = series[0:split_point], series[split_point:]
	print('Dataset %d, Validation %d' % (len(dataset), len(validation)))
	dataset.to_csv('dataset.csv')
	validation.to_csv('validation.csv')

	
	# load data
	series = Series.from_csv('dataset.csv')
	# prepare data


	X = series.values
	X = X.astype('float32')
	train_size = int(len(X) * 0.50)
	train, test = X[0:train_size], X[train_size:]
	# walk-forward validation
	history = [x for x in train]
	predictions = list()
	for i in range(len(test)):
		# predict
		yhat = history[-1]
		predictions.append(yhat)
		# observation
		obs = test[i]
		history.append(obs)
		print('>Predicted=%.3f, Expected=%3.f' % (yhat, obs))
	# report performance
	mse = mean_squared_error(test, predictions)
	rmse = sqrt(mse)
	print('RMSE: %.3f' % rmse)

	fig = Figure()
	ax = fig.add_subplot(111)
	data_df = pandas.read_csv("water.csv")
	data_df = pandas.DataFrame(data_df)
	data_df.plot(ax=ax)
	canvas = FigureCanvas(fig)
	fig.savefig('water/static/img/test.png')
	response = HttpResponse( content_type = 'image/png')
	canvas.print_png(response)


	#return response

	"""
	series = Series.from_csv('water.csv')
	res = series.plot()
	#pyplot.show()

	print("hey")

	
	buffer = io.BytesIO()
	canvas = pyplot.get_current_fig_manager().canvas
	canvas.draw()
	#graphIMG = PIL.Image.frombytes("RGB", canvas.get_width_height(), canvas.tostring_rgb())

	graphIMG = PIL.Image.frombytes("RGB", canvas.get_width_height(), canvas.tostring_rgb())
	graphIMG.save(buffer,"PNG")
	pyplot.close()
	graph = base64.b64encode(buffer.getvalue())

	
	#return response

	def __getnewargs__(self):
		return ((self.endog),(self.k_lags, self.k_diff, self.k_ma))
    #return HttpResponse(buffer.getvalue(), content_type="image/png")
    ARIMA.__getnewargs__ = __getnewargs__
 
# load data
	series = Series.from_csv('dataset.csv')
	# prepare data
	X = series.values
	X = X.astype('float32')
	# fit model
	model = ARIMA(X, order=(2,1,0))
	model_fit = model.fit(trend='nc', disp=0)
	# bias constant, could be calculated from in-sample mean residual
	bias = 1.081624
	# save model
	model_fit.save('model.pkl')
	numpy.save('model_bias.npy', [bias])

	model_fit = ARIMAResults.load('model.pkl')
	bias = numpy.load('model_bias.npy')
	yhat = bias + float(model_fit.forecast()[0])
	print('Predicted: %.3f' % yhat)

	# final

	dataset = Series.from_csv('dataset.csv')
	X = dataset.values.astype('float32')
	history = [x for x in X]
	validation = Series.from_csv('validation.csv')
	y = validation.values.astype('float32')
	# load model
	model_fit = ARIMAResults.load('model.pkl')
	bias = numpy.load('model_bias.npy')
	# make first prediction
	predictions = list()
	yhat = bias + float(model_fit.forecast()[0])
	predictions.append(yhat)
	history.append(y[0])
	print('>Predicted=%.3f, Expected=%3.f' % (yhat, y[0]))
# rolling forecasts
	for i in range(1, len(y)):
		# predict
		model = ARIMA(history, order=(2,1,0))
		model_fit = model.fit(trend='nc', disp=0)
		yhat = bias + float(model_fit.forecast()[0])
		predictions.append(yhat)
		# observation
		obs = y[i]
		history.append(obs)
		print('>Predicted=%.3f, Expected=%3.f' % (yhat, obs))
# report performance
	mse = mean_squared_error(y, predictions)
	rmse = sqrt(mse)
	print('RMSE: %.3f' % rmse)
	pyplot.plot(y)
	pyplot.plot(predictions, color='red')
	pyplot.show()
	"""


	return render(request,'modelResult.html')