$(function(){
/*widgest 中卷起的js*/
    $('.panel-close').click(function(){
        $(this).parent().parent().parent().hide(300);
    });

    $('.collapse').on('hide.bs.collapse',function(){
        $(this).prev().find(".panel-collapse").removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down');
    });

    $('.collapse').on('show.bs.collapse',function(){
        $(this).prev().find(".panel-collapse").removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up');
    });


});

/*提示的js*/
$(function () { $("[data-toggle='tooltip']").tooltip(); });
$('#nav-login').tooltip('hide');


$(function() {
    if( ! $('#myCanvas').tagcanvas({
        textColour : '#222;',
        outlineThickness : 1,
        maxSpeed : 0.03,
        depth : 0.5,
        textHeight:18,

    })) {
    // TagCanvas failed to load
    $('#myCanvasContainer').hide();
    }
    // your other jQuery stuff here...
});