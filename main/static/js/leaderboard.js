function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
}

function closeNav() {
    document.getElementById("mySidenav").style.width = 0;
}


function get_leaderboard() {
    var data = $.ajax({
        type: 'GET',
        url: `/leaderboard`,
        data: {},
        success: function (data) {
            console.log(data);
            var list_rank = data.list_rank;
            var list_net_worth = data.list_net_worth;
            var list_user_name = data.list_user_name;
            
            for(var i =0; i < list_rank.length; i++){
            document.getElementsByClassName("container")[0].innerHTML += '<div class="row #ffffff white change2"> <div class="col s4 center-align">' + list_rank[i].toString() + '</div> <div class="col s4 center-align">' + list_user_name[i] + '</div> <div class="col s4 center-align">' + list_net_worth[i].toString() + '</div> </div>';
        	}
        }
    });
}

get_leaderboard();
