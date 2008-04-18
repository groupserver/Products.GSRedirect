import zope.component, zope.publisher.interfaces
from zope.interface.interface import Interface

import zope.viewlet.interfaces, zope.contentprovider.interfaces 
from zope.schema import *
from zope.interface.interface import Interface

class IGSRedirect(Interface):
    """Redirector for GroupServer
    
    DESCRIPTION
        The redirector maps from a short-URI for a object to the full
        URI for the object. This is necessary because the URIs for posts,
        topics and files, can get too long to fit in an email message, so
        often short-URIs are passed around instead.
        
        A redirector is installed, with the name "r", in the "Content"
        object of a GroupServer installation. The redirector supports three
        "pages":
          * post,
          * topic, and
          * files.
        Each of these "pages" is mapped onto the three methods below, with
        the ID extracted from the URI by traversal-magic. The error-pages
        should be provided in the ZMI.
    """
    
    def post(postId):
        """Redirect to the view of a single post
        
        ARGUMENTS
            "postId"  The identifier of the post.
        
        RETURNS
            A redirect to the page that will display the post. If the post
            with the specified identifier cannot be found, the user will
            be redirected to "/r/post-not-found". If "postId" is not 
            specified, then the user is redirected to "/r/post-no-id".
        
        SIDE EFFECTS
            None
        """
                
    def topic(postId):
        """Redirect to the view of a topic

        ARGUMENTS
            "postId"  The identifier of a post in the topic.
        
        RETURNS
            A redirect to the page that will display the topic.If the post
            with the specified identifier cannot be found, the user will
            be redirected to "/r/topic-not-found". If "postId" is not 
            specified, then the user is redirected to "/r/topic-no-id".
        
        SIDE EFFECTS
            None
        """
        
    def file(fileId):
        """Redirect to a file

        ARGUMENTS
            "fileId"  The identifier of the file.
        
        RETURNS
            A redirect to the file. If the file with the specified
            identifier cannot be found, the user will be redirected to
            "/r/file-not-found". If "postId" is not specified, then the user
            is redirected to "/r/file-no-id".
        
        SIDE EFFECTS
            None
        
        """

    def group(partialGroupId):
        """Redirect to a group
        
        DESCRIPTION
            This redirector sends the user to the group whose ID matches
            "partialGroupId". The system is not sophisticated: it does a 
            simple substring match on the identifiers of the user's groups,
            redirecting the user to the first group that matches.

        ARGUMENTS
            "partialGroupId"  A group-identifier substring.
        
        RETURNS
            A redirect to a group. If no group matches the specified
            substring then the user will be redirected to
            "/r/group-not-found". If "partialGroupId" is not specified, then 
            the user is redirected to "/r/group-no-id".
        
        SIDE EFFECTS
            None
        
        """
        
class IGSRedirectForFolder(Interface):
    pass
