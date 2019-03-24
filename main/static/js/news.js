function get_news() {
    var data = $.ajax({
        type: 'GET',
        url: '/get_news_post',
        data: {},
        success: function (data) {
            console.log(data);
        }
    });
}

get_news();
