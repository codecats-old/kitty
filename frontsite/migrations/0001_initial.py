# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table(u'frontsite_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='profile', unique=True, to=orm['auth.User'])),
        ))
        db.send_create_signal(u'frontsite', ['UserProfile'])

        # Adding model 'Avatar'
        db.create_table(u'frontsite_avatar', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('profile', self.gf('django.db.models.fields.related.OneToOneField')(related_name='avatar', unique=True, to=orm['frontsite.UserProfile'])),
        ))
        db.send_create_signal(u'frontsite', ['Avatar'])

        # Adding model 'VoteUserProfile'
        db.create_table(u'frontsite_voteuserprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_profile', self.gf('django.db.models.fields.related.ForeignKey')(related_name='votes', to=orm['frontsite.UserProfile'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='voted', to=orm['frontsite.UserProfile'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('strength', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1, blank=True)),
        ))
        db.send_create_signal(u'frontsite', ['VoteUserProfile'])

        # Adding model 'Category'
        db.create_table(u'frontsite_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'frontsite', ['Category'])

        # Adding model 'Rhyme'
        db.create_table(u'frontsite_rhyme', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='created_rhymes', to=orm['frontsite.UserProfile'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='rhymes', null=True, to=orm['frontsite.Category'])),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'frontsite', ['Rhyme'])

        # Adding model 'VoteRhyme'
        db.create_table(u'frontsite_voterhyme', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rhyme', self.gf('django.db.models.fields.related.ForeignKey')(related_name='votes', to=orm['frontsite.Rhyme'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rhyme_voted', to=orm['frontsite.UserProfile'])),
            ('data', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('strength', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1, blank=True)),
        ))
        db.send_create_signal(u'frontsite', ['VoteRhyme'])

        # Adding model 'Comment'
        db.create_table(u'frontsite_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('rhyme', self.gf('django.db.models.fields.related.ForeignKey')(related_name='comments', to=orm['frontsite.Rhyme'])),
            ('rhyme_author_saw', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='commented_rhymes', to=orm['frontsite.UserProfile'])),
        ))
        db.send_create_signal(u'frontsite', ['Comment'])

        # Adding model 'RhymeProfiles'
        db.create_table(u'frontsite_rhymeprofiles', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stored_rhymes', to=orm['frontsite.UserProfile'])),
            ('rhyme', self.gf('django.db.models.fields.related.ForeignKey')(related_name='profiles', to=orm['frontsite.Rhyme'])),
            ('position_no', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal(u'frontsite', ['RhymeProfiles'])


    def backwards(self, orm):
        # Deleting model 'UserProfile'
        db.delete_table(u'frontsite_userprofile')

        # Deleting model 'Avatar'
        db.delete_table(u'frontsite_avatar')

        # Deleting model 'VoteUserProfile'
        db.delete_table(u'frontsite_voteuserprofile')

        # Deleting model 'Category'
        db.delete_table(u'frontsite_category')

        # Deleting model 'Rhyme'
        db.delete_table(u'frontsite_rhyme')

        # Deleting model 'VoteRhyme'
        db.delete_table(u'frontsite_voterhyme')

        # Deleting model 'Comment'
        db.delete_table(u'frontsite_comment')

        # Deleting model 'RhymeProfiles'
        db.delete_table(u'frontsite_rhymeprofiles')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'frontsite.avatar': {
            'Meta': {'object_name': 'Avatar'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'profile': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'avatar'", 'unique': 'True', 'to': u"orm['frontsite.UserProfile']"})
        },
        u'frontsite.category': {
            'Meta': {'object_name': 'Category'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'frontsite.comment': {
            'Meta': {'object_name': 'Comment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'commented_rhymes'", 'to': u"orm['frontsite.UserProfile']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rhyme': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'to': u"orm['frontsite.Rhyme']"}),
            'rhyme_author_saw': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'frontsite.rhyme': {
            'Meta': {'object_name': 'Rhyme'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'created_rhymes'", 'to': u"orm['frontsite.UserProfile']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'rhymes'", 'null': 'True', 'to': u"orm['frontsite.Category']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'frontsite.rhymeprofiles': {
            'Meta': {'object_name': 'RhymeProfiles'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stored_rhymes'", 'to': u"orm['frontsite.UserProfile']"}),
            'position_no': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'rhyme': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'profiles'", 'to': u"orm['frontsite.Rhyme']"})
        },
        u'frontsite.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': u"orm['auth.User']"})
        },
        u'frontsite.voterhyme': {
            'Meta': {'object_name': 'VoteRhyme'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rhyme_voted'", 'to': u"orm['frontsite.UserProfile']"}),
            'data': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rhyme': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'votes'", 'to': u"orm['frontsite.Rhyme']"}),
            'strength': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'blank': 'True'})
        },
        u'frontsite.voteuserprofile': {
            'Meta': {'object_name': 'VoteUserProfile'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'voted'", 'to': u"orm['frontsite.UserProfile']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'strength': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'blank': 'True'}),
            'user_profile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'votes'", 'to': u"orm['frontsite.UserProfile']"})
        }
    }

    complete_apps = ['frontsite']