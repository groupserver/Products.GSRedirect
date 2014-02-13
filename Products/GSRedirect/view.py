# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2014 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
from __future__ import absolute_import, unicode_literals
import logging
log = logging.getLogger('GSRedirect')
import time
from zope.component import getAdapter, ComponentLookupError
from Products.XWFMailingListManager.queries import MessageQuery
from zope.publisher.interfaces import IPublishTraverse
from zope.interface import implements
from OFS.Image import getImageInfo
from zExceptions import NotFound
from Products.XWFCore.XWFUtils import get_group_metadata_by_id
from .interfaces import IGSRedirectTraversal, IGSRedirect


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
                raise NotFound("Adapter not found: %s" % name)

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

        self.messageQuery = MessageQuery(self.context)


class GSRedirectBase(object):
    implements(IGSRedirect)

    def __init__(self, traverser):
        self.context = traverser.context
        self.request = traverser.request
        self.traverse_subpath = traverser.traverse_subpath


class GSRedirectTopic(GSMessageRedirectBase):
    def __call__(self):
        a = time.time()

        if len(self.traverse_subpath) == 1:
            postId = self.traverse_subpath[0]
            newPostId = self.messageQuery.post_id_from_legacy_id(postId)
            if newPostId:
                postId = newPostId
            post = self.messageQuery.post(postId)
            if post:
                try:
                    site_root = self.context.site_root()
                    s = getattr(site_root.Content, post['site_id'])  # lint:ok
                    g = getattr(s.groups, post['group_id'])  # lint:ok
                except AttributeError:
                    uri = '/topic-not-found?id=%s' % postId
                else:
                    uri = ('/groups/%s/messages/topic/%s' %
                                                  (post['group_id'],
                                                   postId))
            else:  # Cannot find topic
                uri = '/topic-not-found?id=%s' % postId
        else:  # Topic ID not specified
            uri = '/topic-no-id'

        b = time.time()
        log.debug("redirecting to: %s, took %.2f ms" % (uri, (b - a) * 1000.0))

        return self.request.RESPONSE.redirect(uri, 301)


class GSRedirectPost(GSMessageRedirectBase):
    def __call__(self):
        a = time.time()
        if len(self.traverse_subpath) == 1:
            postId = self.traverse_subpath[0]
            newPostId = self.messageQuery.post_id_from_legacy_id(postId)
            if newPostId:
                postId = newPostId
            post = self.messageQuery.post(postId)
            if post:
                group_metadata = get_group_metadata_by_id(self.context,
                                                        post['group_id'])
                if group_metadata:
                    uri = '/groups/%s/messages/post/%s' % (post['group_id'],
                                                            postId)
                else:
                    uri = '/post-not-found?id=%s' % postId
            else:  # Cannot find post
                uri = '/post-not-found?id=%s' % postId
        else:  # Post ID not specified
            uri = '/post-no-id'

        b = time.time()
        log.debug("redirecting to: %s, took %.2f ms" % (uri, (b - a) * 1000.0))

        return self.request.RESPONSE.redirect(uri, 301)


class GSRedirectFile(GSRedirectBase):
    def __call__(self):
        uri = ''
        if len(self.traverse_subpath) == 1:
            fileId = self.traverse_subpath[0]
            fileAttr = None
        elif len(self.traverse_subpath) >= 2:
            fileId = self.traverse_subpath[0]
            fileAttr = '/'.join(self.traverse_subpath[1:])
        else:  # File ID not specified
            uri = '/r/file-no-id'
            fileId = None
            fileAttr = None

        if not uri:
            result = self.context.FileLibrary2.find_files({'id': fileId})
            if result:
                file_object = result[0].getObject()
                groupId = file_object.group_ids[0]

                fileAttr = fileAttr or file_object.getProperty('title', '')
                uri = '/groups/%s/files/f/%s/%s' % (groupId, fileId,
                                            fileAttr)
            else:
                uri = '/file-not-found?id=%s' % fileId

        return self.request.RESPONSE.redirect(uri, 301)


class GSRedirectImage(GSRedirectBase):
    def __call__(self):
        uri = ''
        if len(self.traverse_subpath) == 1:
            fileId = self.traverse_subpath[0]
            fileAttr = None
        elif len(self.traverse_subpath) >= 2:
            fileId = self.traverse_subpath[0]
            fileAttr = '/'.join(self.traverse_subpath[1:])
        else:  # File ID not specified
            uri = '/r/file-no-id'
            fileId = None
            fileAttr = None

        if not uri:  # URI will be set on error
            result = self.context.FileLibrary2.find_files({'id': fileId})
            if result:
                file_object = result[0].getObject()
                contentType = getImageInfo(file_object.data)[0]
                if contentType:  # Is an image
                    groupId = file_object.group_ids[0]

                    fileAttr = fileAttr or file_object.getProperty('title', '')
                    uri = '/groups/%s/messages/image/%s' % (groupId, fileId)
                else:
                    groupId = file_object.group_ids[0]

                    fileAttr = fileAttr or file_object.getProperty('title', '')
                    uri = '/groups/%s/files/f/%s/%s' % (groupId, fileId,
                                                fileAttr)
            else:
                uri = '/file-not-found?id=%s' % fileId

        #assert type(uri) == str
        assert uri
        return self.request.RESPONSE.redirect(uri, 301)


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
            cs = self.context.Scripts
            groupMemberships = cs.get.group_memberships(groups)
            allGroups = []
            for groupType in groupMemberships.keys():
                allGroups = allGroups + groupMemberships[groupType]

            matchingGroups = [g.getId() for g in allGroups]
            if matchingGroups:
                group = matchingGroups[0]
                uri = '%s/%s' % (group.absolute_url(), rest)
            else:
                uri = '/group-not-found?id=%s' % groupId
        else:  # Group ID not specified
            uri = '/group-no-id'
        return self.request.RESPONSE.redirect(uri)
