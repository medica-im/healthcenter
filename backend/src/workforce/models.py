from django.db import models
from django_postgresql_dag.models import node_factory, edge_factory
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from accounts.models import GrammaticalGender
import logging

logger = logging.getLogger(__name__)

class WorkforceBase(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True
    )
    label = models.CharField(
        max_length=36,
        unique=True,
    )
    description = models.CharField(
        max_length=72,
        blank=True,
        null=True
    )


    class Meta:
        abstract = True


class CategoryManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class HealthPersonnel(WorkforceBase):
    mesh = models.ForeignKey(
        'mesh.Mesh',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Category as a MeSH heading",
        related_name="category"
    )


class EdgeSet(models.Model):
    # Not required, but provides a convenient way of grouping Edges
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class NodeSet(models.Model):
    # Not required, but provides a convenient way of grouping Nodes
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class WorkforceNetworkedgeFacilities(models.Model):
    id = models.BigAutoField(primary_key=True)
    networkedge = models.ForeignKey(
        "workforce.NetworkEdge",
        models.DO_NOTHING
    )
    facility = models.ForeignKey(
        "facility.Facility",
        models.DO_NOTHING
    )
    public_facing = models.BooleanField(
        default=False,
        help_text=_("Should the user node included in this edge be public?")
    )

    class Meta:
        managed = True
        db_table = 'workforce_networkedge_facilities'
        unique_together = (('networkedge', 'facility'),)


class NetworkEdge(edge_factory("NetworkNode", concrete=False)):
    name = models.CharField(max_length=100, unique=True)
    edge_set = models.ForeignKey(
        EdgeSet,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="edge_set_edges",
    )
    facilities = models.ManyToManyField(
        'facility.Facility',
        through='WorkforceNetworkedgeFacilities',
    )

    def __str__(self):
        return f'{self.name} {[f.name for f in self.facilities.all()]}'

    def save(self, *args, **kwargs):
        self.name = f"{self.parent.name} {self.child.name}"
        super().save(*args, **kwargs)


class NetworkNode(node_factory(NetworkEdge)):
    name = models.CharField(max_length=100, unique=True)
    label = models.CharField(max_length=255, blank=True)
    mesh = models.ForeignKey(
        'mesh.Mesh',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    node_set = models.ForeignKey(
        NodeSet,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="node_set_nodes",
    )

    def __str__(self):
        return self.name


class Label(models.Model):


    class GrammaticalNumber(models.TextChoices):
        SINGULAR = 'S', _('Singular')
        PLURAL = 'P', _('Plural')


    class Languages(models.TextChoices):
        ENGLISH = 'en', _('English')
        FRENCH = 'fr', _('French')


    label = models.CharField(max_length=255)
    node = models.ForeignKey(
        'workforce.NetworkNode',
        on_delete=models.CASCADE,
        related_name="labels",
    )
    gender = models.ManyToManyField(
        'accounts.GrammaticalGender',
        related_name='labels',
    )
    grammatical_number = models.CharField(
        max_length=1,
        choices=GrammaticalNumber.choices,
        blank=True,
    )
    language = models.CharField(
        max_length=2,
        choices=Languages.choices,
        default=Languages.ENGLISH,
    )

    def __str__(self):
        return self.label
    
    @staticmethod
    def get_label(node: str, gender: str, number: str, language: str) -> str:
        try:
            node = NetworkNode.objects.get(name=node)
        except NetworkNode.DoesNotExist:
            return
        try:
            gender = GrammaticalGender.objects.get(name=gender)
        except GrammaticalGender.DoesNotExist:
            return
        try:
            label = Label.objects.get(
                node=node,
                gender=gender,
                grammatical_number=number,
                language=language
            )
            return label.label
        except Label.DoesNotExist as e:
            logger.debug(f'{e} for {node=}, {gender=}, {number=}, {language=}')
            return