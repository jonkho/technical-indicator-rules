# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Email_Collector'
        db.create_table('webapp_email_collector', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
        ))
        db.send_create_signal('webapp', ['Email_Collector'])


    def backwards(self, orm):
        
        # Deleting model 'Email_Collector'
        db.delete_table('webapp_email_collector')


    models = {
        'webapp.email_collector': {
            'Meta': {'object_name': 'Email_Collector'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['webapp']
