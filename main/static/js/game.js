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

function get_stock_list(code) {
  var data = $.ajax({
      type: 'POST',
      url: '/',
      data: {
          "code": code
      },
      success: function (data) {
          console.log(data); 
      }
  });
}
document.getElementById("indian1").addEventListener("click", function(){get_stock_list("BSE");});
document.getElementById("international1").addEventListener("click", function(){get_stock_list("NYM");});
