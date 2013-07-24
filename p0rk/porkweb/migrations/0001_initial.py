# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'JobServer'
        db.create_table(u'porkweb_jobserver', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ipaddr', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('port', self.gf('django.db.models.fields.IntegerField')(default=8117)),
            ('hostname', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('os', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('status', self.gf('django.db.models.fields.CharField')(default='Offline', max_length=16)),
            ('details', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'porkweb', ['JobServer'])

        # Adding model 'AttackType'
        db.create_table(u'porkweb_attacktype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'porkweb', ['AttackType'])

        # Adding model 'Param'
        db.create_table(u'porkweb_param', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal(u'porkweb', ['Param'])

        # Adding model 'AttackParam'
        db.create_table(u'porkweb_attackparam', (
            (u'param_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['porkweb.Param'], unique=True, primary_key=True)),
            ('attack', self.gf('django.db.models.fields.related.ForeignKey')(related_name='params', to=orm['porkweb.AttackType'])),
        ))
        db.send_create_signal(u'porkweb', ['AttackParam'])

        # Adding model 'JobParam'
        db.create_table(u'porkweb_jobparam', (
            (u'param_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['porkweb.Param'], unique=True, primary_key=True)),
            ('job', self.gf('django.db.models.fields.related.ForeignKey')(related_name='params', to=orm['porkweb.Job'])),
        ))
        db.send_create_signal(u'porkweb', ['JobParam'])

        # Adding model 'HashType'
        db.create_table(u'porkweb_hashtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('hashcatType', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('hashcat', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('ocllite', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('oclplus', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'porkweb', ['HashType'])

        # Adding model 'Cracked'
        db.create_table(u'porkweb_cracked', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('when', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('hash', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('job', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['porkweb.Job'])),
        ))
        db.send_create_signal(u'porkweb', ['Cracked'])

        # Adding model 'Job'
        db.create_table(u'porkweb_job', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hashes', self.gf('django.db.models.fields.TextField')()),
            ('hashType', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['porkweb.HashType'])),
            ('attackType', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['porkweb.AttackType'])),
            ('jobServer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['porkweb.JobServer'], null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='New', max_length=16)),
            ('progress', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('started', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('finished', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('eta', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('results', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('speed', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'porkweb', ['Job'])

        # Adding model 'Log'
        db.create_table(u'porkweb_log', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('when', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('line', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'porkweb', ['Log'])


    def backwards(self, orm):
        # Deleting model 'JobServer'
        db.delete_table(u'porkweb_jobserver')

        # Deleting model 'AttackType'
        db.delete_table(u'porkweb_attacktype')

        # Deleting model 'Param'
        db.delete_table(u'porkweb_param')

        # Deleting model 'AttackParam'
        db.delete_table(u'porkweb_attackparam')

        # Deleting model 'JobParam'
        db.delete_table(u'porkweb_jobparam')

        # Deleting model 'HashType'
        db.delete_table(u'porkweb_hashtype')

        # Deleting model 'Cracked'
        db.delete_table(u'porkweb_cracked')

        # Deleting model 'Job'
        db.delete_table(u'porkweb_job')

        # Deleting model 'Log'
        db.delete_table(u'porkweb_log')


    models = {
        u'porkweb.attackparam': {
            'Meta': {'object_name': 'AttackParam', '_ormbases': [u'porkweb.Param']},
            'attack': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'params'", 'to': u"orm['porkweb.AttackType']"}),
            u'param_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['porkweb.Param']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'porkweb.attacktype': {
            'Meta': {'object_name': 'AttackType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'porkweb.cracked': {
            'Meta': {'object_name': 'Cracked'},
            'hash': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['porkweb.Job']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'when': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'porkweb.hashtype': {
            'Meta': {'object_name': 'HashType'},
            'hashcat': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hashcatType': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'ocllite': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'oclplus': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'porkweb.job': {
            'Meta': {'object_name': 'Job'},
            'attackType': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['porkweb.AttackType']"}),
            'eta': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'finished': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'hashType': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['porkweb.HashType']"}),
            'hashes': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jobServer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['porkweb.JobServer']", 'null': 'True', 'blank': 'True'}),
            'progress': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'results': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'speed': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'started': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'New'", 'max_length': '16'})
        },
        u'porkweb.jobparam': {
            'Meta': {'object_name': 'JobParam', '_ormbases': [u'porkweb.Param']},
            'job': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'params'", 'to': u"orm['porkweb.Job']"}),
            u'param_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['porkweb.Param']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'porkweb.jobserver': {
            'Meta': {'object_name': 'JobServer'},
            'details': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'hostname': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ipaddr': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'os': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'port': ('django.db.models.fields.IntegerField', [], {'default': '8117'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Offline'", 'max_length': '16'})
        },
        u'porkweb.log': {
            'Meta': {'object_name': 'Log'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line': ('django.db.models.fields.TextField', [], {}),
            'when': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'porkweb.param': {
            'Meta': {'object_name': 'Param'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['porkweb']