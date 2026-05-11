import ldap
from django.core.management.base import BaseCommand
from django.db import transaction
from django_auth_ldap import backend
from django_auth_ldap import config as LDAPconfig


class Command(BaseCommand):
    help = "Creates local user models for users found in the remote LDAP server."

    def add_arguments(self, parser):
        parser.add_argument(
            "lookups",
            nargs="*",
            type=str,
            help="A list of lookups to be looked up in the directory service.",
        )
        return super().add_arguments(parser)

    @transaction.atomic()
    def handle(self, *args, **kwargs):
        verbosity = int(kwargs.get("verbosity", 1))
        lookups = kwargs.get("lookups", [])
        ldap_backend = backend.LDAPBackend()

        if len(lookups) < 1:
            ldap_connection = ldap_backend.ldap.initialize(
                LDAPconfig.settings.AUTH_LDAP_SERVER_URI, bytes_mode=0
            )
            ldap_connection.simple_bind_s(
                LDAPconfig.settings.AUTH_LDAP_BIND_DN,
                LDAPconfig.settings.AUTH_LDAP_BIND_PASSWORD,
            )
            results = ldap_connection.search_s(
                LDAPconfig.settings.LDAP_BASE_DN,
                ldap.SCOPE_SUBTREE,
                "(objectClass=person)",
            )
            count = 0
            for dn, entry in results:
                print("Results: {results}")
                if not dn:
                    continue
                username = entry.get(LDAPconfig.settings.LDAP_USER_LOOKUP_FIELD, [b""])[
                    0
                ].decode("utf-8")

                if username:
                    # This triggers the django-auth-ldap population logic
                    user = ldap_backend.populate_user(username)
                    if user:
                        self.stdout.write(f"Synced: {username}")
                        count += 1

            self.stdout.write(self.style.SUCCESS(f"Successfully synced {count} users."))
        else:
            for username in lookups:
                user = ldap_backend.populate_user(username)
                if verbosity >= 1:
                    self.stdout.write("Synch {user}".format(user=user))
