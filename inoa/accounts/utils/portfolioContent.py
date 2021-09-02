from stocks.models import Stock, Price
from ..models import User, Portfolio

#Retorna as carteiras de um usuario
def portfolioContent(user):
    portfolios = Portfolio.objects.filter(user=user)
    data = []

    for portfolio in portfolios:
        stocks = portfolio.portfolio.all()
        dataStocks = []
        for stock in stocks:
            aux = {
                "id" : stock.id,
                "name" : stock.name,
                "symbol" : stock.symbol,
                "description" : stock.description,
                "website" : stock.website,
                "currency" : stock.currency,
                "current_quote" : stock.current_quote.current_value,
                "limit_inferior" : stock.limit_inferior,
                "limit_superior" : stock.limit_superior,
                "trend": stock.trend,
                "historic" : stock.historic.all().order_by('-date')
            }
            dataStocks.append(aux)
        auxPortifolio = {
            "id" : portfolio.id,
            "name" : portfolio.name,
            "stocks" : dataStocks
        }
        data.append(auxPortifolio)
    
    return data