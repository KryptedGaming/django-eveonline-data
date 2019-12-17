from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponse
from django.views.generic import TemplateView
from django_eveonline_connector.models import EveCharacter, EveEntity
from django_eveonline_entity_extensions.models import EveAsset, EveClone, EveContact, EveContract, EveSkill, EveJournalEntry, EveTransaction
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.contrib.auth.decorators import login_required, permission_required
from .tasks import update_eve_character_all
from django.utils.html import escape

# Character Views

@login_required
@permission_required('django_eveonline_connector.view_evecharacter', raise_exception=True)
def view_character(request, external_id):
    context = {}
    context['character'] = EveCharacter.objects.get(external_id=external_id)
    return render(request, 'django_eveonline_entity_extensions/adminlte/view_character.html', context)


@login_required
@permission_required('django_eveonline_connector.change_evecharacter')
def refresh_character(request, external_id):
    try:
        update_eve_character_all(external_id)
        messages.success(request, "Character successfully updated")
    except Exception as e:
        messages.error(request, "Character was not updated: %s" % e)
    return redirect('django-eveonline-entity-extensions-view-character', external_id)

@login_required
@permission_required('django_eveonline_connector.view_evecharacter', raise_exception=True)
@permission_required('django_eveonline_connector.view_eveasset', raise_exception=True)
def view_character_assets(request, external_id):
    character = EveCharacter.objects.get(external_id=external_id)
    return render(
        request,
        'django_eveonline_entity_extensions/adminlte/assets/view_character_assets.html',
        context={
            'character': character,
        }
    )

@login_required
@permission_required('django_eveonline_connector.view_evecharacter', raise_exception=True)
@permission_required('django_eveonline_connector.view_eveclone', raise_exception=True)
def view_character_clones(request, external_id):
    character = EveCharacter.objects.get(external_id=external_id)
    return render(
        request,
        'django_eveonline_entity_extensions/adminlte/clones/view_character_clones.html',
        context={
            'character': character,
        }
    )

@login_required
@permission_required('django_eveonline_connector.view_evecharacter', raise_exception=True)
@permission_required('django_eveonline_connector.view_evecontract', raise_exception=True)
def view_character_contracts(request, external_id):
    character = EveCharacter.objects.get(external_id=external_id)
    return render(
        request,
        'django_eveonline_entity_extensions/adminlte/contracts/view_character_contracts.html',
        context={
            'character': character,
        }
    )

@login_required
@permission_required('django_eveonline_connector.view_evecharacter', raise_exception=True)
@permission_required('django_eveonline_connector.view_evecontact', raise_exception=True)
def view_character_contacts(request, external_id):
    character = EveCharacter.objects.get(external_id=external_id)
    return render(
        request,
        'django_eveonline_entity_extensions/adminlte/contacts/view_character_contacts.html',
        context={
            'character': character,
        }
    )

@login_required
@permission_required('django_eveonline_connector.view_evecharacter', raise_exception=True)
@permission_required('django_eveonline_connector.view_eveskill', raise_exception=True)
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

@login_required
@permission_required('django_eveonline_connector.view_evecharacter', raise_exception=True)
@permission_required('django_eveonline_connector.view_evejournalentry', raise_exception=True)
def view_character_journal(request, external_id):
    character = EveCharacter.objects.get(external_id=external_id)
    return render(
        request,
        'django_eveonline_entity_extensions/adminlte/journal/view_character_journal.html',
        context={
            'character': character,
        }
    )

