from datetime import datetime
from gluon.utils import web2py_uuid
if session.secret_key is None:
    session.secret_key=web2py_uuid();
#database for boards
db.define_table('boards',
                Field('board_id', default = web2py_uuid(), readable=False, writable=False),
                Field('title', requires=IS_IN_SET({'Lunch','Activity','Forum', 'Support Group'})),
                #Field ('numberOfPosts', 'integer'),
                #Field('most_recent_post', 'datetime'),
                #Field('image', type='upload'),
                )
db.define_table('posts',
                Field('post_id', default = web2py_uuid(), readable=False, writable=False),
                Field('title','string'),
                Field('desc', 'text'),
                Field('created_on', 'datetime'),
                Field('board', 'reference boards', requires=IS_IN_DB(db((db.boards.title=='Lunch') |(db.boards.title=='Forum')),db.boards,'%(title)s')),
                Field('created_by','reference auth_user', default=auth.user_id),
                Field('stars','integer'),
                Field('company', 'reference companies', requires=IS_IN_DB(db,db.companies,'%(name)s')),#, default=auth.user.company),
                )

db.define_table('activities',
                Field('post_id', default = web2py_uuid(), readable=False, writable=False),
                Field('title','text'),
                Field('desc', 'text'),
                Field('created_on', 'datetime'),
                Field('start_time','datetime'),
                Field('end_time','datetime'),
                Field('board', 'reference boards', requires=IS_IN_DB(db((db.boards.title=='Activity')),db.boards,'%(title)s')),
                Field('image', type='upload', requires = IS_IMAGE(extensions=('jpeg', 'png'))),
                Field('created_by','reference auth_user', default=auth.user_id),
                Field('stars','integer'),
                Field('company', 'reference companies', requires=IS_IN_DB(db,db.companies,'%(name)s')),#, default=auth.user.company),
                )
db.define_table('support',
                Field('post_id', default = web2py_uuid(), readable=False, writable=False),
                Field('title','text'),
                Field('desc', 'text'),
                Field('created_on', 'datetime'),
                Field('start_time','datetime'),
                Field('end_time','datetime'),
                Field('board', 'reference boards', requires=IS_IN_DB(db((db.boards.title=='Support Group')),db.boards,'%(title)s')),
                Field('image', type='upload', requires = IS_IMAGE(extensions=('jpeg', 'png'))),
                Field('created_by','reference auth_user', default=auth.user_id),
                Field('stars','integer'),
                  Field('company', 'reference companies', requires=IS_IN_DB(db,db.companies,'%(name)s')),#, default=auth.user.company),
                )

db.define_table('messages',
                Field('msg_id', default = web2py_uuid(), readable=False, writable=False),
                Field('post', 'reference posts', requires=IS_IN_DB(db,db.posts,'%(title)s')),
                Field('created_by','reference auth_user', default=auth.user_id),
                Field('created_by_name','string', default=auth.user.name),
                Field('created_on', 'datetime'),
                Field('title','text'),
                Field('desc', 'text'),
                )

db.posts.created_on.default=datetime.utcnow()
db.activities.created_on.default=datetime.utcnow()
db.support.created_on.default=datetime.utcnow()
db.activities.start_time.default=datetime.utcnow()
db.support.start_time.default=datetime.utcnow()
db.activities.end_time.default=datetime.utcnow()
db.support.end_time.default=datetime.utcnow()
db.messages.created_on.default=datetime.utcnow()



