function get_news() {
    var data = $.ajax({
        type: 'GET',
        url: '/get_news_post',
        data: {},
        success: function (data) {
            console.log(data);
            console.log(document.getElementById("card_holder"));
            console.log(data.news_list);
            console.log(data.news_list[0][0]);
            for (let i = 0 ; i < data.news_list.length ; i++) {
                document.getElementById("card_holder").innerHTML +=
                "<div class='card'>" + 
                "<div class='card-action purple darken-1 white-text'><h5>" + data.news_list[i][0] + 
                "</h5></div>" +
                "<div class='card-content'>" +
                    "<p>" + data.news_list[i][1] + "</p>" +
                "</div>" +
                "<div class='card-action'>" + data.news_list[i][2] + 
                "</div> " +
            "</div>"

            }
        }
    });
}

get_news();

function openNav() {
    document.getElementById("mySidenav").style.width = 250 + 'px';
}

function closeNav() {
    document.getElementById("mySidenav").style.width = 0 + 'px';
}