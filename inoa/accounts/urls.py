from django.urls import  path, include
from .views import Home, Login, Signup, Logout, DeleteStock, StockContent, Calendar, graphic_data, Graph_view
from stocks.utils.updateStocks import update

urlpatterns = [
    path('', Login ,name='login'),
    path('signup/', Signup ,name='signup'),
    path('logout/',Logout,name='logout'),
    path('home/', Home ,name='home'),
    path('stocks/', StockContent ,name='stocks'),
    path('calendar/', Calendar ,name='calendar'),
    path('delete/', DeleteStock ,name='delete'),#de uso do form no index
    path('graphic_data/',graphic_data, name="graphic_data"),
    path('graph/',Graph_view, name="graph")
]

#Chamada da funcao de atualizacao e monitoramento das acoes
update()