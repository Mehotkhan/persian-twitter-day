from mongoengine import Document, EmbeddedDocument, fields, register_connection
from tw_analysis.settings.local_settings import mongodb_authentication_source, mongodb_host, mongodb_password, \
    mongodb_username

alias_lists = ['stream_db']  # list of aliases
dbs = ['Analysis']  # list of databases
for alias, db in zip(alias_lists, dbs):
    register_connection(alias, db, authentication_source=mongodb_authentication_source, username=mongodb_username,
                        password=mongodb_password,
                        host=mongodb_host)


class Analysis(Document):
    meta = {
        "db_alias": "stream_db"
    }
    text = fields.StringField()
    username = fields.StringField()
    user_id = fields.IntField()
    user_screen_name = fields.StringField()
    create_date = fields.DateTimeField()
