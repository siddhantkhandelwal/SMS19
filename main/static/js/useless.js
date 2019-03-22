function sendAnswer_Review() {
    var data = $.ajax({
        type: 'POST',
        url: '/buy_stock/13/',
        data: {
            "units": 2
        },
        success: function (data) {
            console.log(data);
        }
    });
}

sendAnswer_Review();
