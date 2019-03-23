var acc = document.getElementsByClassName("accordion");
var i;

for (i = 0; i < acc.length; i++) {
  acc[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var panel = this.nextElementSibling;
    if (panel.style.maxHeight){
      panel.style.maxHeight = null;
    } else {
      panel.style.maxHeight = panel.scrollHeight + "px";
    }
  });
}

function openBuyDiv() {
    document.getElementById("buyDiv").style.display = "block";
}

function closeBuyDiv() {
    document.getElementById("buyDiv").style.display = "none";
}

function openSellDiv() {
    document.getElementById("sellDiv").style.display = "block";
}

function closeSellDiv() {
    document.getElementById("sellDiv").style.display = "none";
}
var x = document.getElementById("csrf").getAttribute("value");
console.log(x);

function get_stock_list(code) {
    var data = $.ajax({
        type: 'GET',
        url: `/get_game_data/${code}`, //Do not edit these special commas. Everything will go to shit.
        data: {},
        success: function (data) {
            console.log(data);
            stock_list = data.stock_list;
            document.getElementsByClassName("accordion row #e1bee7 purple lighten-4")[0].innerHTML = ""
            for(var i = 0; i < stock_list.length; i++){
                s_list = stock_list[i];
                document.getElementsByClassName("accordion row #e1bee7 purple lighten-4")[0].innerHTML +=  '<div class="accordion row #e1bee7 purple lighten-4" id =' + s_list[0] + '><div class="col s4 center-align offset-s2"><span class="valign nameOfStock">' + s_list[1] + '</span><i class="small material-icons downColor" style="transform: scale(0.5) translateY(5px);"><b><b>arrow_downward</b></b></i></div><div class="col s4 center-align">' + s_list[2] + '</div></div>';          
              }
        }
    });
  }
  
get_stock_list("BSE");
document.getElementById("indian1").addEventListener("click", function(){get_stock_list("BSE");});
document.getElementById("international1").addEventListener("click", function(){get_stock_list("NYM");});
