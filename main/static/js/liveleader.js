function get_leaderboard() {
    var data = $.ajax({
        type: 'GET',
        url: `/final_leaderboard_data`,
        data: {},
        success: function (data) {
            var list_rank = data.list_rank;
            var list_net_worth = data.list_net_worth;
            var list_user_name = data.list_user_name;
            // let user = data.current_username;
            let i;
            for (i = 0; i < list_rank.length; i++) {
                document.getElementsByClassName("change2")[0].innerHTML += '<div><div class="col l2 s4 center-align">' + list_rank[i].toString() + '</div> <div class="col l6 s4 center-align">' + list_user_name[i] + '</div> <div class="col l4 s4 center-align">' + parseFloat(list_net_worth[i]).toFixed(2) + '</div></div>';
            }
            // var userBalance = document.getElementById("balance");
            // userBalance.innerHTML = `Balance: ${balance}`;
        }
    });
}

get_leaderboard();

// function getBalance() {
//     var data = $.ajax({
//         type: 'GET',
//         url: `/get_balance`,
//         data: {},
//         success: function (data) {
//             balance = data.balance;
//             networth = data.net_worth;
//             document.getElementById("balance").innerHTML = "Bal: " + parseFloat(balance).toFixed(2) + " &s | &nbsp; Net: " + parseFloat(networth).toFixed(2);
//         }
//     });
// }

// getBalance();
