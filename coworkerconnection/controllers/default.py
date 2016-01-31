# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################
from gluon.serializers import json

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    board_list=db(db.boards).select()
    post_list=db(db.posts).select()
    return dict(message=T('Welcome to web2py!'), board_list=board_list, post_list=post_list)

def show_messages_lunch():
    post=db(db.posts.post_id==request.args(0)).select().first()
    creator=db(db.auth_user.id==post.created_by).select().first()
    print creator.name
    msg_list=None
    if auth.user_id is not None:
        msg_list=db(db.messages.post==post).select(orderby=~db.messages.created_on)
    return dict(msg_list=msg_list, post=post, creator=creator.name)

def show_messages_support():
    post=db(db.support.post_id==request.args(0)).select().first()
    creator=db(db.auth_user.id==post.created_by).select().first()
    msg_list=None
    if auth.user_id is not None:
        msg_list=db(db.messagesSupport.post==post).select(orderby=~db.messagesSupport.created_on)
    return dict(msg_list=msg_list, post=post, creator=creator.name)

def show_messages_activities():
    post=db(db.activities.post_id==request.args(0)).select().first()
    creator=db(db.auth_user.id==post.created_by).select().first()
    msg_list=None
    if auth.user_id is not None:
        msg_list=db(db.messagesActivity.post==post).select(orderby=~db.messagesActivity.created_on)
    return dict(msg_list=msg_list, post=post, creator=creator.name)

def add_post():
    form=SQLFORM(db.posts, fields=['title', 'desc'])
    form.vars.company=auth.user.company
    form.vars.board=db(db.boards.title=='Lunch').select().first()
    if form.process().accepted:
        redirect(URL('default', 'lunch'))
    return dict(form=form)

def add_support_msg():
    form=SQLFORM(db.messagesSupport, fields=['title', 'desc'])
    post=db(db.support.post_id==request.args(0)).select().first()
    form.vars.post=post
    form.vars.created_by_name=auth.user.name
    if form.process().accepted:
        redirect(URL('default', 'show_messages_support',args=[post.post_id]))
    return dict(form=form)

def add_activities_msg():
    form=SQLFORM(db.messagesActivity, fields=['title', 'desc'])
    post=db(db.activities.post_id==request.args(0)).select().first()
    form.vars.post=post
    form.vars.created_by_name=auth.user.name
    if form.process().accepted:
        redirect(URL('default', 'show_messages_activities',args=[post.post_id]))
    return dict(form=form)

def add_lunch_msg():
    form=SQLFORM(db.messages, fields=['title', 'desc'])
    post=db(db.posts.post_id==request.args(0)).select().first()
    form.vars.post=post
    form.vars.created_by_name=auth.user.name
    print request.args(0)
    if form.process().accepted:
        redirect(URL('default', 'show_messages_lunch',args=[post.post_id]))
    return dict(form=form)

def add_post_activity():
    form=SQLFORM(db.activities, fields=['title', 'desc','image', 'start_time','end_time'])
    form.vars.company=auth.user.company
    form.vars.board=db(db.boards.title=='Activity').select().first()
    if form.process().accepted:
        redirect(URL('default', 'activities'))
    return dict(form=form)

def add_post_support():
    form=SQLFORM(db.support, fields=['title', 'desc','image', 'start_time','end_time'])
    form.vars.company=auth.user.company
    form.vars.board=db(db.boards.title=='Support Group').select().first()
    if form.process().accepted:
        redirect(URL('default', 'support'))
    return dict(form=form)

def lunch():
    board = db(db.boards.title=="Lunch").select().first()  #only lunch posts
    print board
    #company=db(db.posts.company==auth.user.company).select().first()
    post_list=None
    if not auth.user_id is None:
        company=db(db.companies.id==auth.user.company).select().first()
        post_list=db((db.posts.board==board)& (db.posts.company==company)).select(orderby=~db.posts.created_on)

    return dict(post_list=post_list)

def questions():
    board = db(db.boards.title=="Forum").select().first()  # get post ID from request
    post_list=db(db.posts.board==board).select(orderby=~db.posts.created_on)
    form=SQLFORM(db.posts, fields=['title','desc'])
    if not auth.user_id is None:
        form.vars.company=auth.user.company
    form.vars.board=db(db.boards.title=='Forum').select().first()
    if form.process().accepted:
        #session.flash=T('The post has been added')
        redirect(URL('default', 'questions'))
    return dict(post_list=post_list,form=form)

def activities():
    board = db(db.boards.title=="Activity").select().first()  # get post ID from request
   # print board
    post_list=None
    if not auth.user_id is None:
        company=db(db.companies.id==auth.user.company).select().first()
        post_list=db((db.activities.board==board)& (db.activities.company==company)).select(orderby=~db.activities.created_on)
    #print json(post_list)
    return dict(post_list=post_list,calendar=json(post_list))

def support():
    board = db(db.boards.title=="Support Group").select().first()
    post_list=None
    if auth.user_id is not None:
        company=db(db.companies.id==auth.user.company).select().first()
        post_list=db((db.support.board==board)& (db.support.company==company)).select(orderby=~db.support.created_on)
    return dict(post_list=post_list,calendar=json(post_list))

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


