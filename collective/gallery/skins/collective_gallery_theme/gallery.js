$(document).ready(function(){
    $("#pikame").PikaChoose({text: { play: "", stop: "", previous: "", next: "" }});
    $("#pikame").jcarousel({
        scroll: 4,
        initCallback: function(carousel){
            $(carousel.list).find('img').click(function(){
                //console.log($(this).parents('.jcarousel-item').attr('jcarouselindex'));
                carousel.scroll(parseInt($(this).parents('.jcarousel-item').attr('jcarouselindex')));
            });
        }
    });
    
});
