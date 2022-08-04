from project.settings import TIME_ZONE
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from bs4 import BeautifulSoup
import requests
from requests import get
from pro.autoscraper.autoscraper.auto_scraper import AutoScraper
from .models import Txns

# Create your views here.
def index(request):
	return render(request,'pro/login.html',{})

def sign(request):
	return render(request,'pro/signup.html',{})	

def home(request):
	return render(request,'pro/myycrousel.html',{})

def port(request):
	return render(request,'pro/portfolio.html',{})

def docu(request):
	return render(request,'pro/documentation.html',{})

def dash(request):
	return render(request,'pro/dashboard.html',{})	


@csrf_exempt
def send_data(request):
	try:
		if(request.POST):
			User.objects.create(username=request.POST['user'],first_name=request.POST['frtName'],last_name=request.POST['lrtName'],email=request.POST['mail'],password=request.POST['password'])
           
	except Exception as e:
		print('Error is ',e)
	return HttpResponse('success')	


@csrf_exempt
def log(request):
	try:
		u=request.POST['uname']

		p=request.POST['pword']
		if(u!='' or p!=''):
			z=authenticate(username=u,password=p)
			if(z=='True'):
				login(request,z)
			return HttpResponse('log_success')
		else:
			return HttpResponse('Error')
	except Exception as e:
		print('error is',e)

# ###############################################################
@csrf_exempt
def url1(request):
	f1=open('D:\\abc\\structure.txt','a')
	u=request.POST['url']
	print(u)
	url ='https://'+u
	response = get(url)
	f1.write(response.text[:])
	f1.close()
	return HttpResponse('success')


#################################################################
@csrf_exempt
def links(request):
	url =request.POST['web']
	r  = requests.get("http://" +url)
	data = r.text
	soup = BeautifulSoup(data)
	m=open('D:\\abc\\link.txt','a')
	for link in soup.find_all('a'):
		print(link.get('href'))
		m.write(link.get('href'))
		m.write("\n")
	m.close()
	return HttpResponse('link_success')

#################################################################
@csrf_exempt
def texts(request):
	url="https://etherscan.io/txs"
	scraper = AutoScraper()
	soup_data = scraper._get_soup(url)
	tabledata = soup_data.find('table', class_="table table-hover")
	
	headers = []
	for i in tabledata.find_all('th'):
		title = i.text
		headers.append(title)

	tr_datas = []
	td_datas = []
	for trdata in tabledata.find_all('tr'):
		for td in trdata.find_all('td'):
			td_datas.append(td)

		if len(td_datas) > 0:
    		
			hash = td_datas[1].find('a').text
			method = td_datas[2].find('span').text
			block = td_datas[3].find('a').text
			time_txt = td_datas[4].find('span').text
			
			txn_from_tag = td_datas[6].find('a')
			txn_from_attrs = txn_from_tag.attrs
			txn_from = ''
			search_key = 'title'
			if search_key in txn_from_attrs.keys(): 
        			txn_from = txn_from_attrs[search_key]
			else:
    				txn_from = txn_from_tag.text
					
			txn_to_tag = td_datas[8].find('a')
			txn_to_attrs = txn_to_tag.attrs
			txn_to = ''

			if search_key in txn_to_attrs.keys(): 
        			txn_to = txn_to_attrs[search_key]
			else:
    				txn_to = txn_to_tag.text

			value = td_datas[9].text.split(' Ether')[0]
			fee = td_datas[10].text
			
			row = Txns(txn_hash = hash,	method = method, block = block, age = time_txt, txn_from = txn_from, txn_to = txn_to, value = value, txn_fee = fee)
			row.save()
		
	return HttpResponse('text_success')	