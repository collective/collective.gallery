// We only want these styles applied when javascript is enabled
$(document).ready(function(){
    $('div.navigation').css({
        'width': '300px',
        'float': 'left'
    });
    $('div.gallerycontent').css('display', 'block');
    // Initialize Minimal Galleriffic Gallery
    $('#thumbs').galleriffic({
        imageContainerSel: '#slideshow',
        controlsContainerSel: '#controls'
    });
});
