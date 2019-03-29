function closeBuyDiv() {
    document.getElementById("buyDiv").style.display = "none";
}

function openSellDiv() {
    document.getElementById("sellDiv").style.display = "block";
}

function closeSellDiv() {
    document.getElementById("sellDiv").style.display = "none";
}

function get_stock_list(code) {
    var data = $.ajax({
        type: 'GET',
        url: `/get_stock_purchased/${code}`, //Do not edit these special commas. Everything will go to shit.
        data: {},
        beforeSend: function () {
            $('.loader').show();
        },
        complete: function () {
            $('.loader').hide();
        },
        success: function (data) {

            let marketStatus = data.marketStatus;

            // if( !data.marketStatus) {
            //     alert('This market has been temporarily closed by EFA');
            //     return;<p><h5>Event is not live yet. Register after 21:00 IST (Read BST)</h5></p>
            // }
            let s_list; // stores info of stock
            stock_list = data.stocks_purchased;
            if (stock_list.length == 0) {
                $(".stock_list")[0].innerHTML = "<div class='row'><div class='col s12 black white-text center-align flow-text' style='font-family: 'Ubuntu', sans-serif;'>" +
                    "No stocks owned for the current market.</div></div>"
                getBalance();
            }

            else {
                getBalance();
                document.getElementsByClassName("stock_list")[0].innerHTML = "";
                for (var i = 0; i < stock_list.length; i++) {
                    s_list = stock_list[i];
                    var accordion = document.createElement("div");
                    accordion.setAttribute("class", "accordion row");
                    accordion.setAttribute("data-pk", s_list[0]);

                    var innerDiv = document.createElement("div");
                    innerDiv.setAttribute("class", "col s4 center-align ");

                    var span = document.createElement("span");
                    span.setAttribute("class", "valign nameOfStock");
                    span.innerHTML = s_list[1];

                    var price = document.createElement("div");
                    price.setAttribute("class", "col s4 center-align ");
                    price.innerHTML = s_list[2] + " ";

                    var trendSpanUp = document.createElement("span");
                    trendSpanUp.setAttribute("class", "valign");
                    trendSpanUp.innerHTML = "<i class='fa fa-angle-up' style='color: green;'></i>";

                    var trendSpanDown = document.createElement("span");
                    trendSpanDown.setAttribute("class", "valign");
                    trendSpanDown.innerHTML = "<i class='fa fa-angle-down' style='color: red;'></i>";

                    var units = document.createElement("div");
                    units.setAttribute("class", "col s4 center-align ");

                    var span2 = document.createElement("span");
                    span2.setAttribute("class", "valign");
                    span2.innerHTML = s_list[3];

                    var panel = document.createElement("div");
                    panel.setAttribute("class", "panel row #e1bee7 purple lighten-4");
                    panel.style.transition = "height 0.1s linear";

                    var buyButton = document.createElement("button");
                    buyButton.setAttribute("id", "buy-btn" + i.toString());
                    buyButton.setAttribute("data-pk", s_list[0]);
                    buyButton.setAttribute("class", "buy col s2 offset-s3");
                    buyButton.innerHTML = "BUY";
                    buyButton.style.padding = "5px";

                    var sellButton = document.createElement("button");
                    sellButton.setAttribute("id", "sell-btn" + i.toString());
                    sellButton.setAttribute("class", "sell col s2 offset-s2");
                    sellButton.setAttribute("data-pk", s_list[0]);
                    sellButton.innerHTML = "SELL";
                    sellButton.style.padding = "5px";
                    // buyButton.style.display = "none";
                    // buyButton.innerHTML = s_list;

                    var userBalance = document.getElementById("balance");
                    userBalance.innerHTML = `Balance: ${balance}`;
                    panel.appendChild(buyButton);
                    innerDiv.appendChild(span);
                    accordion.appendChild(innerDiv);

                    //Fifth element of StockTrend required here. Demo functioning with number of stocks purchased.
                    if (s_list[4] > 0) {
                        price.appendChild(trendSpanUp);
                    }
                    else {
                        price.appendChild(trendSpanDown);
                    }

                    accordion.appendChild(price);
                    accordion.appendChild(units);
                    units.appendChild(span2);
                    panel.appendChild(buyButton); panel.appendChild(sellButton);
                    document.getElementsByClassName("stock_list")[0].appendChild(accordion.cloneNode(true));
                    document.getElementsByClassName("stock_list")[0].appendChild(panel);
                }
            }
            var acc = document.getElementsByClassName("accordion");
            var i = 0;

            while (i < acc.length) {
                acc[i].addEventListener("click", function () {
                    this.classList.toggle("active");
                    var panel = this.nextElementSibling;
                    // console.log('s_list');
                    panel.style.maxHeight = panel.scrollHeight + "px";
                    let stockStatus = s_list[5];
                    // console.log(stockStatus);
                    // console.log(s_list);
                    if( !marketStatus) {
                        alert('Market has been closed by EFA.');
                        return;
                    }
                    if( !stockStatus) {
                        alert('This stock has been closed by EFA.');
                        return;
                    }
                    if (panel.style.height) {
                        panel.style.height = null;
                    } else {
                        panel.style.height = "50px";
                    }
                });
                i++;
            }

            var buy = document.getElementsByClassName("buy");
            var sell = document.getElementsByClassName("sell");
            var j = 0;
            var x = 0;

            var alpha; //pk for buy
            //pk for cell  ---- I don't know why I'm using different variables for buy and sell.

            //FOR BUY BUTTONS
            while (j < buy.length) {
                buy[j].addEventListener("click", function (e) {
                    document.getElementById("blur").style.display = "block";
                    alpha = this.getAttribute("data-pk");
                    document.getElementById("buyDiv").style.display = "block";
                    let i;
                    for( i=0; i<stock_list.length; i++) {
                        if( stock_list[i][0] == alpha)
                            break;
                    }
                    document.getElementById("buyInfo").innerHTML = "Stock: " + stock_list[i][1] + ", Price:     " + stock_list[i][2];
                });
                j++;
            }
            //FOR SELL BUTTONS
            while (x < sell.length) {
                sell[x].addEventListener("click", function (e) {
                    document.getElementById("blur").style.display = "block";
                    alpha = this.getAttribute("data-pk");
                    document.getElementById("sellDiv").style.display = "block";
                    let btnId = e.target.id.toString();
                    btnId = btnId.substring(btnId.length - 1);
                    document.getElementById("sellInfo").innerHTML = "Stock: " + stock_list[btnId][1] + ", Price:     " + stock_list[btnId][2];
                });
                x++;
            }

            //FOR SUBMITTING SELL REQUEST
            $("#submit_sell").off();
            $("#submit_sell").on("click", function () {
                var inputNumber = document.getElementById("number1").value;
                sellStock(parseInt(alpha), parseFloat(inputNumber), code);
                getBalance();
                hideSellDiv();
            });

            //FOR SUBMITTING BUY REQUEST
            $("#submit_buy").off();
            $("#submit_buy").on("click", function () {
                var inputNumber = document.getElementById("number").value;
                buyStock(parseInt(alpha), parseFloat(inputNumber), code);
                getBalance();
                hideBuyDiv();
            });
        }
    });
}

