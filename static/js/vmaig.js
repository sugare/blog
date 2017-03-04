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

$(function () {
    $('#loadmore').bind('click', function () {
        var page = parseInt($('#page').val());
        $(this).html('加载中...');
        status = $(this).attr("data-status");
        if (status == 1) {
            status = $(this).attr("data-status", "0");
            $.ajax({
                type : "POST",
                url : "/",
                data : "page=" + page,
                success : function (data) {
                    if (data == "1") {
                        $('#loadmore').hide()
                    } else {
                        $('#page').val(page + 1);
                        $('#all-post-list').append(data);
                        console.log(page);
                        $("#loadmore").html('加载更多... <span class="glyphicon glyphicon-arrow-down"></span>');
                        $("#loadmore").attr("data-status", "1");
                    }



                }

            });
        }
    });
});

$(function () {
    $('[name="category"]').bind('click', function () {
        var category = $(this).val();

        $('#all-post-list').html('<div class="progress progress-striped active"><div class="progress-bar progress-bar-success" role="progressbar" aria-valuenow="60" aria-valuemin="0" aria-valuemax="100" style="width: 100%;"><span class="sr-only"></span></div></div>');
        var parent = $(this).parent();
        parent.addClass('active').siblings().removeClass('active');
        // $(this).parent().addClass('active');
        setTimeout(function () {
            $.ajax({
            type : "POST",
            url : "/api",
            data : "category=" + category,
            success : function (data) {
                $('#all-post-list').html(data);
                }
            });
        }, 300);

    })
});
