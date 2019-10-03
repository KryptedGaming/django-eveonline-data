from django.urls import path
from django_eveonline_ent import views

urlpatterns = [
    path('character/view/<int:external_id>/', views.view_character, name="django-eveonline-audit-view-character"),
    path('character/refresh/<int:external_id>/', views.refresh_character, name="django-eveonline-audit-refresh-character"),
    path('corporation/view/<int:external_id>/', views.view_corporation, name="django-eveonline-audit-view-corporation"),
    path('corporation/refresh/<int:external_id>/', views.refresh_corporation, name="django-eveonline-audit-refresh-corporation"),
    path('alliance/view/<int:external_id>/', views.view_alliance, name="django-eveonline-audit-view-alliance"),
    path('character/view/<int:external_id>/assets/', views.view_character_assets, name="django-eveonline-audit-view-character-assets"),
    path('character/view/<int:external_id>/clones/', views.view_character_clones, name="django-eveonline-audit-view-character-clones"),
    path('character/view/<int:external_id>/contacts/', views.view_character_contacts, name="django-eveonline-audit-view-character-contacts"),
]

# JSON
urlpatterns += [
    path('api/assets/', views.get_assets, name="django-eveonline-audit-api-assets"),
    path('api/clones/', views.get_clones, name="django-eveonline-audit-api-clones"),
    path('api/contacts/', views.get_contacts, name="django-eveonline-audit-api-contacts"),
]