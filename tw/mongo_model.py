from mongoengine import Document, EmbeddedDocument, fields, register_connection
from tw_analysis.settings.local_settings import mongodb_authentication_source, mongodb_host, mongodb_password, \
    mongodb_username, mongodb_port

alias_lists = ['stream_db']  # list of aliases
dbs = ['Analysis']  # list of databases
for alias, db in zip(alias_lists, dbs):
    register_connection(alias, db, authentication_source=mongodb_authentication_source, username=mongodb_username,
                        password=mongodb_password,
                        host=mongodb_host, port=mongodb_port)


class Analysis(Document):
    meta = {
        "db_alias": "stream_db"
    }
    tweet_id = fields.IntField()
    text = fields.StringField()
    clean_text = fields.ListField()
    user_name = fields.StringField()
    user_id = fields.IntField()
    user_screen_name = fields.StringField()
    user_location = fields.StringField()
    user_created_at = fields.DateTimeField()
    user_description = fields.StringField()
    user_followers_count = fields.IntField()
    user_friends_count = fields.IntField()
    user_statuses_count = fields.IntField()
    user_favourites_count = fields.IntField()
    create_date = fields.DateTimeField()
    create_date_timestamp_ms = fields.IntField()
    source = fields.StringField()
    media_type = fields.DynamicField()
    is_quote_status = fields.BooleanField()
