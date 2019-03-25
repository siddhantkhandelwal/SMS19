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
        success: function (data) {
            stock_list = data.stocks_purchased;
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
                price.innerHTML = s_list[2];

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
                sellButton.setAttribute("id", "sell-btn" + s_list[0].toString());
                sellButton.setAttribute("class", "sell col s2 offset-s2");
                sellButton.setAttribute("data-pk", s_list[0]);
                sellButton.innerHTML = "SELL";
                sellButton.style.padding = "5px";
                // buyButton.style.display = "none";
                // buyButton.innerHTML = s_list;

                var userBalance = document.getElementById("balance");
                userBalance.innerHTML = `User Balance: ${balance}`;
                panel.appendChild(buyButton);
                innerDiv.appendChild(span);
                accordion.appendChild(innerDiv);
                accordion.appendChild(price);
                accordion.appendChild(units);
                units.appendChild(span2);
                panel.appendChild(buyButton); panel.appendChild(sellButton);
                document.getElementsByClassName("stock_list")[0].appendChild(accordion.cloneNode(true));
                document.getElementsByClassName("stock_list")[0].appendChild(panel);
            }
            var acc = document.getElementsByClassName("accordion");
            var i = 0;

            while (i < acc.length) {
                acc[i].addEventListener("click", function () {
                    this.classList.toggle("active");
                    var panel = this.nextElementSibling;
                    // panel.style.maxHeight = panel.scrollHeight + "px";
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
                buy[j].addEventListener("click", function () {
                    alpha = this.getAttribute("data-pk");
                    document.getElementById("buyDiv").style.display = "block";
                    document.getElementById("buyInfo").innerHTML = "Stock: " + s_list[1] + " Price:     " + s_list[0];
                });
                j++;
            }
            //FOR SELL BUTTONS
            while (x < sell.length) {
                // console.log("abcd");
                sell[x].addEventListener("click", function () {
                    alpha = this.getAttribute("data-pk");
                    document.getElementById("sellDiv").style.display = "block";
                    document.getElementById("sellInfo").innerHTML = "Stock: " + s_list[1] + " Price:     " + s_list[0];
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
document.getElementById("indian1").addEventListener("click", function () { get_stock_list("BSE"); });
document.getElementById("international1").addEventListener("click", function () { get_stock_list("NYM"); });
document.getElementById("international2").addEventListener("click", function () { get_stock_list("JPN"); });

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
            document.getElementById("balance").innerHTML = "Balance: " + balance.toString();
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

function addTabs() {
    if (window.innerWidth > 500) {
        document.getElementById("heading").innerHTML = "&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;PORTFOLIO";
    }
}

addTabs();

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
