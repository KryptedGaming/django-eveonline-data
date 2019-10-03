from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse
from django.views.generic import TemplateView
from django_eveonline_connector.models import EveCharacter, EveEntity
from django_eveonline_audit.models import EveAsset, EveClone, EveContact
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape

# Character Views
def view_character(request, external_id):
    context = {}
    context['character'] = EveCharacter.objects.get(external_id=external_id)
    return render(request, 'django_eveonline_audit/adminlte/view_character.html', context)

def refresh_character(request, external_id):
    pass 

def view_character_assets(request, external_id):
    character = EveCharacter.objects.get(external_id=external_id)
    return render(
        request,
        'django_eveonline_audit/adminlte/assets/view_character_assets.html',
        context = {
            'character': character,
        }
    )

def view_character_clones(request, external_id):
    character = EveCharacter.objects.get(external_id=external_id)
    return render(
        request,
        'django_eveonline_audit/adminlte/clones/view_character_clones.html',
        context = {
            'character': character,
        }
    )

def view_character_contacts(request, external_id):
    character = EveCharacter.objects.get(external_id=external_id)
    return render(
        request,
        'django_eveonline_audit/adminlte/contacts/view_character_contacts.html',
        context = {
            'character': character,
        }
    )

# Corporation Views
def view_corporation(request, external_id):
    pass 

def refresh_corporation(request, external_id):
    pass

# Alliance Views
def view_alliance(request, external_id):
    pass

# JSON Responses
def get_assets(request):
    if 'external_id' not in request.GET:
        return HttpResponse(status=400)
    if not EveEntity.objects.filter(external_id=request.GET.get('external_id')):
        return HttpResponse(status=404)
    return AssetJson.as_view()(request)

def get_clones(request):
    if 'external_id' not in request.GET:
        return HttpResponse(status=400)
    if not EveEntity.objects.filter(external_id=request.GET.get('external_id')):
        return HttpResponse(status=404)
    return CloneJson.as_view()(request)

def get_contacts(request):
    if 'external_id' not in request.GET:
        return HttpResponse(status=400)
    if not EveEntity.objects.filter(external_id=request.GET.get('external_id')):
        return HttpResponse(status=404)
    return ContactJson.as_view()(request)

# JSON Class Views
class AssetJson(BaseDatatableView):
    model = EveAsset
    columns = ['item', 'location', 'quantity']
    order_columns = ['item', 'location', 'quantity']

    def filter_queryset(self, qs):
        # implement searching
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(item__istartswith=search)

        # return character
        external_id = self.request.GET.get('external_id')
        return qs.filter(Q(entity__external_id=external_id))

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.item,
                item.location,
                item.quantity,
            ])
        return json_data

class CloneJson(BaseDatatableView):
    model = EveClone
    columns = ['location', 'implants']
    order_columns = ['location', 'implants']

    def filter_queryset(self, qs):
        # implement searching
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(Q(location__istartswith=search) | Q(implants__contains=search))
            
        # return character
        external_id = self.request.GET.get('external_id')
        return qs.filter(Q(entity__external_id=external_id))

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.location,
                item.implants.replace(",", "<br>"),
            ])
        return json_data

class ContactJson(BaseDatatableView):
    model = EveContact
    columns = ['name', 'contact_type', 'standing']
    order_columns = ['name', 'contact_type', 'standing']

    def filter_queryset(self, qs):
        # implement searching
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(Q(name__istartswith=search))
            
        # return character
        external_id = self.request.GET.get('external_id')
        return qs.filter(Q(entity__external_id=external_id))

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.name,
                item.contact_type,
                item.standing
            ])
        return json_data