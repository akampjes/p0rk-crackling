# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Task'
        db.create_table(u'porkweb_task', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('job', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['porkweb.Job'])),
            ('taskid', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('taskstatus', self.gf('django.db.models.fields.CharField')(default='New', max_length=16)),
            ('taskresults', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'porkweb', ['Task'])


    def backwards(self, orm):
        # Deleting model 'Task'
        db.delete_table(u'porkweb_task')


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
        },
        u'porkweb.task': {
            'Meta': {'object_name': 'Task'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['porkweb.Job']"}),
            'taskid': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'taskresults': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'taskstatus': ('django.db.models.fields.CharField', [], {'default': "'New'", 'max_length': '16'})
        }
    }

    complete_apps = ['porkweb']