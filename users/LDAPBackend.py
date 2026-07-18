import logging

from django_auth_ldap.backend import LDAPBackend

logger = logging.getLogger(__name__)


# Just a place holder. Not used.
class CustomLDAPBackend(LDAPBackend):
    def get_or_build_user(self, username, ldap_user):
        """
        This must return a (User, built) 2-tuple for the given LDAP user.

        username is the Django-friendly username of the user. ldap_user.dn is
        the user's DN and ldap_user.attrs contains all of their LDAP
        attributes.

        The returned User object may be an unsaved model instance.

        """
        model = self.get_user_model()
        logger.debug("==== CustomLDAPBackend - ldap_user.attrs ====")
        # for key, value in ldap_user.attrs.items():
        #     logger.debug(f"{key}: {value}")

        if self.settings.USER_QUERY_FIELD:
            query_field = self.settings.USER_QUERY_FIELD
            logger.debug(f"query_field: {query_field}")
            query_value = ldap_user.attrs[self.settings.USER_ATTR_MAP[query_field]][0]
            logger.debug(query_value)
            lookup = query_field
        else:
            query_field = model.USERNAME_FIELD
            query_value = username.lower()
            lookup = "{}__iexact".format(query_field)

        try:
            user = model.objects.get(**{lookup: query_value})
        except model.DoesNotExist:
            user = model(**{query_field: query_value})
            built = True
        else:
            built = False

        return (user, built)
