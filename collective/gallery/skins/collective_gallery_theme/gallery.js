// We only want these styles applied when javascript is enabled
jQuery(document).ready(function($){
    $('div#gallerythumbs').css({'display': 'block'});
    $('a.thumb').css({
        'float': 'left',
        'margin-right':'5px',
        'height':'80px', //use ul.thumbs heigth from css
        'border-bottom':'none'
    });

    var onMouseOutOpacity = 0.67;
    $('.thumbs li').opacityrollover({
     mouseOutOpacity: onMouseOutOpacity,
     mouseOverOpacity: 1.0,
     fadeSpeed: 'fast',
     exemptionSelector: '.selected'
     }); 

    var gallery = $('#gallerythumbs').galleriffic({

        //delay:                     3000, // in milliseconds
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
        syncTransitions:           false, // Specifies whether the out and in transitions occur simultaneously or distinctly
        defaultTransitionDuration: 1000, // If using the default transitions, specifies the duration of the transitions
        onSlideChange:             undefined, // accepts a delegate like such: function(prevIndex, nextIndex) { ... }
        onTransitionOut:           undefined, // accepts a delegate like such: function(slide, caption, isSync, callback) { ... }
        onTransitionIn:            undefined, // accepts a delegate like such: function(slide, caption, isSync) { ... }
        onPageTransitionOut:       undefined,
        onPageTransitionIn:        undefined,
        onImageAdded:              undefined, // accepts a delegate like such: function(imageData, $li) { ... }
        onImageRemoved:            undefined  // accepts a delegate like such: function(imageData, $li) { ... }
    });
    $('#gallerypageprev').click(function(e) {
        $('#gallerypause').hide();
        $('#galleryplay').show();
       gallery.previousPage();
       e.preventDefault();
     });
    
    $('#gallerypagenext').click(function(e) {
        $('#gallerypause').hide();
        $('#galleryplay').show();
       gallery.nextPage();
       e.preventDefault();
     }); 
    $('#galleryprev').click(function(e) {
        $('#gallerypause').hide();
        $('#galleryplay').show();
       gallery.previous();
       e.preventDefault();
     });
    $('#gallerynext').click(function(e) {
        $('#gallerypause').hide();
        $('#galleryplay').show();
       gallery.next();
       e.preventDefault();
     });
    if (gallery.autoStart)
        $('#galleryplay').hide();
    else 
        $('#gallerypause').hide();
    $('#galleryplay').click(function(e) {
       gallery.play();
       e.preventDefault();
       $('#galleryplay').hide();
       $('#gallerypause').show();
     });
    $('#gallerypause').click(function(e) {
       gallery.pause();
       e.preventDefault();
       $('#gallerypause').hide();
       $('#galleryplay').show();
     });
     $('#galleryphoto').tooltip({position:'center right', effect:'fade',relative:true});

});
