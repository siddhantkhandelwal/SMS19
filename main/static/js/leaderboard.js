function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
}

function closeNav() {
    document.getElementById("mySidenav").style.width = 0;
}


function get_leaderboard() {
    var data = $.ajax({
        type: 'GET',
        url: '/leaderboard/',
        data: {},
        success: function (data) {
            console.log(data);
            list_ranks = data.list_ranks;
            list_net_worth = data.list_net_worth;
            list_name = data.list_name;
            for(var i =0; i <list_ranks.length; i++){
            document.getElementsByClassName("container")[0].innerHTML = '<div class="row #ffffff white change2"> <div class="col s4 center-align">' + list_ranks[i] + '</div> <div class="col s4 center-align">' + list_name[i] + '</div> <div class="col s4 center-align">' + list_net_worth[i] + '</div> </div>';
        	}
        }
    });
}

get_leaderboard();
