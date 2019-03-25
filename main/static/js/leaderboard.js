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

            for (var i = 0; i < list_rank.length; i++) {
                document.getElementsByClassName("change2")[0].innerHTML += '<div class="col s4 center-align">' + list_rank[i].toString() + '</div> <div class="col s4 center-align">' + list_user_name[i] + '</div> <div class="col s4 center-align">' + list_net_worth[i].toString() + '</div>';
            }

            var userBalance = document.getElementById("balance");
            userBalance.innerHTML = `Balance: ${balance}`;
        }
    });
}

get_leaderboard();

function getBalance() {
    var data = $.ajax({
        type: 'GET',
        url: `/get_balance`,
        data: {},
        success: function (data) {
            balance = data.balance;
            document.getElementById("balance").innerHTML = "Balance: " + balance.toString();
        }
    });
}

getBalance();

function addTabs() {
    if (window.innerWidth > 500) {
        document.getElementById("heading").innerHTML = "&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;LEADERBOARD";
    }
}

addTabs();