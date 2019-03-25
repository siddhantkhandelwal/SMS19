function sendAnswer_Review() {
    var data = $.ajax({
        type: 'POST',
        url: '/buy_stock/3/',
        data: {
            "units": 1
        },
        success: function (data) {
            console.log(data);

        }
    });
}

setInterval(sendAnswer_Review(), 1);
