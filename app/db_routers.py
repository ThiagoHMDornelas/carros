from django.conf import settings


class SimpleRouter:
    """
    Roteia tudo para o banco definido no .env (ACTIVE_DB)
    """

    def db_for_read(self, model, **hints):
        return settings.ACTIVE_DB

    def db_for_write(self, model, **hints):
        return settings.ACTIVE_DB

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return db == settings.ACTIVE_DB
