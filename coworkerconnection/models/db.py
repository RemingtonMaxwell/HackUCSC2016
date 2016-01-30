from gluon.tools import Auth
from images import RESIZE

db = DAL("sqlite://storage.sqlite")
auth = Auth(db)
db.define_table('companies',
                Field('name', 'string'),
                Field('website', 'string'),
                Field('email','string'),
                )
db.define_table(
    auth.settings.table_user_name,
    Field('name', length=128, default=''),
    Field('username', length=20, default='', unique=True),
    Field ('email', length=128, default='', unique=True),
    Field('password', 'password', length=512,            # required
          readable=False, label='Password'),
    Field('posts', writable=False),
    Field('bio', 'text'),
    Field('company','reference companies', requires=IS_IN_DB(db,db.companies,'%(name)s')),
    Field('picture', 'upload'),
    Field('registration_key', length=512,                # required
          writable=False, readable=False, default=''),
    Field('reset_password_key', length=512,              # required
          writable=False, readable=False, default=''),
    Field('registration_id', length=512,                 # required
          writable=False, readable=False, default=None))

custom_auth_table = db[auth.settings.table_user_name] # get the custom_auth_table
custom_auth_table.username.requires = [
    IS_NOT_IN_DB(db, custom_auth_table.email)]
custom_auth_table.picture.requires = [IS_EMPTY_OR(
    IS_LENGTH(minsize=0, maxsize=1048576,error_message='Please choose a picture smaller than 1MB')),
    IS_IMAGE(extensions=('gif', 'jpeg', 'jpg', 'png'), error_message = 'Invalid image type'),
    RESIZE(150,150)]
custom_auth_table.name.label = "Name"
custom_auth_table.password.requires = [CRYPT()]
custom_auth_table.email.requires = [
  IS_EMAIL(error_message=auth.messages.invalid_email),
  IS_NOT_IN_DB(db, custom_auth_table.email)]

auth.settings.table_user = custom_auth_table
auth.define_tables(username=True, signature=False)


auth.settings.login_captcha = False
auth.retrieve_username_captcha = False
auth.retrieve_password_captcha = False