@login_required
@permission_required('django_eveonline_connector.view_evecharacter', raise_exception=True)
@permission_required('django_eveonline_connector.view_evetransaction', raise_exception=True)
def view_character_transactions(request, external_id):
    character = EveCharacter.objects.get(external_id=external_id)
    return render(
        request,
        'django_eveonline_entity_extensions/adminlte/transactions/view_character_transactions.html',
        context={
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


def get_contracts(request):
    if 'external_id' not in request.GET:
        return HttpResponse(status=400)
    if not EveEntity.objects.filter(external_id=request.GET.get('external_id')):
        return HttpResponse(status=404)
    return ContractJson.as_view()(request)


def get_journal(request):
    if 'external_id' not in request.GET:
        return HttpResponse(status=400)
    if not EveEntity.objects.filter(external_id=request.GET.get('external_id')):
        return HttpResponse(status=404)
    return JournalJson.as_view()(request)

def get_transactions(request):
    if 'external_id' not in request.GET:
        return HttpResponse(status=400)
    if not EveEntity.objects.filter(external_id=request.GET.get('external_id')):
        return HttpResponse(status=404)
    return TransactionJson.as_view()(request)


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


class JournalJson(BaseDatatableView):
    model = EveJournalEntry
    columns = ['date', 'type', 'first_party', 'second_party', 'value']
    order_columns = ['date', 'type', 'first_party', 'second_party', 'value']

    def filter_queryset(self, qs):
        # implement searching
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(Q(type__istartswith=search) |
                           Q(first_party__istartswith=search) |
                           Q(second_party__istartswith=search))

        # return character
        external_id = self.request.GET.get('external_id')
        return qs.filter(Q(entity__external_id=external_id))

    def prepare_results(self, qs):
        json_data = []
        # resolve custom template responses
        for entry in qs:
            first_party_ext = "jpg"
            second_party_ext = "jpg"
            if entry.first_party_type == "CORPORATION":
                first_party_ext = "png"
            if entry.second_party_type == "CORPORATION":
                second_party_ext = "png"
            # add avatars for first party field
            if entry.first_party_type == "CORPORATION" or entry.first_party_type == "CHARACTER":
                entry_first_party = """
                <img width="32px" src="https://imageserver.eveonline.com/%s/%s_64.%s" class="img-circle img-bordered-sm" alt="Avatar">
                %s 
                """ % (entry.first_party_type.title(), entry.first_party_id, first_party_ext, entry.first_party)
            else:
                entry_first_party = entry.type
            # add avatars for second party field
            if entry.second_party_type == "CORPORATION" or entry.second_party_type == "CHARACTER":
                entry_second_party = """
                <img width="32px" src="https://imageserver.eveonline.com/%s/%s_64.%s" class="img-circle img-bordered-sm" alt="Avatar">
                %s 
                """ % (entry.second_party_type.title(), entry.second_party_id, second_party_ext, entry.second_party)
            else:
                entry.second_party = entry.type
            # clean up value html
            if entry.value < 0:
                amount_color = "red"
            else:
                amount_color = "green"
            entry_amount = """
                <p><span style="color: %s">%s</span></p>
            """ % (amount_color, f'{entry.value:,}')

            json_data.append([
                entry.date.strftime("%m-%d-%Y"),
                entry.type.title(),
                entry_first_party,
                entry_second_party,
                entry_amount,
            ])

        return json_data

class TransactionJson(BaseDatatableView):
    model = EveTransaction
    columns = ['client', 'item', 'quantity', 'value']
    order_columns = ['client', 'item', 'quantity', 'value']

    def filter_queryset(self, qs):
        # implement searching
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(Q(item__istartswith=search) |
                           Q(client__istartswith=search)
                           )

        # return character
        external_id = self.request.GET.get('external_id')
        return qs.filter(Q(entity__external_id=external_id))

    def prepare_results(self, qs):
        json_data = []
        # resolve custom template responses
        for transaction in qs:
            client_ext = "jpg"
            if transaction.client_type == "CORPORATION":
                client_ext = "png"
            # add avatars for client
            if transaction.client_type.upper() == "CORPORATION" or transaction.client_type.upper() == "CHARACTER":
                transaction_client = """
                <img width="32px" src="https://imageserver.eveonline.com/%s/%s_64.%s" class="img-circle img-bordered-sm" alt="Avatar">
                %s 
                """ % (transaction.client_type.title(), transaction.client_id, client_ext, transaction.client)
            else:
                transaction_client = transaction.client_type
            # clean up value html
            if transaction.is_buy:
                amount_color = "red"
            else:
                amount_color = "green"
            transaction_amount = """
                <p><span style="color: %s">%s</span></p>
            """ % (amount_color, f'{transaction.value:,}')

            json_data.append([
                transaction_client, 
                transaction.item,
                transaction.quantity,
                transaction_amount,
            ])

        return json_data