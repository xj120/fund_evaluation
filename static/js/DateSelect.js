function renderTime(elem, value, range) {
    layui.laydate.render({
        elem: elem, //绑定元素
        value: value, //默认值
        range: range, //是否开启时间范围
        done: function (value, date, endDate) {
            // console.log(value); //得到日期生成的值，如：2022-08-18 - 2022-09-01
            // console.log(date); //得到日期时间对象：{year: 2022, month: 8, date: 18, hours: 0, minutes: 0, seconds: 0}
            // console.log(endDate); //得结束的日期时间对象，开启范围选择（range: true）才会返回。对象成员同上。
            // console.log(date['year']);
            let s_year = date['year'];
            let s_month = date['month'];
            let s_day = date['date'];
            let e_year = endDate['year'];
            let e_month = endDate['month'];
            let e_day = endDate['date'];
            $.ajax({
                url: "/testAjax",
                type: 'POST',
                dataType: 'json',//表示返回的数据必须为json，否则：会走下面error对应的方法。
                data: {
                    value: value,
                    date: date,
                    endDate: endDate
                },
                success: function (data) {
                },
                error: function () {
                    alert("数据发送失败！");
                }
            })
        }, //选择时间触发的回调函数
        trigger: 'click',
        theme: '#5b5b5b', //主题色
    });
}

renderTime("#timer", "", ["#sTime", '#eTime']);
