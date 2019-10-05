from django.db import models
from django_eveonline_connector.models import EveEntity


class EveAsset(models.Model):
    item = models.CharField(max_length=64)
    item_type = models.CharField(max_length=32)
    location = models.CharField(max_length=128)
    quantity = models.IntegerField()
    entity = models.ForeignKey(
        EveEntity, on_delete=models.CASCADE, related_name="assets")


class EveClone(models.Model):
    location = models.CharField(max_length=128)
    implants = models.TextField()
    entity = models.ForeignKey(
        EveEntity, on_delete=models.CASCADE, related_name="clones")

    def __str__(self):
        return "%s: %s" % (self.entity, self.location)

    def get_implant_list(self):
        return self.implants.split(",")


class EveContact(models.Model):
    contact_choices = (
        ("CHARACTER", "CHARACTER"),
        ("CORPORATION", "CORPORATION"),
        ("ALLIANCE", "ALLIANCE")
    )

    name = models.CharField(max_length=255)
    contact_type = models.CharField(max_length=32, choices=contact_choices)
    standing = models.FloatField()
    entity = models.ForeignKey(
        EveEntity, on_delete=models.CASCADE, related_name="contacts")


class EveContract(models.Model):
    contract_id_types = (
        ("CHARACTER", "CHARACTER"),
        ("CORPORATION", "CORPORATION")
    )
    external_id = models.IntegerField()

    issued_by = models.CharField(max_length=128)
    issued_to = models.CharField(max_length=128, null=True)
    issued_by_type = models.CharField(max_length=32, choices=contract_id_types)
    issued_to_type = models.CharField(
        max_length=32, choices=contract_id_types, null=True)
    accepted_by = models.CharField(max_length=128, null=True)
    accepted_by_type = models.CharField(
        max_length=32, choices=contract_id_types, null=True)

    contract_type = models.CharField(max_length=32)
    contract_status = models.CharField(max_length=64)
    contract_value = models.FloatField()
    contract_items = models.TextField()

    date_created = models.DateTimeField()

    entity = models.ForeignKey(
        EveEntity, on_delete=models.CASCADE, related_name="contracts")


class EveSkill(models.Model):
    name = models.CharField(max_length=64)
    group = models.CharField(max_length=64)
    level = models.IntegerField()
    entity = models.ForeignKey(
        EveEntity, on_delete=models.CASCADE, related_name="skills")

    class Meta:
        unique_together = ['entity', 'name']


class EveSkillPoints(models.Model):
    value = models.IntegerField()
    entity = models.OneToOneField(
        EveEntity, on_delete=models.CASCADE, related_name="skillpoints")


class EveNetWorth(models.Model):
    value = models.FloatField()
    entity = models.OneToOneField(
        EveEntity, on_delete=models.CASCADE, related_name="net_worth")


class EveJournalEntry(models.Model):
    party_type_choices = (
        ("CHARACTER", "CHARACTER"),
        ("CORPORATION", "CORPORATION")
    )
    external_id = models.IntegerField()
    type = models.CharField(max_length=128)
    value = models.FloatField()
    date = models.DateField()
    first_party = models.CharField(max_length=128)
    first_party_id = models.IntegerField()
    first_party_type = models.CharField(
        max_length=32, choices=party_type_choices)
    second_party = models.CharField(max_length=128)
    second_party_id = models.IntegerField()
    second_party_type = models.CharField(
        max_length=32, choices=party_type_choices)
    entity = models.ForeignKey(
        EveEntity, on_delete=models.CASCADE, related_name="journal")


class EveTransaction(models.Model):
    value = models.FloatField()
    item = models.CharField(max_length=64)
    quantity = models.IntegerField()
    is_buy = models.BooleanField()
    client_id = models.IntegerField()
    entity = models.ForeignKey(
        EveEntity, on_delete=models.CASCADE, related_name="transactions")
