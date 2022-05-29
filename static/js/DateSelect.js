function renderTime(elem, value, range) {
    layui.laydate.render({
        elem: elem, //绑定元素
        value: value, //默认值
        range: range, //是否开启时间范围
        done: function (value, date, endDate) {
            console.log(value); //得到日期生成的值，如：2022-08-18 - 2022-09-01
            console.log(date); //得到日期时间对象：{year: 2022, month: 8, date: 18, hours: 0, minutes: 0, seconds: 0}
            console.log(endDate); //得结束的日期时间对象，开启范围选择（range: true）才会返回。对象成员同上。
        }, //选择时间触发的回调函数
        trigger: 'click',
        theme: '#5b5b5b', //主题色
    });
}
renderTime("#timer", "", ["#sTime", '#eTime']);