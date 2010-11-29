// We only want these styles applied when javascript is enabled
jQuery(document).ready(function($){
    jq('div.navigation').css({
        'width': '550px',
        'float': 'left'
    });
    jq('div.gallerycontent').css('display', 'block');
    jq('a.thumb').css({
        'float': 'left',
        'margin-right':'5px',
        'height':'60px',
        'border-bottom':'none'
    });
    // Initialize Minimal Galleriffic Gallery
    jq('#thumbs').galleriffic({
        imageContainerSel: '#slideshow',
        controlsContainerSel: '#controls',
        captionContainerSel: '#caption'
    });
});
