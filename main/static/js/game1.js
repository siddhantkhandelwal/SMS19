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
        url: `/get_stocks_data/${code}`, //Do not edit these special commas. Everything will go to shit.
        data: {},
        beforeSend: function () {
            $('.loader').show();
        },
        complete: function () {
            $('.loader').hide();
        },
        success: function (data) {

            let marketStatus  = true;
            if(!marketStatus) {
                alert('This market has been temporarily closed by EFA');
            }

            console.log(data);
            stock_list = data.stocks_list;
            // balance = data.balance;
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

                var unitDiv = document.createElement("div");
                unitDiv.setAttribute("class", "col s4 center-align");

                var span2 = document.createElement("span");
                span2.setAttribute("class", "valign");
                span2.innerHTML = s_list[4];

                var panel = document.createElement("div");
                panel.setAttribute("class", "panel row #e1bee7 purple lighten-4");
                panel.style.transition = "height 0.1s linear";

                var buyButton = document.createElement("button");
                buyButton.setAttribute("id", "buy-btn" + i.toString());
                buyButton.setAttribute("data-pk", s_list[0]);
                buyButton.setAttribute("class", "buy col s2 offset-s5");
                buyButton.style.padding = "5px";
                buyButton.innerHTML = "BUY";

                unitDiv.appendChild(span2);
                innerDiv.appendChild(span);
                accordion.appendChild(innerDiv);

                //Fifth element of StockTrend required here. Demo functioning with number of stocks available.
                console.log(s_list);
                if (s_list[5] > 0) {
                    price.appendChild(trendSpanUp);
                }
                else {
                    price.appendChild(trendSpanDown);
                }

                accordion.appendChild(price);
                accordion.appendChild(unitDiv);
                panel.appendChild(buyButton);
                document.getElementsByClassName("stock_list")[0].appendChild(accordion.cloneNode(true));
                document.getElementsByClassName("stock_list")[0].appendChild(panel);
            }
            var acc = document.getElementsByClassName("accordion");
            var i = 0;

            while (i < acc.length) {
                // console.log("acd");
                acc[i].addEventListener("click", function () {
                    this.classList.toggle("active");
                    var panel = this.nextElementSibling;
                    // console.log(panel);
                    // panel.style.maxHeight = panel.scrollHeight + "px";
                    let stockStatus = true;
                    if( !stockStatus) {
                        alert('This stock has been closed by EFA.');
                        return;
                    }
                    if (panel.style.height) {
                        panel.style.height = null;
                    } else {
                        panel.style.height = "60px";
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
                    // console.log(list_of_stocks, j);
                    let btnId = e.target.id.toString();
                    btnId = btnId.substring(btnId.length - 1);
                    document.getElementById("buyInfo").innerHTML = "Stock: " + stock_list[btnId][1] + ", Price:     " + stock_list[btnId][2];
                });
                j++;
            }
            //FOR SELL BUTTONS
            while (x < sell.length) {
                // console.log("abcd");
                sell[x].addEventListener("click", function () {
                    alpha = this.getAttribute("data-pk");
                    document.getElementById("sellDiv").style.display = "block";
                });
                x++;
            }

            //FOR SUBMITTING BUY REQUEST
            $("#submit_buy").off();
            $("#submit_buy").on("click", function () {
                var inputNumber = document.getElementById("number").value;
                // console.log(alpha);
                // console.log(inputNumber);
                // console.log("buy");
                buyStock(parseInt(alpha), parseFloat(inputNumber), code);
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
            // console.log(data);
            document.getElementById("popup").style.display = "block";
            document.getElementById("popup").innerHTML = data.message;
            setTimeout(function () {
                document.getElementById("popup").style.display = "none";
            }, 5000);
            getBalance();
            get_stock_list(code);
            document.getElementById("number").value = "";
            $('.closeBuySellDiv').trigger('click');
        }
    });
}

function sellStock(pk, units) {

    // console.log(units);

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
            console.log(data);
        }
    });
}

function getBalance() {
    var data = $.ajax({
        type: 'GET',
        url: `/get_balance`,
        data: {},
        success: function (data) {
            // console.log(data);
            balance = data.balance;
            document.getElementById("balance").innerHTML = "Balance: " + balance.toString();
        }
    });
}

getBalance();
function hideBuyDiv() {
    document.getElementById("buyDiv").style.display = "none";
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
