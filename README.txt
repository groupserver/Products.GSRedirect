Introduction
============

The redirector is a folder, ``/r``, that is used in URLs that are shorter
than normal, especially those to do with groups. For example, rather than
using the URL
<http://groupserver.org/groups/development/messages/topic/mgEw4smZbOJqZGouMHYsg>
the much shorter URL <http://groupserver.org/r/topic/mgEw4smZbOJqZGouMHYsg>
is used.

This product provides support for the redirect folder itself, and the
redirectors for

* Topics,
* Posts,
* Files, and
* Images.

TODO
====

This product should be broken up. Only the base marker-interface should be
provided by a new ``gs.redirect`` product. The redirectors for topics,
post, files and images should be provided by their respective products.

..  LocalWords:  redirector redirectors
