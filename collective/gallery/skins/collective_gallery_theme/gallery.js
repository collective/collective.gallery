// We only want these styles applied when javascript is enabled

jQuery(document).ready(function($){
  var galleryMaxsize = 400;
  var galleryMouseOpacity = 0.67;
  var galleryPhoto = $('#galleryphoto');
  var galleryPhotoPosition = galleryPhoto.position();
  var galleryPhotoWidth = galleryPhoto.width();
  var galleryPhotoHeight = galleryPhoto.height();
  
  function galleryResizePhoto(photo) {
      // resize the photo if the scale is greater than our maxsize
      if (!photo)return;
      var dw = photo.width() - galleryMaxsize;
      var dh = photo.height() - galleryMaxsize;
      if (dw > 0 || dh > 0) {
          if (dw > dh){
              photo.width(galleryMaxsize);
          }else{photo.height(galleryMaxsize);}
      }
  }
  function galleryCenterPhoto(photo) {
      // display the photo in the good absolute position
      // fix fast navigation bug (where imgs where added one upon the other)
      if (!photo)return;
      var photoWidth = photo.width();
      var photoHeight = photo.height();
      var photoTop = parseInt(galleryPhotoPosition.top + (galleryPhotoHeight - photoHeight) / 2);
      var photoLeft = parseInt(galleryPhotoPosition.left + (galleryPhotoWidth - photoWidth) / 2);
      photo.parent().parent().css({'position': 'absolute', 'top': photoTop + 'px', 'left': photoLeft + 'px'});
  }

    if ($('div#gallerythumbs').length == 0){return;}
    if ($('ul.thumbs li').length == 0){return;}
    $('div#gallerythumbs').css({'display': 'block'});
    $('a.thumb').css({
        'float': 'left',
        'margin-right':'5px',
        'height':'80px', //use ul.thumbs heigth from css
        'border-bottom':'none'
    });

    $('.thumbs li, #gallerypageprev, #gallerypagenext').opacityrollover({
     mouseOutOpacity: galleryMouseOpacity,
     mouseOverOpacity: 1.0,
     fadeSpeed: 'fast',
     exemptionSelector: '.selected'
     }); 

    var gallery = $('#gallerythumbs').galleriffic({

        delay:                     3000, // in milliseconds
        numThumbs:                 5, // The number of thumbnails to show page
        //preloadAhead:              40, // Set to -1 to preload all images
        enableTopPager:            false,
        enableBottomPager:         false,
        //maxPagesToShow:            7,  // The maximum number of pages to display in either the top or bottom pager
        imageContainerSel:         '#galleryphoto', // The CSS selector for the element within which the main slideshow image should be rendered
        //controlsContainerSel:      '', // The CSS selector for the element within which the slideshow controls should be rendered
        captionContainerSel:       '#gallerycaption', // The CSS selector for the element within which the captions should be rendered
        //loadingContainerSel:       '#galleryloading', // The CSS selector for the element within which should be shown when an image is loading
        renderSSControls:          false, // Specifies whether the slideshow's Play and Pause links should be rendered
        renderNavControls:         false, // Specifies whether the slideshow's Next and Previous links should be rendered
        //playLinkText:              'Play',
        //pauseLinkText:             'Pause',
        //prevLinkText:              'Previous',
        //nextLinkText:              'Next',
        //nextPageLinkText:          'Next &rsaquo;',
        //prevPageLinkText:          '&lsaquo; Prev',
        enableHistory:             false, // Specifies whether the url's hash and the browser's history cache should update when the current slideshow image changes
        enableKeyboardNavigation:  false, // Specifies whether keyboard navigation is enabled
        autoStart:                 true, // Specifies whether the slideshow should be playing or paused when the page first loads
        syncTransitions:           true, // Specifies whether the out and in transitions occur simultaneously or distinctly
        defaultTransitionDuration: 500, // If using the default transitions, specifies the duration of the transitions
        onSlideChange: function(prevIndex, nextIndex) {
           if (this.isSlideshowRunning) {
              $('#galleryplay').hide();
              $('#gallerypause').show();
           } else {
              $('#gallerypause').hide();
              $('#galleryplay').show();
           }
        },
        onTransitionOut:           undefined, // accepts a delegate like such: function(slide, caption, isSync, callback) { ... }
        onTransitionIn:            function(newSlide, newCaption, isSync){
            //code kept from galleriffic
            $('.image-caption').hide();
            newSlide.fadeTo(this.getDefaultTransitionDuration(isSync), 1.0);
            if (newCaption)
                newCaption.fadeTo(this.getDefaultTransitionDuration(isSync), 1.0);
            galleryResizePhoto(newSlide.find('img'));
            galleryCenterPhoto(newSlide.find('img'));

        }, // accepts a delegate like such: function(slide, caption, isSync) { ... }
        onPageTransitionOut:       undefined, // accepts a delegate like such: function(slide, caption, isSync, callback) { ... }
        onPageTransitionIn:        undefined, // accepts a delegate like such: function(slide, caption, isSync) { ... }
        onImageAdded:              undefined, // accepts a delegate like such: function(imageData, $li) { ... }
        onImageRemoved:            undefined  // accepts a delegate like such: function(imageData, $li) { ... }
    });
    if (gallery.autoStart){
        $('#galleryplay').hide();
        $('#gallerypause').show();
    } else {
        $('#gallerypause').hide();
        $('#galleryplay').show();
    }
    $('#gallerypageprev').click(function(e) {
       gallery.previousPage();
       e.preventDefault();
     });
    
    $('#gallerypagenext').click(function(e) {
       gallery.nextPage();
       e.preventDefault();
     }); 
    $('#galleryprev').click(function(e) {
       gallery.previous();
       e.preventDefault();
     });
    $('#gallerynext').click(function(e) {
       gallery.next();
       e.preventDefault();
     });

    $('#galleryplay').click(function(e) {
       $('#galleryplay').hide();
       gallery.play();
       e.preventDefault();
       $('#gallerypause').show();
     });
    $('#gallerypause').click(function(e) {
       $('#gallerypause').hide();
       gallery.pause();
       e.preventDefault();
       $('#galleryplay').show();
     });
     $('#galleryphoto').tooltip({position:'center right', effect:'fade',relative:true});

});
