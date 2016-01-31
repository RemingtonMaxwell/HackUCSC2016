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

def add_post():
    form=SQLFORM(db.posts, fields=['title', 'desc','image', 'board'])
    form.vars.company=auth.user.company
    if form.process().accepted:
        session.flash=T('The post has been added')
        redirect(URL('default', 'index'))
    return dict(form=form)
def add_post_activity():
    form=SQLFORM(db.activities, fields=['title', 'desc','image', 'start_time','end_time'])
    form.vars.company=auth.user.company
    form.vars.board=db(db.boards.title=='Activity').select().first()
    if form.process().accepted:
        session.flash=T('The post has been added')
        redirect(URL('default', 'index'))
    return dict(form=form)

def lunch():
    board = db(db.boards.title=="Lunch").select().first()  #only lunch posts
    print board
    #company=db(db.posts.company==auth.user.company).select().first()
   # print company
    post_list=db(db.posts.board==board).select()
    return dict(post_list=post_list)

def questions():
    board = db(db.boards.title=="Forum").select().first()  # get post ID from request
    print board
    post_list=db(db.posts.board==board).select()
    return dict()

def activities():
    board = db(db.boards.title=="Activity").select().first()  # get post ID from request
   # print board
    post_list=None
    if auth.user_id is not None:
        company=db(db.companies.id==auth.user.company).select().first()
    #print company

   # print posts.com
        post_list=db((db.activities.board==board)& (db.activities.company==company)).select()

    return dict(post_list=post_list,calendar=json(post_list))

def support():
    board = db(db.boards.title=="Support Group").select().first()
    post_list=None
    if auth.user_id is not None:
        company=db(db.companies.id==auth.user.company).select().first()
    #print company

   # print posts.com
        post_list=db((db.support.board==board)& (db.support.company==company)).select()

    return dict(post_list=post_list)

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


