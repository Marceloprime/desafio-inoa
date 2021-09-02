from django.urls import  path, include
from .views import Index, Login, Signup, Logout, DeleteStock
from stocks.utils.updateStocks import update

urlpatterns = [
    path('', Login ,name='login'),
    path('signup/', Signup ,name='signup'),
    path('logout/',Logout,name='logout'),
    path('home/', Index ,name='index'),
    path('delete/', DeleteStock ,name='delete'),#de uso do form no index
]

#Chamada da funcao de atualizacao e monitoramento das acoes
update()