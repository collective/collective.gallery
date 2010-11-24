// We only want these styles applied when javascript is enabled
jq(document).ready(function(){
    jq('div.navigation').css({
        'width': '300px',
        'float': 'left'
    });
    jq('div.gallerycontent').css('display', 'block');
    // Initialize Minimal Galleriffic Gallery
    jq('#thumbs').galleriffic({
        imageContainerSel: '#slideshow',
        controlsContainerSel: '#controls'
    });
});
