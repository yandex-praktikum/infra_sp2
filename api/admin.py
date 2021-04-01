from django.apps import apps
from django.contrib import admin

models = apps.get_models()

# Можно лучше: Как и раньше, заводим все модели в админку. Можно вот так:
for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
