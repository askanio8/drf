from rest_framework import serializers
from women.models import Women


# свой класс серилизации
class WomenSerializer1(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    content = serializers.CharField()
    # свойства read_only=True заполняются автоматически
    time_create = serializers.DateTimeField(read_only=True)
    time_update = serializers.DateTimeField(read_only=True)
    is_published = serializers.BooleanField(default=True)
    cat_id = serializers.IntegerField()

    def create(self, validated_data):  # вызывается методом is_valid()? save()!
        return Women.objects.create(**validated_data)  # создается запись в бд и возвращается назад

    def update(self, instance, validated_data):  # вызывается методом is_valid()? save()!
        instance.title = validated_data.get("title", instance.title)
        instance.content = validated_data.get("content", instance.content)
        instance.time_update = validated_data.get("time_update", instance.time_update)
        instance.is_published = validated_data.get("is_published", instance.is_published)
        instance.cat_id = validated_data.get("cat_id", instance.cat_id)
        instance.save()
        return instance



############## НИЗКОУРОВНЕВАЯ СЕРИЛИЗАЦИЯ ДЕСЕРИЛИЗАЦИЯ
# подопытный класс для серилизации
#class WomenModel:
#    def __init__(self, title, content):
#        self.title = title
#        self.content = content

# класс серилизатор для WomenModel
#class WomenSerializer(serializers.Serializer):
#    title = serializers.CharField(max_length=255)
#    content = serializers.CharField()

# кодируем класс в json
#def encode():
#    model = WomenModel('Анджелина Джоли', 'Биография')  # модель
#    model_sr = WomenSerializer(model)  # словарь
#    # Serializer может преводить класс в удобный для перевода в json формат с валидацией данных
#    model_sr.data
#    json = JSONRenderer().render(model_sr.data)  # json

# из json в класс
#def decode():
#    stream = io.BytesIO(b'{"title": "Анджелина Джоли", "content": "Биография"}')  # поток
#    data = JSONParser.parse(stream)  # json
#    serializer = WomenSerializer(data=data)
#    serializer.is_valid()  # обязательно вызвать чтобы появилось serializer.validated_data
#    print(serializer.validated_data)  # словарь

########################################################

# автосерилизация
class WomenSerializer(serializers.ModelSerializer):
    # при добавлениии пользователя выбирать не нужно, поле заполняется автоматически
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Women
        #fields = ('title', 'content', 'is_published', 'cat', 'user')
        fields = '__all__'
