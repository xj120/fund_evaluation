const myChart = echarts.init(document.getElementById("lines"));
let option = {
    title: {
        text: '收益曲线',
        textAlign: 'center',
        textStyle: {
            fontSize: 20
        },
        subtext: '点击图例添加/移除组合',
        subtextStyle: {
            fontSize: 12,
            color: '#5b5b5b',
        },
        left: 100,
        top: -3
    },
    tooltip: {
        //触发方式 - 坐标轴
        trigger: 'axis'
    },
    grid: {
        containLabel: true
    },
    toolbox: {
        feature: {
            saveAsImage: {},
            dataView: { //数据视图
                show: true
            },
            restore: {                             //配置项还原。
                show: true,                         //是否显示该工具。
                title: "还原",
            },
        },
        right: 30
    },
    legend: {
        x: 'left',
        padding: [0, 0, 0, 185],
        width: 700,
        itemWidth: 16
    },
    xAxis: {
        data: [],
        type: 'category',
        boundaryGap: false,
    },
    yAxis: {
        name: '涨幅(%)',
        type: 'value',
        nameTextStyle: {
            padding: [0, 0, -225, -150],
            fontSize: 14,
            color: '#000000'
        },
    },
    dataZoom: [
        {
            type: 'slider',
            start: 10,
            end: 60,
            bottom: 0,
        },
        {
            type: 'inside',
            start: 10,
            end: 60,
            bottom: 0,
        },
    ],
    series: []
}
myChart.showLoading();
$.ajax({
    type: 'get',
    url: '../static/data/test.json',
    dataType: "json",
    success: function (result) {
        let series_list = [];

        option.xAxis.data = result.dateTime;
        option.series = result.series;
        myChart.setOption(option);
        myChart.hideLoading();
    },
    error: function () {
        alert("图表请求数据失败！");
        myChart.hideLoading();
    }
});