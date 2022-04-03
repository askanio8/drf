import io

from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser

from .models import Women, Category
from .permissions import *

# Create your views here.
from .serializers import WomenSerializer

########## класс без серилизации, просто API для работы с моделью таблиц бд, возвращает список а не json
#class WomenAPIView(APIView):
#    def get(self, request):
#        lst = Women.objects.all().values()
#        return Response({'posts': list(lst)})
#
#    def post(self, request):
#        post_new = Women.objects.create(
#            title=request.data['title'],
#            content=request.data['content'],
#            cat_id=request.data['cat_id']
#        )
#        return Response({'post': model_to_dict(post_new)}

################## низкоуровневый класс с серилизацией
#class WomenAPIView1(APIView):
#    def get(self, request):
#        w = Women.objects.all()
#        # many=True значит нужно отдать не одну запись
#        return Response({'posts': WomenSerializer(w, many=True).data})

#    def post(self, request):
#        serializer = WomenSerializer(data=request.data)
#        serializer.is_valid(raise_exception=True)
#        serializer.save()  # вместо строчек ниже, если в серилизаторе есть метод create()
#        #post_new = Women.objects.create(
#        #    title=request.data['title'],
#        #    content=request.data['content'],
#        #    cat_id=request.data['cat_id']
#        #)
#        #return Response({'post': WomenSerializer(post_new).data})

#        return Response({'post': serializer.data})

#    def put(self, request, *args, **kwargs):
#        pk = kwargs.get("pk", None)  # если ключа pk нет, то None
#        if not pk:  # если запрос без поля pk
#            return Response({"error": "Method PUT not allowed"})

#        try:  # пытаемся найти объект в таблице по индексу
#            instance = Women.objects.get(pk=pk)
#        except:
#            return Response({"error", "Object does not exists"})

#        serializer = WomenSerializer(data=request.data, instance=instance)
#        serializer.is_valid(raise_exception=True)
#        # а здесь будет вызват метод update, т.к. в конструкторе WomenSerializer было 2 параметра
#        serializer.save()
#        return Response({"post": serializer.data})
#########################################################################

########### с помощью классов ListCreate UpdateAPIView RetrieveUpdateDestroyAPIView ...
#class WomenAPIView(generics.ListCreate):  # GET и POST
#    queryset = Women.objects.all()
#    serializer_class = WomenSerializer


#class WomenAPIUpdate(generics.UpdateAPIView):  # PUT
#    queryset = Women.objects.all()  # это ленивый запрос, будет получена только одна запись
#    serializer_class = WomenSerializer

#class WomenAPIDetailView(generics.RetrieveUpdateDestroyAPIView):  # CRUD (только для одной записи)
#    queryset = Women.objects.all()  # это ленивый запрос, будет получена только одна запись
#    serializer_class = WomenSerializer
################################################################

# С помощью классов ViewSet (есть еще GenericViewSet ModelViewSet ReadOnlyModelViewSet)
# кроме того можно определить свой класс VievSet через список родительских классов ViewSet, чтобы
# ограничить список типов запросов
#class WomenViewSet(viewsets.ModelViewSet):
#    queryset = Women.objects.all()
#    serializer_class = WomenSerializer
#
#    # дополнительные адреса
#    @action(methods=['get'], detail=False)  # detail=False значит возвращать список а не одну запись
#    def category(self, request):  # из имени метода создается адрес .../women/category/
#        cats = Category.objects.all()
#        return Response({'cats': [c.name for c in cats]})  # список категорий в Category
#
#    @action(methods=['get'], detail=True)  # detail=True значит возвращать одну запись
#    def somecategory(self, request, pk=None):  # из имени метода создается адрес .../women/<int>/somecategory/
#        cats = Category.objects.get(pk=pk)
#        return Response({'cats': cats.name})  # имя категории

########### еще один вариант с использованием APIView
class WomeAPIListPagination(PageNumberPagination):  # локальная пагинация
    page_size = 3
    page_query_param = 'page_size'
    max_page_size = 4

class WomenAPIlist(generics.ListCreateAPIView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)  # читать всем, изменять только с правами
    pagination_class = WomeAPIListPagination  # локальная пагинация

class WomenAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer
    permission_classes = (IsOwnerOrReadOnly, )
    #authentication_classes = (TokenAuthentication, )  # только по токенам, по сессиям нельзя будет

class WomenAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer
    permission_classes = (IsAdminUser, )  # удалять может только администратор
