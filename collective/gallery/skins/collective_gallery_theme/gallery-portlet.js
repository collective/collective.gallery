// We only want these styles applied when javascript is enabled

var init_galleryportlet = function(id, container){
    var gallery = $(id).galleriffic({

        delay:                     3000, // in milliseconds
        //numThumbs:                 5, // The number of thumbnails to show page
        //preloadAhead:              40, // Set to -1 to preload all images
        enableTopPager:            false,
        enableBottomPager:         false,
        //maxPagesToShow:            7,  // The maximum number of pages to display in either the top or bottom pager
        imageContainerSel:         '#slideshow', // The CSS selector for the element within which the main slideshow image should be rendered
        //controlsContainerSel:      '', // The CSS selector for the element within which the slideshow controls should be rendered
        //captionContainerSel:       '#gallerycaption', // The CSS selector for the element within which the captions should be rendered
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
    });

};
