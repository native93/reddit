# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################
@auth.requires_login()
def view_comment():
    no=request.args(0)
    c=db((db.comment.pid==no)&(db.auth_user.id==db.comment.author)).select()
    return dict(c=c,no=no)
@auth.requires_login()
def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html
    """
    c=db(db.category_table.id>0).select()
    return dict(c=c)
@auth.requires_login()
def post_comment():
    c=request.args(0)
    form=SQLFORM.factory(
        Field('comment_b','text'))                              
    if form.accepts(request.vars,session):
        db.comment.insert(comment_body=form.vars.comment_b,pid=c)
        redirect(URL('view_comment',args=c))
    elif form.errors:
        response.flash="Error"
    return dict(form=form)
@auth.requires_login()
def post_feed():
    form=SQLFORM(db.post)
    if form.accepts(request.vars,session):
        redirect(URL('index'))
    else:
        response.flash="Error"
    return dict(form=form)
@auth.requires_login()
def view_post():   
    no=request.args(0)
    p=db(db.post.category==no).select()
    return dict(p=p)
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
