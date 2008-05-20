'''GroupServer Page-Redirector
'''
from zope.component import getMultiAdapter, getAdapter, ComponentLookupError
from Products.XWFMailingListManager import queries
from interfaces import IGSRedirectTraversal, IGSRedirect
from zope.publisher.interfaces import IPublishTraverse
from zope.interface import implements

from zExceptions import NotFound

import Products.Five, Globals

import logging
log = logging.getLogger('GSRedirect')

class GSRedirectTraversal(object):
    implements(IGSRedirectTraversal, IPublishTraverse)
    
    def __init__(self, context, request):
        self.context = context
        self.request = request
        
        self.traverse_subpath = []

    def __call__(self):
        if self.traverse_subpath:
            # get a named adapter
            name = self.traverse_subpath.pop(0)
            try:
                return getAdapter(self, IGSRedirect, name=name)()
            except ComponentLookupError:
                raise NotFound

        raise NotFound

    def publishTraverse(self, request, name):
        self.traverse_subpath.append(name)

        return self

class GSMessageRedirectBase(object):
    implements(IGSRedirect)
    def __init__(self, traverser):
        self.context = traverser.context
        self.request = traverser.request
        self.traverse_subpath = traverser.traverse_subpath

        da = self.context.zsqlalchemy
        assert da, 'No data-adaptor found'
        
        self.messageQuery = queries.MessageQuery(self.context, da)

class GSRedirectBase(object):
    implements(IGSRedirect)
    def __init__(self, traverser):
        self.context = traverser.context
        self.request = traverser.request
        self.traverse_subpath = traverser.traverse_subpath

class GSRedirectTopic(GSMessageRedirectBase):
    def __call__(self):
        if len(self.traverse_subpath) == 1:
            postId = self.traverse_subpath[0]
            newPostId = self.messageQuery.post_id_from_legacy_id(postId)
            if newPostId:
                postId = newPostId
            post = self.messageQuery.post(postId)
            if post:
                group = self.context.Scripts.get.group_by_id(post['group_id'])
                if group:
                    uri = '%s/messages/topic/%s' % (group.absolute_url(),
                                                    postId)
                else:
                    uri = '/topic-not-found?id=%s' % postId
            else: # Cannot find topic
                uri = '/topic-not-found?id=%s' % postId
        else: # Topic ID not specified
            uri = '/topic-no-id'

        log.info("redirecting to: %s" % uri)

        return self.request.RESPONSE.redirect(uri)

class GSRedirectPost(GSMessageRedirectBase):
    def __call__(self):
        if len(self.traverse_subpath) == 1:
            postId = self.traverse_subpath[0]
            newPostId = self.messageQuery.post_id_from_legacy_id(postId)
            if newPostId:
                postId = newPostId
            post = self.messageQuery.post(postId)
            if post:
                group = self.context.Scripts.get.group_by_id(post['group_id'])
                if group:
                    uri = '%s/messages/post/%s' % (group.absolute_url(), postId)
                else:
                    uri = '/post-not-found?id=%s' % postId
            else: # Cannot find post
                uri = '/post-not-found?id=%s' % postId
        else: # Post ID not specified
            uri = '/post-no-id'

        log.info("redirecting to: %s" % uri)

        return self.request.RESPONSE.redirect(uri)

class GSRedirectFile(GSRedirectBase):
    def __call__(self):
        uri = ''
        if len(self.traverse_subpath) == 1:
            fileId = self.traverse_subpath[0]
            fileName = None
        elif len(self.traverse_subpath) == 2:
            fileId, fileName = self.traverse_subpath[0:]            
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
                uri = '/file-not-found?id=%s' % fileId
        
        return self.request.RESPONSE.redirect(uri)

class GSRedirectGroup(GSRedirectBase):
    def __call__(self):
        subpaths = self.traverse_subpath
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
                uri = '/group-not-found?id=%s' % groupId
        else: # Group ID not specified
            uri = '/group-no-id'
        return self.request.RESPONSE.redirect(uri)

