from celery import shared_task
from django.utils.dateparse import parse_datetime
from django_eveonline_connector.models import EveCharacter, EveCorporation, EveAlliance
from django_eveonline_entity_extensions.models import EveAsset, EveClone, EveContact, EveContract, EveSkill, EveSkillPoints, EveNetWorth, EveJournalEntry, EveTransaction
from django_eveonline_connector.services.esi.assets import get_eve_character_assets
from django_eveonline_connector.services.esi.clones import get_eve_character_clones
from django_eveonline_connector.services.esi.contacts import get_eve_character_contacts
from django_eveonline_connector.services.esi.contracts import get_eve_character_contracts
from django_eveonline_connector.services.esi.skills import get_eve_character_skills
from django_eveonline_connector.services.esi.journal import get_eve_character_journal
from django_eveonline_connector.services.esi.transactions import get_eve_character_transactions
from django_eveonline_connector.services.esi.character import get_eve_character_skillpoints, get_eve_character_net_worth
import logging

logger = logging.getLogger(__name__)

""" 
Global Tasks
These tasks are what users register to maintain up-to-date audit information.
"""

@shared_task
def update_all_eve_characters_assets(corporation_id=None, alliance_id=None):
    if corporation_id:
        characters = EveCharacter.objects.filter(corporation__external_id=corporation_id).exclude(token=None)
    elif alliance_id:
        characters = EveCharacter.objects.filter(corporation__alliance__external_id=alliance_id).exclude(token=None)
    else:
        characters = EveCharacter.objects.all().exclude(token=None)
    
    for character in characters:
        update_eve_character_assets.apply_async(args=[character.external_id])

@shared_task
def update_all_eve_characters_clones(corporation_id=None, alliance_id=None):
    if corporation_id:
        characters = EveCharacter.objects.filter(corporation__external_id=corporation_id).exclude(token=None)
    elif alliance_id:
        characters = EveCharacter.objects.filter(corporation__alliance__external_id=alliance_id).exclude(token=None)
    else:
        characters = EveCharacter.objects.all().exclude(token=None)
    
    for character in characters:
        update_eve_character_clones.apply_async(args=[character.external_id])

@shared_task
def update_all_eve_characters_contacts(corporation_id=None, alliance_id=None):
    if corporation_id:
        characters = EveCharacter.objects.filter(corporation__external_id=corporation_id).exclude(token=None)
    elif alliance_id:
        characters = EveCharacter.objects.filter(corporation__alliance__external_id=alliance_id).exclude(token=None)
    else:
        characters = EveCharacter.objects.all().exclude(token=None)
    
    for character in characters:
        update_eve_character_contacts.apply_async(args=[character.external_id])

@shared_task
def update_all_eve_characters_contracts(corporation_id=None, alliance_id=None):
    if corporation_id:
        characters = EveCharacter.objects.filter(corporation__external_id=corporation_id).exclude(token=None)
    elif alliance_id:
        characters = EveCharacter.objects.filter(corporation__alliance__external_id=alliance_id).exclude(token=None)
    else:
        characters = EveCharacter.objects.all().exclude(token=None)
    
    for character in characters:
        update_eve_character_contracts.apply_async(args=[character.external_id])

@shared_task
def update_all_eve_characters_journals(corporation_id=None, alliance_id=None):
    if corporation_id:
        characters = EveCharacter.objects.filter(corporation__external_id=corporation_id).exclude(token=None)
    elif alliance_id:
        characters = EveCharacter.objects.filter(corporation__alliance__external_id=alliance_id).exclude(token=None)
    else:
        characters = EveCharacter.objects.all().exclude(token=None)
    
    for character in characters:
        update_eve_character_journal.apply_async(args=[character.external_id])

@shared_task
def update_all_eve_characters_skills(corporation_id=None, alliance_id=None):
    if corporation_id:
        characters = EveCharacter.objects.filter(corporation__external_id=corporation_id).exclude(token=None)
    elif alliance_id:
        characters = EveCharacter.objects.filter(corporation__alliance__external_id=alliance_id).exclude(token=None)
    else:
        characters = EveCharacter.objects.all().exclude(token=None)
    
    for character in characters:
        update_eve_character_skills.apply_async(args=[character.external_id])

@shared_task
def update_all_eve_characters_transactions(corporation_id=None, alliance_id=None):
    if corporation_id:
        characters = EveCharacter.objects.filter(corporation__external_id=corporation_id).exclude(token=None)
    elif alliance_id:
        characters = EveCharacter.objects.filter(corporation__alliance__external_id=alliance_id).exclude(token=None)
    else:
        characters = EveCharacter.objects.all().exclude(token=None)
    
    for character in characters:
        update_eve_character_transactions.apply_async(args=[character.external_id])

"""
EveCharacter Tasks 
The tasks are used to update backend models related to EveCharacter objects
"""
@shared_task
def update_eve_character_all(character_id):
    update_eve_character_assets.apply_async(args=[character_id])
    update_eve_character_clones.apply_async(args=[character_id])
    update_eve_character_contacts.apply_async(args=[character_id])
    update_eve_character_contracts.apply_async(args=[character_id])
    update_eve_character_journal.apply_async(args=[character_id])
    update_eve_character_skills.apply_async(args=[character_id])
    update_eve_character_transactions.apply_async(args=[character_id])

