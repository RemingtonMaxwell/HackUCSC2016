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
                Field('title','text'),
                Field('desc', 'text'),
                Field('created_on', 'datetime'),
                Field('board', 'reference boards', requires=IS_IN_DB(db,db.boards,'%(title)s')),
                Field('image', type='upload'),
                Field('created_by','reference auth_user', default=auth.user_id),
                Field('stars','integer'),
                Field('company', 'reference companies', requires=IS_IN_DB(db,db.companies,'%(name)s')),#, default=auth.user.company),
                )

db.posts.created_on.default=datetime.utcnow()

