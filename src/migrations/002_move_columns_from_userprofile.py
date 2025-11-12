"""Peewee migrations -- 002_move_columns_from_userprofile.py.

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
    
    migrator.add_fields(
        'user',

        biography=pw.CharField(max_length=256, default=""),
        website=pw.TextField(null=True))

    migrator.change_fields('user', username=pw.CharField(max_length=30, unique=True))

    migrator.change_fields('user', full_name=pw.CharField(max_length=80))

    migrator.change_fields('user', password=pw.CharField(max_length=256))

    migrator.change_fields('user', email=pw.CharField(max_length=256))

    migrator.sql("""
    UPDATE "user" SET biography = (SELECT p.biography FROM userprofile p WHERE p.user_id = id LIMIT 1), 
    website = (SELECT p.website FROM userprofile p WHERE p.user_id = id LIMIT 1);
    """)

    migrator.remove_fields('userprofile', 'year', 'instagram', 'facebook', 'telegram')


def rollback(migrator: Migrator, database: pw.Database, *, fake=False):
    """Write your rollback migrations here."""
    
    migrator.add_fields(
        'userprofile',

        year=pw.IntegerField(null=True),
        instagram=pw.TextField(null=True),
        facebook=pw.TextField(null=True),
        telegram=pw.TextField(null=True))

    migrator.remove_fields('user', 'biography', 'website')

    migrator.change_fields('user', username=pw.CharField(max_length=255, unique=True))

    migrator.change_fields('user', full_name=pw.TextField())

    migrator.change_fields('user', password=pw.CharField(max_length=255))

    migrator.change_fields('user', email=pw.CharField(max_length=255))