@shared_task
def update_eve_character_assets(character_id):
    assets = get_eve_character_assets(character_id)
    # TODO: don't lazy delete
    EveAsset.objects.filter(entity__external_id=character_id).delete()
    for asset in assets:
        EveAsset(
            item=asset['item_name'],
            location=asset['location'],
            quantity=asset['quantity'],
            entity=EveCharacter.objects.get(external_id=character_id)
        ).save()

@shared_task
def update_eve_character_clones(character_id):
    clones = get_eve_character_clones(character_id)
    # TODO: don't lazy delete
    EveClone.objects.filter(entity__external_id=character_id).delete()
    for clone in clones:
        EveClone(
            location=clone['location'],
            implants=",".join(clone['implants']),
            entity=EveCharacter.objects.get(external_id=character_id)
        ).save()

@shared_task
def update_eve_character_contacts(character_id):
    logger.info("Updating contacts for %s" % character_id)
    contacts = get_eve_character_contacts(character_id)
    # TODO: don't lazy delete
    logger.info("Deleting existing contacts for %s" % character_id)
    EveContact.objects.filter(entity__external_id=character_id).delete()
    for contact in contacts:
        EveContact(
            name=contact['name'],
            contact_type=contact['type'],
            entity=EveCharacter.objects.get(external_id=character_id),
            standing=contact['standing']
        ).save()

@shared_task
def update_eve_character_contracts(character_id):
    logger.info("Updating contracts for %s" % character_id)
    contracts = get_eve_character_contracts(character_id)
    # TODO: don't lazy delete
    logger.info("Deleting existing contracts for %s" % character_id)
    EveContract.objects.filter(entity__external_id=character_id).delete()
    for contract in contracts:
        EveContract(
            external_id=contract['contract_id'],
            issued_by=contract['issued_by'],
            issued_by_type=contract['issued_by_type'],
            issued_to=contract['issued_to'],
            issued_to_type=contract['issued_to_type'],
            accepted_by=contract['accepted_by'],
            accepted_by_type=contract['accepted_by_type'],
            contract_type=contract['contract_type'],
            contract_status=contract['contract_status'],
            contract_value=contract['contract_value'],
            contract_items="\n".join(contract['items']),
            date_created=parse_datetime(contract['date_created'].to_json()),
            entity=EveCharacter.objects.get(external_id=character_id),
        ).save()
    logger.info("Successfully updated contracts for %s" % character_id)

@shared_task
def update_eve_character_skills(character_id):
    logger.info("Updating skills for %s" % character_id)
    skills = get_eve_character_skills(character_id)
    entity = EveCharacter.objects.get(external_id=character_id)
    # TODO: don't lazy delete
    logger.info("Deleting existing skills for %s" % character_id)
    EveSkill.objects.filter(entity__external_id=character_id).delete()
    for skill in skills:
        EveSkill(
            level=skill['trained_skill_level'],
            group=skill['skill_type'],
            name=skill['skill_name'],
            entity=EveCharacter.objects.get(external_id=character_id)
        ).save()
    logger.info("Successfully updated skills for %s" % character_id)
    skill_points = get_eve_character_skillpoints(character_id)
    eve_skill_points = EveSkillPoints.objects.get_or_create(entity=entity)[0]
    eve_skill_points.value = skill_points
    eve_skill_points.save()
    logger.info("Successfully updated skillpoints for %s" % character_id)

@shared_task
def update_eve_character_journal(character_id):
    logger.info("Updating journal entries for %s" % character_id)
    entity = EveCharacter.objects.get(external_id=character_id)
    # Get existing journal IDs
    existing_journal_entries = [
        entry.external_id for entry in EveJournalEntry.objects.filter(entity=entity)]
    journal = get_eve_character_journal(
        character_id, ignore_ids=existing_journal_entries)
    for entry in journal:
        EveJournalEntry(
            external_id=entry['id'],
            value=entry['amount'],
            type=entry['ref_type'].replace("_", " ").upper(),
            date=parse_datetime(entry['date'].to_json()),
            first_party=entry['first_party_name'],
            first_party_id=entry['first_party_id'],
            first_party_type=entry['first_party_type'],
            second_party=entry['second_party_name'],
            second_party_id=entry['second_party_id'],
            second_party_type=entry['second_party_type'],
            entity=entity
        ).save()
    logger.info("Successfully updated journal entries for %s" % entity.name)
    net_worth = get_eve_character_net_worth(character_id)
    eve_net_worth = EveNetWorth.objects.get_or_create(entity=entity)[0]
    eve_net_worth.value = net_worth
    eve_net_worth.save()
    logger.info("Successfully updated net worth for %s" % entity.name)

@shared_task
def update_eve_character_transactions(character_id):
    logger.info("Updating transactions for %s" % character_id)
    entity = EveCharacter.objects.get(external_id=character_id)
    # get existing transaction ids 
    existing_transaction_ids = [
        transaction.external_id for transaction in EveTransaction.objects.filter(entity=entity)
    ]
    transactions = get_eve_character_transactions(character_id, ignore_ids=existing_transaction_ids)

    for transaction in transactions:
        logger.debug(transaction)
        EveTransaction(
            item=transaction['type_name'],
            client=transaction['client'],
            client_id=transaction['client_id'],
            client_type=transaction['client_type'],
            external_id=transaction['transaction_id'],
            quantity=transaction['quantity'],
            is_buy=transaction['is_buy'], 
            value=transaction['quantity']*transaction['unit_price'],
            entity=entity,  
        ).save()