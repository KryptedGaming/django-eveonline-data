from django.urls import path
from . import views

urlpatterns = [
    path('character/view/<int:external_id>/', views.view_character, name="django-eveonline-entity-extensions-view-character"),
    path('character/refresh/<int:external_id>/', views.refresh_character, name="django-eveonline-entity-extensions-refresh-character"),
    path('corporation/view/<int:external_id>/', views.view_corporation, name="django-eveonline-entity-extensions-view-corporation"),
    path('corporation/refresh/<int:external_id>/', views.refresh_corporation, name="django-eveonline-entity-extensions-refresh-corporation"),
    path('alliance/view/<int:external_id>/', views.view_alliance, name="django-eveonline-entity-extensions-view-alliance"),
    path('character/view/<int:external_id>/assets/', views.view_character_assets, name="django-eveonline-entity-extensions-view-character-assets"),
    path('character/view/<int:external_id>/clones/', views.view_character_clones, name="django-eveonline-entity-extensions-view-character-clones"),
    path('character/view/<int:external_id>/contacts/', views.view_character_contacts, name="django-eveonline-entity-extensions-view-character-contacts"),
]

# JSON
urlpatterns += [
    path('api/assets/', views.get_assets, name="django-eveonline-entity-extensions-api-assets"),
    path('api/clones/', views.get_clones, name="django-eveonline-entity-extensions-api-clones"),
    path('api/contacts/', views.get_contacts, name="django-eveonline-entity-extensions-api-contacts"),
]