'''GroupServer Page-Redirector
'''
from Products.Five.traversable import Traversable
from Products.XWFMailingListManager import queries
from interfaces import IGSRedirect
from zope.app.traversing.interfaces import ITraversable
from zope.interface import implements

import Products.Five, Globals

class GSRedirect(Products.Five.BrowserView, Traversable):
    implements(IGSRedirect, ITraversable)
    
    def __init__(self, context, request):
        self.context = context
        self.request = request

        request.form['subpaths'] = []
        
        da = self.context.zsqlalchemy
        assert da, 'No data-adaptor found'
        
        self.messageQuery = queries.MessageQuery(self.context, da)
      
    def traverse(self, name, furtherPath):
        self.request.form['subpaths'].append(name)
        
        return self

    def post(self):
        if len(self.request.form['subpaths']) == 1:
            postId = self.request.form['subpaths'][0]
            newPostId = self.messageQuery.post_id_from_legacy_id(postId)
            if newPostId:
                postId = newPostId
            post = self.messageQuery.post(postId)
            if post:
                group = self.context.Scripts.get.group_by_id(post['group_id'])
                if group:
                    uri = '%s/messages/post/%s' % (group.absolute_url(), postId)
                else:
                    uri = '/r/%s?id=%s' % (self.postNotFoundId, postId)
            else: # Cannot find post
                uri = '/r/post-not-found?id=%s' % postId
        else: # Post ID not specified
            uri = '/r/post-no-id'
        return self.request.RESPONSE.redirect(uri)
        
    def topic(self):
        if len(self.request.form['subpaths']) == 1:
            postId = self.request.form['subpaths'][0]
            newPostId = self.messageQuery.post_id_from_legacy_id(postId)
            if newPostId:
                postId = newPostId
            post = self.messageQuery.post(postId)
            if post:
                group = self.context.Scripts.get.group_by_id(post['group_id'])
                if group:
                    uri = '%s/messages/topic/%s' % (group.absolute_url(), postId)
                else:
                    uri = '/r/topic-not-found?id=%s' % postId
            else: # Cannot find topic
                uri = '/r/topic-not-found?id=%s' % postId
        else: # Topic ID not specified
            uri = '/r/topic-no-id'
        return self.request.RESPONSE.redirect(uri)

    def file(self):
        uri = ''
        if len(self.request.form['subpaths']) == 1:
            fileId = self.request.form['subpaths'][0]
            fileName = None
        elif len(self.request.form['subpaths']) == 2:
            fileId, fileName = self.request.form['subpaths'][0:]            
        else: # File ID not specified
            uri = '/r/file-no-id'
            fileId = None
            fileName = None
            
        if not uri:
            result = self.context.FileLibrary2.find_files({'id': fileId})
            if result:
                file_object = result[0].getObject()
                groupId = file_object.group_ids[0]
                group = self.context.Scripts.get.group_by_id(groupId)
            
                fileName = fileName or file_object.getProperty('title','')
                uri = '%s/files/f/%s/%s' % (group.absolute_url(), fileId, 
                                            fileName)
            else:
                uri = '/r/file-not-found?id=%s' % fileId
        
        return self.request.RESPONSE.redirect(uri)

    def group(self):
        subpaths = self.request.form['subpaths']
        if len(subpaths) >= 1:
            groupId = subpaths[0]
            
            rest = ''
            if (len(subpaths) >= 2):
              rest = '/'.join(subpaths[1:])
            
            ## --=mpj17=-- The call to "group_memberships" and 
            ##   "groups_object" need replacing.
            groups = self.context.Scripts.get.groups_object()            
            groupMemberships = self.context.Scripts.get.group_memberships(groups)
            allGroups = []
            for groupType in groupMemberships.keys():
                allGroups = allGroups + groupMemberships[groupType]

            matchingGroups = filter(lambda g: groupId in g.getId(), 
                                    allGroups)
            if matchingGroups:
                group = matchingGroups[0]
                uri = '%s/%s' % (group.absolute_url(), rest)
            else:
                uri = '/r/group-not-found?id=%s' % groupId
        else: # Group ID not specified
            uri = '/r/group-no-id'
        return self.request.RESPONSE.redirect(uri)

Globals.InitializeClass( GSRedirect )
