import requests
from threading import Timer
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from decouple import config 
from datetime import datetime

#My modules
from ..models import Stock, Price
from accounts.models import User, Portfolio
from stocks.utils.setInterval import SetInterval


#Email e senhas
sender_address = config('email')
sender_pass = config('password')
receiver_address =  config('email')

def send_emails_sales(stock):
    portfolios = Portfolio.objects.filter(portfolio=stock)

    for portfolio in portfolios:
        mail_content = "Olá " + portfolio.user.first_name + " ."+ " O ativo " + stock.name + " está em queda, recomendamos a venda"

        #COnfiguração do MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = 'Inoa, recomendação.'   #Linha do assunto
        #o corpo da mensagem
        message.attach(MIMEText(mail_content, 'plain'))
        #eh criado SMTP session para enviar o email
        session = smtplib.SMTP('smtp.gmail.com', 587) #porta do gmail
        session.starttls() #habilitar segurança
        session.login(sender_address, sender_pass) #login
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        print('Email enviado')


def send_emails_purchase(stock):
    portfolios = Portfolio.objects.filter(portfolio=stock)

    for portfolio in portfolios:
        mail_content = "Olá " + portfolio.user.first_name + " ."+ " O ativo " + stock.name + " está em alta, recomendamos a compra"

        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = 'Inoa, recomendação.'  
        message.attach(MIMEText(mail_content, 'plain'))
        session = smtplib.SMTP('smtp.gmail.com', 587) 
        session.starttls()
        session.login(sender_address, sender_pass) 
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        print('Email enviado')

#atualizacao das acoes
def updateStocks() :
    stocks = Stock.objects.all()

    for stock in stocks:
        r = requests.get('https://api.hgbrasil.com/finance/stock_price?key='+config('API_KEY')+'&symbol='+ stock.symbol)
        data = r.json()
        price = Price(symbol=stock.symbol,current_value=data['results'][stock.symbol]['price'])
        price.save()

        #verificar a tendencia
        if stock.current_quote.current_value > float(data['results'][stock.symbol]['price']):
            stock.trend = 'down'
        elif stock.current_quote.current_value < float(data['results'][stock.symbol]['price']):
            stock.trend = 'up'

        #verificar os limites
        if stock.limit_inferior > float(data['results'][stock.symbol]['price']):
            stock.limit_inferior = float(data['results'][stock.symbol]['price'])
            try:
                send_emails_sales(stock)
            except:
                print('Falha no envio')

        if stock.limit_superior < float(data['results'][stock.symbol]['price']):
            stock.limit_superior = float(data['results'][stock.symbol]['price'])
            try:
                send_emails_purchase(stock)
            except:
                print('Falha no envio')

        before_price = stock.current_quote
        stock.current_quote = price
        stock.historic.add(price)# preco antigo eh salvo no historico
        stock.save()
        print(stock)
    print('\n')

#Usar a classe SetInterval para rodar a funcao updateStocks a cada periodo determinado no time
def update():
    now = datetime.now()
    #funcionamento da B3 das 8:00 as 19:00
    if now.hour < 19 and now.hour > 8:
        qtd_stock = len(Stock.objects.all())
        limit = int(400 / qtd_stock)
        print('Flag1')
        if limit == 0:
            print('Limite de ações alcançado, não é possivel realizar uma resquest com essa quantidade')
        else:   
            time = int(39600 / limit)#qtd de segundos em 11 horas
            print(time)
            inter=SetInterval(time,updateStocks)
            t=Timer(time,inter)
            t.start()