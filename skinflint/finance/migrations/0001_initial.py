# flake8: noqa
# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Budget'
        db.create_table('finance_budget', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('amount', self.gf('django.db.models.fields.IntegerField')()),
            ('balance', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('finance', ['Budget'])

        # Adding model 'Income'
        db.create_table('finance_income', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('amount', self.gf('django.db.models.fields.IntegerField')()),
            ('when', self.gf('django.db.models.fields.DateField')()),
            ('budget', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['finance.Budget'])),
        ))
        db.send_create_signal('finance', ['Income'])

        # Adding model 'Expense'
        db.create_table('finance_expense', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('amount', self.gf('django.db.models.fields.IntegerField')()),
            ('when', self.gf('django.db.models.fields.DateField')()),
            ('budget', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['finance.Budget'])),
        ))
        db.send_create_signal('finance', ['Expense'])


    def backwards(self, orm):
        # Deleting model 'Budget'
        db.delete_table('finance_budget')

        # Deleting model 'Income'
        db.delete_table('finance_income')

        # Deleting model 'Expense'
        db.delete_table('finance_expense')


    models = {
        'finance.budget': {
            'Meta': {'ordering': "('-amount',)", 'object_name': 'Budget'},
            'amount': ('django.db.models.fields.IntegerField', [], {}),
            'balance': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'finance.expense': {
            'Meta': {'ordering': "('when',)", 'object_name': 'Expense'},
            'amount': ('django.db.models.fields.IntegerField', [], {}),
            'budget': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['finance.Budget']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'when': ('django.db.models.fields.DateField', [], {})
        },
        'finance.income': {
            'Meta': {'ordering': "('when',)", 'object_name': 'Income'},
            'amount': ('django.db.models.fields.IntegerField', [], {}),
            'budget': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['finance.Budget']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'when': ('django.db.models.fields.DateField', [], {})
        }
    }

    complete_apps = ['finance']
