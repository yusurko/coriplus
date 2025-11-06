"""Peewee migrations -- 001_0_9_to_0_10.py.

Some examples (model - class or model name)::

    > Model = migrator.orm['table_name']            # Return model in current state by name
    > Model = migrator.ModelClass                   # Return model in current state by name

    > migrator.sql(sql)                             # Run custom SQL
    > migrator.run(func, *args, **kwargs)           # Run python function with the given args
    > migrator.create_model(Model)                  # Create a model (could be used as decorator)
    > migrator.remove_model(model, cascade=True)    # Remove a model
    > migrator.add_fields(model, **fields)          # Add fields to a model
    > migrator.change_fields(model, **fields)       # Change fields
    > migrator.remove_fields(model, *field_names, cascade=True)
    > migrator.rename_field(model, old_field_name, new_field_name)
    > migrator.rename_table(model, new_table_name)
    > migrator.add_index(model, *col_names, unique=False)
    > migrator.add_not_null(model, *field_names)
    > migrator.add_default(model, field_name, default)
    > migrator.add_constraint(model, name, sql)
    > migrator.drop_index(model, *col_names)
    > migrator.drop_not_null(model, *field_names)
    > migrator.drop_constraints(model, *constraints)

"""

from contextlib import suppress

import peewee as pw
from peewee_migrate import Migrator


with suppress(ImportError):
    import playhouse.postgres_ext as pw_pext


def migrate(migrator: Migrator, database: pw.Database, *, fake=False):
    """Write your migrations here."""
    
    @migrator.create_model
    class BaseModel(pw.Model):
        id = pw.AutoField()

        class Meta:
            table_name = "basemodel"

    @migrator.create_model
    class User(pw.Model):
        id = pw.AutoField()
        username = pw.CharField(max_length=255, unique=True)
        full_name = pw.TextField()
        password = pw.CharField(max_length=255)
        email = pw.CharField(max_length=255)
        birthday = pw.DateField()
        join_date = pw.DateTimeField()
        is_disabled = pw.IntegerField()

        class Meta:
            table_name = "user"

    @migrator.create_model
    class Message(pw.Model):
        id = pw.AutoField()
        user = pw.ForeignKeyField(column_name='user_id', field='id', model=migrator.orm['user'])
        text = pw.TextField()
        pub_date = pw.DateTimeField()
        privacy = pw.IntegerField()

        class Meta:
            table_name = "message"

    @migrator.create_model
    class MessageUpvote(pw.Model):
        id = pw.AutoField()
        message = pw.ForeignKeyField(column_name='message_id', field='id', model=migrator.orm['message'])
        user = pw.ForeignKeyField(column_name='user_id', field='id', model=migrator.orm['user'])
        created_date = pw.DateTimeField()

        class Meta:
            table_name = "messageupvote"
            indexes = [(('message', 'user'), True)]

    @migrator.create_model
    class Notification(pw.Model):
        id = pw.AutoField()
        type = pw.TextField()
        target = pw.ForeignKeyField(column_name='target_id', field='id', model=migrator.orm['user'])
        detail = pw.TextField()
        pub_date = pw.DateTimeField()
        seen = pw.IntegerField()

        class Meta:
            table_name = "notification"

    @migrator.create_model
    class Relationship(pw.Model):
        id = pw.AutoField()
        from_user = pw.ForeignKeyField(column_name='from_user_id', field='id', model=migrator.orm['user'])
        to_user = pw.ForeignKeyField(column_name='to_user_id', field='id', model=migrator.orm['user'])
        created_date = pw.DateTimeField()

        class Meta:
            table_name = "relationship"
            indexes = [(('from_user', 'to_user'), True)]

    @migrator.create_model
    class Report(pw.Model):
        id = pw.AutoField()
        media_type = pw.IntegerField()
        media_id = pw.IntegerField()
        sender = pw.ForeignKeyField(column_name='sender_id', field='id', model=migrator.orm['user'], null=True)
        reason = pw.IntegerField()
        status = pw.IntegerField()
        created_date = pw.DateTimeField()

        class Meta:
            table_name = "report"

    @migrator.create_model
    class Upload(pw.Model):
        id = pw.AutoField()
        type = pw.TextField()
        message = pw.ForeignKeyField(column_name='message_id', field='id', model=migrator.orm['message'])

        class Meta:
            table_name = "upload"

    @migrator.create_model
    class UserAdminship(pw.Model):
        user = pw.ForeignKeyField(column_name='user_id', field='id', model=migrator.orm['user'], primary_key=True)

        class Meta:
            table_name = "useradminship"

    @migrator.create_model
    class UserProfile(pw.Model):
        user = pw.ForeignKeyField(column_name='user_id', field='id', model=migrator.orm['user'], primary_key=True)
        biography = pw.TextField()
        location = pw.IntegerField(null=True)
        year = pw.IntegerField(null=True)
        website = pw.TextField(null=True)
        instagram = pw.TextField(null=True)
        facebook = pw.TextField(null=True)
        telegram = pw.TextField(null=True)

        class Meta:
            table_name = "userprofile"


def rollback(migrator: Migrator, database: pw.Database, *, fake=False):
    """Write your rollback migrations here."""
    
    migrator.remove_model('userprofile')

    migrator.remove_model('useradminship')

    migrator.remove_model('upload')

    migrator.remove_model('report')

    migrator.remove_model('relationship')

    migrator.remove_model('notification')

    migrator.remove_model('messageupvote')

    migrator.remove_model('message')

    migrator.remove_model('user')

    migrator.remove_model('basemodel')
