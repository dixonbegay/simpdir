# Simple and Important Managed Phone Directory

A phone directory that is LDAP compatible.

## Configuration

Use a .env file in the root directory to set environment variables that will be required. Below are instructions as to what needs to be configured. The `.env` file should be placed in `src` directory.

Set `LDAP_SUPERUSER_GROUP` to a distinguished name of a group that will be your superadmins.<br>
Example:`LDAP_SUPERUSER_GROUP=cn=admins,cn=groups,cn=accounts,dc=example,dc=com`

Example .env configuration.
```Dotenv
DEBUG=False
SECRET_KEY='django-insecure-$$$1234568$$$'
TIME_ZONE=America/Phoenix
ALLOWED_HOSTS_LISTS=localhost,.example.com

AUTH_LDAP_SERVER_URI=ldaps://172.64.159.3
AUTH_LDAP_BIND_AS_AUTHENTICATING_USER=True
AUTH_LDAP_BIND_DN=uid=ldapuser,cn=users,cn=accounts,dc=example,dc=com
AUTH_LDAP_BIND_PASSWORD=supersecret1234$

LDAP_TLS_REQUIRE_CERT=True
LDAP_BASE_DN=cn=users,cn=accounts,dc=example,dc=com
LDAP_GROUP_SEARCH=cn=groups,cn=accounts,dc=example,dc=com
LDAP_SUPERUSER_GROUP=cn=admins,cn=groups,cn=accounts,dc=example,dc=com
LDAP_IS_STAFF=cn=supervisors,cn=groups,cn=accounts,dc=example,dc=com

PHONENUMBER_DEFAULT_FORMAT=NATIONAL
PHONENUMBER_DEFAULT_REGION=US
```

NOTE: The group you specify in `LDAP_SUPERUSER_GROUP` will also be identified in the Django web application as staff as well, meaning `is_staff` will return true for each of these users. To change this behavior, you can edit the code in `src/conf/settings.py`. This was done because in order for users to access the Django admin portal by default, the user must also have `is_staff` set to true for each user object.

### Using Windows Active Directory?
Below is what you should set in the user-attributes-map.json file if your directory service is Windows Active Directory.

```json
"username": "sAMAccountName"
"department": "department"
```

### Using FreeIPA 4?
Below is what you should set in the user-attributes-map.json file if your directory service is FreeIPA. Tested with version 4.12.2.
```json
"username": "uid"
"department": "departmentNumber"
```

### Phone Number Format and Region Setting
When creating contacts, there are options that need to be set on how the phone numbers should be saved and formatted in the database.

Below are options of what `PHONENUMBER_DEFAULT_FORMAT` can be set to. Please [click here](https://django-phonenumber-field.readthedocs.io/en/stable/reference.html#settings-format-choices) for more details.
- `NATIONAL` - (xxx) xxx-xxxx
- `INTERNATIONAL` - +x xxx-xxx-xxxx
- `E.164` - +xxxxxxxxxxx
- `RFC3966` - tel:+x-xxx-xxx-xxxx

`PHONENUMBER_DEFAULT_REGION` should be set to a two-letter country code based on ISO-3166-1. This indicates how to interpret regional phone numbers. [List of current codes](https://en.wikipedia.org/wiki/ISO_3166-1#Current_codes).

Example configuration is below.
```
PHONENUMBER_DEFAULT_FORMAT=NATIONAL
PHONENUMBER_DEFAULT_REGION=US
```

## Developing and Contributing
To setup and load test data, do the following.<br>
1. Run `pipenv run python manage.py makemigrations`
2. Run `pipenv run python manage.py migrate`
3. Run `pipenv run python manage.py ldap_sync_users`
4. Run `pipenv run python manage.py loaddata db.json`
4. Run `pipenv run python manage.py runserver`