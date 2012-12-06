Introduction
============

This add-on contains core controller to build gallery addons for Plone.

The goals are:

* Have a simple photo fetchers component in one API
* Support many photos providers (picasa, flickr, ...)
* Stay as simple as possible

How to install
==============

This addon can be installed as any other addon. Please follow the official
documentation.

Upgrade from 1.X
----------------

If you migrate from 1.X, you should add an other addon like collective.galleria.
Note that Galleriffic is deprecated.

To cleanup you plonesite, you can call @@collective.gallery.zclean has
administrator or use the profile 'zclean'.

Components (Backend)
====================

Summary:

* No custom content type, only views
* Works with lots of photos (is developed to work with +300 photos)
* Ramcache setup with a default key to one hours + modification date
* Works with Folder, Topic and Link content types
* picasaweb_ and flickr_ support.
* facebook support.
* I18N: english, french, german and italian are available

collective.gallery use zope.components to provide as much reusable components
as possible.

First we have photo resources. Plone already manage this for you:

* Folder can contains Image
* Topic can be criterized to list only Image content type
* Link can be sources of photos throw picasaweb.google.com and flickr.com services.

Next you have the main component: IGallery.
This interface is implemented at two levels:

* As named adapter over IATLink to get photos from picasaweb or flickr or facebook.
* As browserview to control the resource (@@gallery)

Folder & Image
--------------

Folder and Image content type can be used to build a gallery. Add a folder and
then add every images in it. Once its done come up to the folder and choose
'Gallery view' in the display drop down menu and voila.

The folder gallery component query the portal_catalog and adapts brains to
IPhoto.

Topic & Image
-------------

Topic can be used to build a gallery. Add a topic and add criteria on the Type
to select only Image. Next choose the 'Gallery view' in the drop down menu and
voila.

The topic gallery component use the topic's queryCatalog method to get brains,
then they are adapted to IPhoto

Link
----

Link can be used to build a gallery. Add a link, set URL to one of the following
services, validate and choose the 'Gallery view' in the drop down menu and
voila.

The link gallery component get all named adapters from Link to IGallery and call
the validate method. The first validated adapter is kept as resources.

picasaweb_
~~~~~~~~~~

In Plone, just paste the share link provided by picasaweb inside a Link content
type and display your link content with the view 'Gallery view' available in the
drop down display menu.

SIZES : 32, 48, 64, 72, 104, 144, 150, 160, 94, 110, 128, 200, 220, 288, 320,
          400, 512, 576, 640, 720, 800, 912, 1024, 1152, 1280, 1440, 1600

All metadatas are supported

Link supported are:

* http://picasaweb.google.XX/userid/albumname
* https://picasaweb.google.XX/userid/albumname
* https://picasaweb.google.XX/userid/privatealbumname?authkey=AUTHKEY

flickr_
~~~~~~~

In Plone, just paste the share link provided by flickr inside a Link content
type and display your link content with the view gallery available in the drop down display menu.

Flickr service is not album centric but photo centric. Supported case:

  http://www.flickr.com/photos/autowitch/sets/107460
  It is an album, no problem

  http://www.flickr.com/photos/rbpdesigner
  We have the username, return all photos

  http://www.flickr.com/photos/searchtags/123,456
  We return the photos of a search on the comma separated list of tags

  http://www.flickr.com/photos/rbpdesigner/searchtags/123,456
  We return the photos of a search on the comma separated list of tags; for that specific user

IPhoto.description metadata is not supported

facebook_
~~~~~~~~~

In Plone as with other link you just have to paste the link inside a Link content
type.

The album must be public. Links supported are:

* http://www.facebook.com/album.php?aid=ALBUMID&id=OTHERID
* http://www.facebook.com/media/set/?set=a.ALBUMID.OTHERID.STHELSE (the url must contains 5 dots)

IPhoto.description metadata is not supported

Integrators
===========

You have some examples of addons based on this one:

* collective.galleria
* collective.galleriffic
* collective.fancyboxgallery
* collective.highslide
* collective.portlet.fancyboxgallery

Extra addons to use with collective.gallery:

* collective.quickupload
* Products.ImageEditor

You want more ?
===============

The picasaweb and flickr services let you embed a flash slideshow to display your photos.
Views are already available to use those services:

* @@gallery-picasaweb-slideshow
* @@gallery-flickr-slideshow

But they are not integrated in the Plone UI.

Credits
=======

Companies
---------

|makinacom|_

* `Planet Makina Corpus <http://www.makina-corpus.org>`_
* `Contact Makina Corpus <mailto:python@makina-corpus.org>`_


People
------

- JeanMichel FRANCOIS aka toutpt <toutpt@gmail.com>
- Mathieu Le Marec - Pasquet <kiorky@cryptelium.net> 
- Jean-Philippe Camguilhem <jp.camguilhem@gmail.com>
- Johannes Raggam <raggam-nl@adm.at>
- Giacomo Spettoli

.. |makinacom| image:: http://depot.makina-corpus.org/public/logo.gif
.. _makinacom:  http://www.makina-corpus.com
.. _flickr: http://www.flickr.com
.. _picasaweb: http://picasaweb.google.com
.. _jcarousel: http://sorgalla.com/jcarousel
.. _facebook: http://www.facebook.com
