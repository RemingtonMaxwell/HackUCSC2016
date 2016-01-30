from datetime import datetime
from gluon.utils import web2py_uuid
if session.secret_key is None:
    session.secret_key=web2py_uuid();
#database for boards
db.define_table('boards',
                Field('board_id', default = web2py_uuid(), readable=False, writable=False),
                Field('title', requires=IS_IN_SET({'Lunch','Activity','Forum'})),
                #Field ('numberOfPosts', 'integer'),
                #Field('most_recent_post', 'datetime'),
                #Field('image', type='upload'),
                )
db.define_table('posts',
                Field('post_id', default = web2py_uuid(), readable=False, writable=False),
                Field('title'),
                Field('desc', 'text'),
                Field('created_on', 'datetime'),
                Field('board', 'reference boards', requires=IS_IN_DB(db,db.boards,'%(title)s')),
                Field('last_update', 'datetime'),
                Field('created_by'),
                Field('image', type='upload'),
                Field('user_id'),
                Field('stars','integer'),
                Field('company', 'reference companies', requires=IS_IN_DB(db,db.companies,'%(name)s')),
                )
