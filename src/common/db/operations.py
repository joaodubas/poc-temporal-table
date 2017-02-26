# encoding: utf-8
from django.db import migrations, models
from psycopg2.extensions import AsIs


def temporal_table(klass: models.Model) -> list:
    """Create sql operations to create a temporal table based in a given model.

    Args:
        klass (models.Model): model class that must have a temporal table.

    Returns:
        list: with migration operations to be performed.

    """
    table_name = AsIs(klass._meta.db_table)

    # NOTE (jpd): system period column
    fwd_column_sys_period = '''ALTER TABLE %s
    ADD COLUMN sys_period tstzrange NOT NULL
    DEFAULT tstzrange(current_timestamp, null);'''
    bwd_column_sys_period = 'ALTER TABLE %s DROP COLUMN sys_period;'

    # NOTE (jpd): historical table
    fwd_table_history = 'CREATE TABLE %s_history (LIKE %s)'
    bwd_table_history = 'DROP TABLE %s_history;'

    # NOTE (jpd): versioning trigger (where the magic happens)
    fwd_trigger_versioning ='''CREATE TRIGGER %s_versioning_trigger
    BEFORE INSERT OR UPDATE OR DELETE ON %s
    FOR EACH ROW EXECUTE PROCEDURE versioning(
        'sys_period', '%s_history', true
    );'''
    bwd_trigger_versioning = 'DROP TRIGGER %s_versioning_trigger'

    operations = [
        migrations.RunSQL(
            [(fwd_column_sys_period, (table_name,),)],
            [(bwd_column_sys_period, (table_name,),)]
        ),
        migrations.RunSQL(
            [(fwd_table_history, (table_name, table_name),)],
            [(bwd_table_history, (table_name,),)]
        ),
        migrations.RunSQL(
            [(fwd_trigger_versioning, (table_name, table_name, table_name),)],
            [(bwd_trigger_versioning, (table_name,),)]
        ),
    ]
    return operations


def json_gin_index(klass: models.Model, field_name: str) -> list:
    """Create gin index for json fields, using jsonb_path_ops.

    Args:
        klass (models.Model):
        field_name (str):

    Returns:
        list

    """
    table_name = AsIs(klass._meta.db_table)
    field_name = AsIs(field_name)
    fwd_index = 'CREATE INDEX %s_%s_gin ON %s USING GIN (%s jsonb_path_ops);'
    bwd_index = 'DROP INDEX %s_%s_gin;'
    operations = [
        migrations.RunSQL(
            [(fwd_index, [table_name, field_name, table_name, field_name])],
            [(bwd_index, [table_name, field_name])],
        )
    ]
    return operations
