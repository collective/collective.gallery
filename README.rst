Notes: gdata 2.0.10 doesn't work properly: http://code.google.com/p/gdata-python-client/issues/detail?id=367#c1
please pin the version to 2.0.9

Introduction
============

This add-on is gallery add-on for Plone.

It is tested with Plone 4 but it is also used with Plone 3.

This add-on is split in two parts: the UI and components

The goals are:

* Have a simple to customize gallery add-on for plone (non intrusive).
* Use very ligth weight resources
* Don't embed display configuration inside data

User Interface
==============

The user interface has been designed to be easy to customize. Files are located
in the skin directory (easy to customize):

* gallery.html.pt: Zope Page Template to render the html code
* gallery.css: pure css design to display 400*400 photos
* gallery.html.pt.metadata: to set the title of the page in display drop down menu
* gallery.js: the javascript integration of galleriffic_.
* gallery_tooltip.png: the tooltip used to display the title/description of the photo

The user interface has many feature:

* resize photo if too big by setting the width or height
* paginate thumbs for navigation (5 by default)
* opacity on mouse rollover thumbs
* play / pause (autostart by default)
* display more than 300 photos without any performance issue
* display title and description throw a smart jquerytool tooltip

There are also two portets, which can be used:

* "Show Galleries" portlet to display random photos from random galleries.
* An itemview portlet to display specific photos.


Components (Backend)
====================

Summary:

* No custom content type, only views
* Works with lots of photos (is developed to work with +300 photos)
* Ramcache setup with a default key to one hours + modification date
* Works with Folder, Topic and Link content types
* picasaweb_ and flickr_ support.
* facebook support.
* I18N: english, french and german are available

collective.gallery use zope.components to provide as much reusable as possible
components.

First we have photo resources. Plone already manage this for you:

* Folder and Large Plone Folder can contains Image
* Topic can be criterized to list only Image
* Link can be sources of photos throw picasaweb.google.com and flickr.com services.

Next you have the business component: IGallery. This interface is implemented
at two levels:

* As named adapter over IATLink to get photos from picasaweb or flickr.
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

flickr_
~~~~~~~

In Plone, just paste the share link provided by flickr inside a Link content
type and display your link content with the view gallery available in the drop down display menu.

Flickr service is not album centric but photo centric. Supported case:

  http://www.flickr.com/photos/autowitch/sets/107460
  It is an album, no problem

  http://www.flickr.com/photos/rbpdesigner
  We have the username, return all photos

IPhoto.description metadata is not supported

facebook_
~~~~~~~~~

In Plone as with other link you just have to paste the link inside a Link content
type.

The album must be public.

IPhoto.description metadata is not supported

Galleriffic_
============

* Smart image preloading after the page is loaded
* Thumbnail navigation (with pagination)
* jQuery.history plugin integration to support bookmark-friendly URLs per-image
* Slideshow (with optional auto-updating url bookmarks)
* Keyboard navigation
* Events that allow for adding your own custom transition effects
* API for controlling the gallery with custom controls
* Support for image captions
* Flexible configuration
* Graceful degradation when javascript is not available
* Support for multiple galleries per page

Integrators
===========

Because it is easy to customize, lets write some lines about how to fit gallery
to your needs.

Some advices:

be fixed width. Photo are fixed, you want your gallery to be nice, lets fixed its width.

You can configure in properties the max photo size you want but backends may not support
this settings.

Most of galleries do not contains every photos in the same size or in the same proportions.
Take care of this when you are customizing javascript and css.

All controllers can be placed where ever you want because they are accessed by #id

Gallery is not configurable because it needs to generate javascript and css.
It would make the add-on too much complex to customize. If you want configuration take
a look at plonetruegallery_

To register the "Show Galleries" portlet, you can add the following xml snippet
to your portlets.xml Generic Setup file:::

    <assignment
      name="gallery-portlet"
      category="context"
      key="/"
      manager="plone.rightcolumn"
      type="collective.gallery.show_galleries"
      visible="True">
      <property name="search_portal">True</property>
      <property name="num_pictures">1</property>
      <property name="image_size">mini</property>
   </assignment>


You want more ?
===============

The picasaweb and flickr services let you embed a flash slideshow to display your photos.
Views are already available to use those services:

* @@gallery-picasaweb-slideshow
* @@gallery-flickr-slideshow

But they are not integrated in the Plone UI.

References
==========

This add-on is use in production here and there:

* http://www.nantes-developpement.com/search?portal_type=Diaporama
* http://www.recuperateurdepluie.fr/photos-aqualogic

Roadmap
=======

* [1.0] finish the css
* [1.1] exif integration
* [2.0] add photos
* [2.0] search photos
* [2.0] collective.harlequin as an extra dependency

Credits
=======

Companies
---------

|makinacom|_

  * `Planet Makina Corpus <http://www.makina-corpus.org>`_
  * `Contact us <mailto:python@makina-corpus.org>`_


Authors

  - JeanMichel FRANCOIS aka toutpt <toutpt@gmail.com>

Contributors

  - Johannes Raggam <raggam-nl@adm.at>

.. |makinacom| image:: http://depot.makina-corpus.org/public/logo.gif
.. _makinacom:  http://www.makina-corpus.com
.. _Galleriffic: http://www.twospy.com/galleriffic/
.. _flickr: http://www.flickr.com
.. _picasaweb: http://picasaweb.google.com
.. _jcarousel: http://sorgalla.com/jcarousel
.. _Pikachoose: http://pikachoose.com
.. _facebook: http://www.facebook.com
.. _plonetruegallery: http://plone.org/products/plone-true-gallery
