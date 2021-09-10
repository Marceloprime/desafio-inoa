#django library
from django.shortcuts import render , redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

#python library
import requests
import json
from django.http import HttpResponse
import yfinance as yf
from yahoo_fin.stock_info import get_data
import pandas as pd

#Meus modules
from stocks.models import Stock, Price
from .models import User, Portfolio
from .utils.portfolioContent import portfolioContent
from stocks.utils.economic_calendar import economic_calendar


def Login(request):
    if(str(request.user) != "AnonymousUser"):
        return redirect('home')
    
    try:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Caso tenha sucesso
            return redirect('home')
        else:
            # Erro no login
            return render(request, 'login.html')

    except:
        return render(request, 'login.html')

    return render(request,'login.html')    

@login_required
def Logout(request):
    logout(request)
    return render(request, 'logout.html')#nesse html eh redirecionado para a urllogin

def Signup(request):
    if request.POST:
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        cpf_or_cnpj = request.POST['cpf_or_cnpj']
        phone = '+55' + request.POST['phone']
        password = request.POST['password']

        is_active = True
        try:
            user = User.objects._create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password,is_active=is_active,phone=phone,cpf_or_cnpj=cpf_or_cnpj)
        except:
            print("Erro na criação do usuário")
    return render(request,'signup.html')

@login_required
def Home(request):
    user =  request.user
    portfolios = portfolioContent(user)
   
    context = {
        "user" : user,
        "portfolios" : portfolios
    }
    
    if request.POST:
        try:
            if request.POST['portifolio']:#Criacao de portifolio
                user = User.objects.filter(username=request.user.username)[0]

                if Portfolio.objects.filter(name=request.POST['portifolio']):
                    messages.error(request,"Erro! esse nome já é usado")
                    return render(request, 'home.html',context=context)

                portfolio = Portfolio(user=user,name=request.POST['portifolio'])
                portfolio.save()

                messages.success(request,"Carteira criada com sucesso")

                portfolios = portfolioContent(user)
                context.portfolios = portfolios

                return render(request, 'home.html',context=context)
        except:
            print('Portifolio invalido')


        try:
            symbol = request.POST['codigo']
            portfolio = request.POST['type_content']
            portfolio = Portfolio.objects.filter(id=portfolio)[0]
        except:
            symbol = ''


        if symbol != '':
            symbol = symbol.upper()

            try:
                if_there_is = Portfolio.objects.filter(id=request.POST['type_content'],portfolio=Stock.objects.filter(symbol=symbol)[0].id)[0]
            except:
                if_there_is = None

            if if_there_is != None:
                messages.error(request,'Esse código '+ symbol + ' Já foi cadastrado')
            else:
                try:
                    r = requests.get('https://api.hgbrasil.com/finance/stock_price?key=9495f087&symbol='+symbol)
                    data = r.json()
                    price = Price(symbol=symbol,current_value=data['results'][symbol]['price'])
                    price.save()
                    stock = Stock(name=data['results'][symbol]['name'],symbol=symbol,description=data['results'][symbol]['description'],website=data['results'][symbol]['website'],currency=data['results'][symbol]['currency'],current_quote=price,limit_inferior=data['results'][symbol]['price'],limit_superior=data['results'][symbol]['price'])
                    stock.save()
                    portfolio.portfolio.add(stock)

                except:
                    messages.error(request,'Esse código '+ symbol + ' esta incorreto')
                    print(data)

    return render(request, 'home.html',context=context)

#usado pelo form em home.html para deletar um ativo

@login_required
def StockContent(request):
    user =  request.user
    portfolios = portfolioContent(user)
   
    context = {
        "user" : user,
        "portfolios" : portfolios
    }
    
    return render(request, 'stocks.html',context=context)

@login_required
def Calendar(request):
    user =  request.user
    calendar = economic_calendar()
    context = {
        "user" : user,
        "calendar": calendar
    }
    return render(request, 'calendar.html',context=context)

@login_required
def DeleteStock(request):
    if request.POST:
        try:
            stock_id = request.POST['submit']
            Stock.objects.filter(id=stock_id).delete()
        except:
            print('Erro ao deletar ativo')
    
    user =  request.user
    portifolios = portfolioContent(user)
    context = {
        "user" : user,
        "portifolios" : portifolios
    }

    return render(request, 'home.html',context=context)

@login_required
def graphic_data(request):

    user =  request.user
    portfolios = Portfolio.objects.filter(user=user)
    data = []
    for portfolio in portfolios:
        for stock in portfolio.portfolio.all():
            priceData = []
            for price in stock.historic.all():
                aux = {
                    "value" : price.current_value,
                    "date": str(price.date)
                }

                priceData.append(aux)
            
            aux = {
                "stock" : stock.id,
                "prices" : priceData
            }
        data.append(aux)

    #data = json.dumps(data)
    return HttpResponse(data)

@login_required
def Graph_view(request):
    if request.POST:
        symbol = request.POST['symbol']

        try:
            stock = Stock.objects.filter(symbol=symbol)[0]
        except:
            stock = ''
        
        dataHistoric = get_data(symbol+'.SA', start_date="12/04/2010", end_date="09/09/2021", index_as_date = True, interval="1d")
        weekly_data = get_data("msft", interval = "1wk")

        data = []
        
        try:
            for index, row in dataHistoric.iterrows():
                date = str(index)
                date = date.split(" ")

                print(int(row['close']))
                print(row['close'])

                data.append([date[0],int(row['close'])])
        except:
            print('error')
        #for historic in stock.historic.all():  
            #data.append([str(historic.date),int(historic.current_value)])


        context = {
            "stock" : stock,
            "historic" : data,
        }
        #print(data)
        return render(request, 'graph.html',context=context)

    return render(request, 'graph.html',context=context)