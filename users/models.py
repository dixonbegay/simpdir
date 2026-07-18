from django.contrib.auth.models import AbstractUser
from django.db import models


class LDAPuser(AbstractUser):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=128)
    telephoneNumber = models.CharField(max_length=21)
    mobile = models.CharField(max_length=24)
    department = models.CharField(max_length=80)

    def __str__(self):
        return self.username


# Below is a helper to inspect LDAP user data before saving.
# @receiver(pre_save, sender=LDAPuser)
# def set_ldap_properties(sender, instance, raw, using, update_fields, **kwargs):
#     print("Sender: ", sender)
#     print("==== Instance type ====")
#     print(type(instance))
#     print("==== Dumping LDAP user instance ====")
#     print(instance)
#     print("instance.description: ", instance.description)
#     print("raw: ", raw)
#     print("using: ", using)
#     print("update_fields: ", update_fields)
