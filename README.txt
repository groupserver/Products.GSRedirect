=======================
``Products.GSRedirect``
=======================
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Redirect folder for GroupServer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2014-02-13
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 3.0 New Zealand License`_
  by `OnlineGroups.Net`_.

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

* Topics ``/r/topic``,
* Posts ``/r/post/``,
* Files ``/r/file/``, and
* Images ``r/img/``.

The links are made available through the share widget [#share]_.

TODO
====

This product should be broken up. Only the base marker-interface should be
provided by a new ``gs.redirect`` product. The redirectors for topics
[#topics]_, post [#posts]_, files [#files]_ and images [#images]_ should be
provided by their respective products.

Resources
=========

- Code repository: https://source.iopen.net/groupserver/Products.GSRedirect
- Questions and comments to http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net
.. _Michael JasonSmith: http://groupserver.org/p/mpj17
.. _Creative Commons Attribution-Share Alike 3.0 New Zealand License:
   http://creativecommons.org/licenses/by-sa/3.0/nz/

.. [#share] See <https://source.iopen.net/groupserver/gs.content.js.sharebox>
.. [#topics] See <https://source.iopen.net/groupserver/gs.group.messages.topic>
.. [#posts] See <https://source.iopen.net/groupserver/gs.group.messages.post>
.. [#files] See <https://source.iopen.net/groupserver/gs.group.messages.file>
.. [#images] See <https://source.iopen.net/groupserver/gs.group.messages.images>

..  LocalWords:  redirector redirectors
