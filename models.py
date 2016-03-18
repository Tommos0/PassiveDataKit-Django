from __future__ import unicode_literals

import importlib

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.contrib.gis.db import models


def generator_label(identifier):
    for app in settings.INSTALLED_APPS:
        try:
            pdk_api = importlib.import_module(app + '.pdk_api')
            
            name = pdk_api.name_for_generator(identifier)
            
            if name is not None:
                return name
        except ImportError:
            pass
        except AttributeError:
            pass
            
    return generator_identifier


class DataPoint(models.Model):
    source = models.CharField(max_length=1024, db_index=True)
    generator = models.CharField(max_length=1024, db_index=True)
    generator_identifier = models.CharField(max_length=1024, db_index=True, default='unknown-generator')
    
    created = models.DateTimeField(db_index=True)
    generated_at = models.PointField(null=True)
    
    recorded = models.DateTimeField(db_index=True)
    
    properties = JSONField()

    
class DataBundle(models.Model):
    recorded = models.DateTimeField(db_index=True)
    properties = JSONField()
    
    processed = models.BooleanField(default=False, db_index=True)


class DataSourceGroup(models.Model):
    name = models.CharField(max_length=1024, db_index=True)        

    def __unicode__(self):
        return self.name


class DataSource(models.Model):
    identifier = models.CharField(max_length=1024, db_index=True)
    name = models.CharField(max_length=1024, db_index=True, unique=True)
    
    group = models.ForeignKey(DataSourceGroup, related_name='sources', null=True, on_delete=models.SET_NULL)
    
    def __unicode__(self):
        return self.name + ' (' + self.identifier + ')'
        
    def latest_point(self):
        return DataPoint.objects.filter(source=self.identifier).order_by('-created').first()
    
    def point_count(self):
        return DataPoint.objects.filter(source=self.identifier).count()
        
    def point_frequency(self):
        count = self.point_count()
        
        if count > 0:
            first = DataPoint.objects.filter(source=self.identifier).order_by('created').first()
            last = DataPoint.objects.filter(source=self.identifier).order_by('created').last()
            
            seconds = (last.created - first.created).total_seconds()
            
            return count / seconds
            
        return 0
    
    def generator_statistics(self):
        generators = []
        
        identifiers = DataPoint.objects.filter(source=self.identifier).order_by('generator_identifier').values_list('generator_identifier', flat=True).distinct()
        
        for identifier in identifiers:
            generator = {}
            
            generator['identifier'] = identifier
            generator['source'] = self.identifier
            generator['label'] = generator_label(identifier)
            
            generator['points_count'] = DataPoint.objects.filter(source=self.identifier, generator_identifier=identifier).count()
            
            first_point = DataPoint.objects.filter(source=self.identifier, generator_identifier=identifier).order_by('created').first()
            last_point = DataPoint.objects.filter(source=self.identifier, generator_identifier=identifier).order_by('-created').first()
            last_recorded = DataPoint.objects.filter(source=self.identifier, generator_identifier=identifier).order_by('-recorded').first()
        
            generator['last_recorded'] = last_recorded.recorded
            generator['first_created'] = first_point.created
            generator['last_created'] = last_point.created

            generator['frequency'] = float(generator['points_count']) / (last_point.created - first_point.created).total_seconds()
            
            generators.append(generator)
        
        return generators
        
class DataPointVisualizations(models.Model):
    source = models.CharField(max_length=1024, db_index=True)
    generator_identifier = models.CharField(max_length=1024, db_index=True)
    last_updated = models.DateTimeField(db_index=True)
