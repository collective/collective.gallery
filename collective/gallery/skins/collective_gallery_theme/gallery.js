jq(document).ready(function(){
    jq("#pikame").PikaChoose({text: { play: "", stop: "", previous: "", next: "" }});
    jq("#pikame").jcarousel({
        scroll: 4,
        initCallback: function(carousel){
            jq(carousel.list).find('img').click(function(){
                //console.log($(this).parents('.jcarousel-item').attr('jcarouselindex'));
                carousel.scroll(parseInt($(this).parents('.jcarousel-item').attr('jcarouselindex')));
            });
        }
    });
    
});
