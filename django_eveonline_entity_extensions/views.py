from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse
from django.views.generic import TemplateView
from django_eveonline_connector.models import EveCharacter, EveEntity
from django_eveonline_entity_extensions.models import EveAsset, EveClone, EveContact, EveContract, EveSkill
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape

# Character Views


def view_character(request, external_id):
    context = {}
    context['character'] = EveCharacter.objects.get(external_id=external_id)
    return render(request, 'django_eveonline_entity_extensions/adminlte/view_character.html', context)


def refresh_character(request, external_id):
    pass


def view_character_assets(request, external_id):
    character = EveCharacter.objects.get(external_id=external_id)
    return render(
        request,
        'django_eveonline_entity_extensions/adminlte/assets/view_character_assets.html',
        context={
            'character': character,
        }
    )


def view_character_clones(request, external_id):
    character = EveCharacter.objects.get(external_id=external_id)
    return render(
        request,
        'django_eveonline_entity_extensions/adminlte/clones/view_character_clones.html',
        context={
            'character': character,
        }
    )


def view_character_contracts(request, external_id):
    character = EveCharacter.objects.get(external_id=external_id)
    return render(
        request,
        'django_eveonline_entity_extensions/adminlte/contracts/view_character_contracts.html',
        context={
            'character': character,
        }
    )


def view_character_contacts(request, external_id):
    character = EveCharacter.objects.get(external_id=external_id)
    return render(
        request,
        'django_eveonline_entity_extensions/adminlte/contacts/view_character_contacts.html',
        context={
            'character': character,
        }
    )


def view_character_skills(request, external_id):
    character = EveCharacter.objects.get(external_id=external_id)
    character_skills = EveSkill.objects.filter(entity=character)
    return render(
        request,
        'django_eveonline_entity_extensions/adminlte/skills/view_character_skills.html',
        context={
            'character': character,
            'skills': character_skills,
            'skill_names': ",".join([skill.name for skill in character_skills]),
            'skill_levels': ",".join([str(skill.level) for skill in character_skills]),
            'groups': set([skill.group for skill in character_skills]),
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


def get_contracts(request):
    if 'external_id' not in request.GET:
        return HttpResponse(status=400)
    if not EveEntity.objects.filter(external_id=request.GET.get('external_id')):
        return HttpResponse(status=404)
    return ContractJson.as_view()(request)


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
            qs = qs.filter(Q(location__istartswith=search)
                           | Q(implants__contains=search))

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


class ContractJson(BaseDatatableView):
    model = EveContract
    columns = ['date_created', 'contract_status',
               'contract_type', 'issued_by', 'issued_to', 'contract_items']
    order_columns = ['date_created', 'contract_status',
                     'contract_type', 'issued_by', 'issued_to', 'contract_items']

    def filter_queryset(self, qs):
        # implement searching
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(Q(issued_by__istartswith=search) |
                           Q(issued_to__istartswith=search) |
                           Q(accepted_by__istartswith=search)
                           )

        # return character
        external_id = self.request.GET.get('external_id')
        return qs.filter(Q(entity__external_id=external_id))

    def prepare_results(self, qs):
        json_data = []
        for contract in qs:
            date_created = contract.date_created
            contract_status = contract.contract_status
            contract_type = contract.contract_type
            from_who = contract.issued_by
            if contract.accepted_by:
                to_who = contract.accepted_by
            elif contract.issued_to:
                to_who = contract.issued_to
            else:
                to_who = "Public"
            actions = """
                <button class="text-center btn btn-success" data-toggle="modal" data-target="#view_%s"><i class="fa fa-eye"></i></button>
                <div class="modal fade col-md-12" id="view_%s" data-backdrop="false">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h4>View Contract</h4>
                            </div>

                            <div class="modal-body">
                               <p>%s</p>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                            </div>
                        </div>
                    </div>
                </div>
            """ % (contract.pk, contract.pk, contract.contract_items.replace("\n", "<br>"))

            json_data.append([
                date_created.strftime("%m-%d-%Y"),
                contract_status,
                contract_type.replace("_", " ").upper(),
                from_who,
                to_who,
                actions
            ])
        return json_data
