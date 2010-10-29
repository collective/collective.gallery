Notes: gdata 2.0.10 doesn't work properly: http://code.google.com/p/gdata-python-client/issues/detail?id=367#c1
please pin the version to 2.0.9

Introduction
============

Gallery is an add-on full of features with a design that make it easy to customize.

It is tested with: Plone 3.3.X and Plone 4

It use Pikachoose_ plugin with jcarousel_ packaged in collective.js.pikachoose

It support Galleriffic_ plugin with jquery.history embed in the package.

Plone integration of galleriffic use example1_. An other example can be find
on http://goo.gl/yqNi

Goals
=====

* Have a simple to customize gallery product for plone.
* Use very ligth weight resources
* Don't embed display configuration inside data

Features
========

* No custom content type, only views
* Works with lots of photos (is developed to work with +300 photos)
* Ramcache setup with a default key to one hours + modification date
* Works with Folder, Topic and Link content types
* picasaweb_ and flickr_ support.
* I18N: english and french are available
* tested

picasaweb_
----------

* It's free to use
* Web albums, synchronised with picasa software
* Share your albums
* Add geo-tags to your photos
* Automatically organize your photos based on the people in them
* Display in a slideshow (flash)

In Plone, just paste the share link provided by picasaweb inside a Link content type
and display your link content with the view gallery available in the drop down display menu.

flickr_
-------

* It's free to use
* Share your photos
* Upload and organize
* Add geo-tags to your photos
* Display in a slideshow (flash)

In Plone, just paste the share link provided by flickr inside a Link content type
and display your link content with the view gallery available in the drop down display menu.

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

Pickachoose_
============

* easy to setup
* jCarousel integrates smoothly with PikaChoose to give your gallery simple and effective carousel.

Components
==========

collective.gallery use zope.components to provide as much reusable as possible components.

First we have photo resources. Plone already manage this for you:

* Folder and Large Plone Folder can contains Image
* Topic can be criterized to list only Image
* Link can be sources of photos throw picasaweb.google.com and flickr.com services.

Next you have the business component: IGallery. This interface is implemented at two levels:

* As named adapter over IATLink to get photos from picasaweb or flickr.
* As browserview to control the resource (@@gallery)

The picasaweb and flickr services let you embed a flash slideshow to display your photos.
Views are already available to use those services:

* @@gallery-picasaweb-slideshow
* @@gallery-flickr-slideshow

But they are not integrated in the Plone UI.

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

.. |makinacom| image:: http://depot.makina-corpus.org/public/logo.gif
.. _makinacom:  http://www.makina-corpus.com
.. _Galleriffic: http://www.twospy.com/galleriffic/
.. _flickr: http://www.flickr.com
.. _picasaweb: http://picasaweb.google.com
.. _jcarousel: http://sorgalla.com/jcarousel
.. _Pikachoose: http://pikachoose.com
