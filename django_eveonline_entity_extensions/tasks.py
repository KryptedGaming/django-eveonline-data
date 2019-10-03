from celery import shared_task 
from django_eveonline_connector.models import EveCharacter, EveCorporation, EveAlliance 
from django_eveonline_audit.models import EveAsset, EveClone, EveContact, EveContract, EveSkill, EveSkillPoints, EveNetWorth, EveJournalEntry, EveTransaction
from django_eveonline_audit.queries.character.assets import get_eve_character_assets
from django_eveonline_audit.queries.character.clones import get_eve_character_clones
from django_eveonline_audit.queries.character.contacts import get_eve_character_contacts
import logging

logger = logging.getLogger(__name__)

""" 
Global Tasks
These tasks are what users register to maintain up-to-date audit information.
"""

@shared_task
def update_eve_characters_data():
    pass 

@shared_task
def update_eve_corporations_data():
    pass 

@shared_task
def update_eve_alliances_data():
    pass 

"""
EveCharacter Tasks 
The tasks are used to update backend models related to EveCharacter objects
"""
def update_character_assets(character_id):
    assets = get_eve_character_assets(character_id)
    # TODO: don't lazy delete
    EveAsset.objects.filter(entity__external_id=character_id).delete()
    for asset in assets:
        EveAsset(
            item = asset['item_name'],
            location = asset['location'],
            quantity = asset['quantity'],
            entity = EveCharacter.objects.get(external_id=character_id)
        ).save()

def update_character_clones(character_id):
    clones = get_eve_character_clones(character_id)
    # TODO: don't lazy delete
    EveClone.objects.filter(entity__external_id=character_id).delete()
    for clone in clones:
        EveClone(
            location = clone['location'],
            implants = ",".join(clone['implants']),
            entity = EveCharacter.objects.get(external_id=character_id)
        ).save()

def update_character_contacts(character_id):
    logger.info("Updating contacts for %s" % character_id)
    contacts = get_eve_character_contacts(character_id)
    # TODO: don't lazy delete 
    logger.info("Deleting existing contacts for %s" % character_id)
    EveContact.objects.filter(entity__external_id=character_id).delete()
    for contact in contacts:
        EveContact(
            name = contact['name'],
            contact_type = contact['type'],
            entity = EveCharacter.objects.get(external_id=character_id),
            standing = contact['standing']
        ).save()

def update_character_contracts():
    pass

def update_character_skills():
    pass 

def update_character_journal():
    pass 

def update_character_transactions():
    pass