get_stock_list("BSE");
document.getElementById("indian1").addEventListener("click", function () { 
    get_stock_list("BSE");
    document.getElementById("conversion").innerHTML = "1 &#8377; = 1 &#8377;";
});
document.getElementById("international1").addEventListener("click", function () {
    get_stock_list("NYM");
    document.getElementById("conversion").innerHTML = "69.16 &#8377; = 1 &#36;";
});
document.getElementById("international2").addEventListener("click", function () {
    get_stock_list("JPN");
    document.getElementById("conversion").innerHTML = "0.63 &#8377; = 1 &#165;";
});

function buyStock(pk, units, code) {

    if (units < 0 || ((units - Math.floor(units)) != 0) || units > 10000) {
        alert('Enter valid value');
        return;
    }

    var data = $.ajax({
        type: 'POST',
        url: `/buy_stock/${pk}/`,
        data: {
            "units": units
        },
        success: function (data) {
            document.getElementById("popup").style.display = "block";
            document.getElementById("popup").innerHTML = data.message;
            setTimeout(function () {
                document.getElementById("popup").style.display = "none";
            }, 5000);
            getBalance();
            get_stock_list(code);
            document.getElementById("number").value = "";
            $('.closeBuyDiv').trigger('click');
        }
    });
}

function sellStock(pk, units, code) {

    if (units < 0 || ((units - Math.floor(units)) != 0) || units > 10000) {
        alert('Enter valid value');
        return;
    }

    var data = $.ajax({
        type: 'POST',
        url: `/sell_stock/${pk}/`,
        data: {
            "units": units
        },
        success: function (data) {
            document.getElementById("popup").style.display = "block";
            document.getElementById("popup").innerHTML = data.message;
            setTimeout(function () {
                document.getElementById("popup").style.display = "none";
            }, 5000);
            getBalance();
            get_stock_list(code);
            document.getElementById("number1").value = "";
            $('.closeSellDiv').trigger('click');
        }
    });
}

function getBalance() {
    var data = $.ajax({
        type: 'GET',
        url: `/get_balance`,
        data: {},
        success: function (data) {
            balance = data.balance;
            networth = data.net_worth;
            document.getElementById("balance").innerHTML = "Bal: " + parseFloat(balance).toFixed(2) + "&nbsp; | &nbsp;Net: " + parseFloat(networth).toFixed(2);
        }
    });
}

getBalance();
function hideBuyDiv() {
    document.getElementById("buyDiv").style.display = "none";

}

function hideSellDiv() {
    document.getElementById("sellDiv").style.display = "none";

}

function hideBlurDiv() {
    document.getElementById("blur").style.display = "none";
}

var btnContainer = document.getElementById("myDiv");

var btns = btnContainer.getElementsByClassName("butn");

for (var i = 0; i < btns.length; i++) {
    btns[i].addEventListener("click", function () {
        var current = document.getElementsByClassName("activeLink");
        current[0].className = current[0].className.replace(" activeLink", "");
        this.className += " activeLink";
    });
}
   // buyButton.addEventListener('click', function() {
                //     document.getElementById("buyDiv").style.display = "block";
                //     document.getElementById("submit_buy").setAttribute("data-button-type", s_list[0]);
                //     var submit = document.getElementById("submit_buy");
                //     submit.addEventListener('click', function() {
                //         var x = document.getElementById("number").value;
                //         console.log(x);
                //         console.log(submit.getAttribute("data-button-type"));
                //     })
                //     console.log("lol");
                // });


// '<div class="accordion row #e1bee7 purple lighten-4"><div class="col s4 center-align offset-s2"><span class="valign nameOfStock">'+ s_list[1] +'</span><i class="small material-icons downColor" style="transform: scale(0.5) translateY(5px);"><b><b>arrow_downward</b></b></i></div><div class="col s4 center-align">'+s_list[2]+'</div></div><div class="panel row #e1bee7 purple lighten-4"><button class="buy col s2 offset-s3" onclick="openBuyDiv()" style="padding: 7px">BUY</button><button class="sell col s2 offset-s2" onclick="openSellDiv()" style="padding: 7px">SELL</button></div>'
