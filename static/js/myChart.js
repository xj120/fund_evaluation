const myChart = echarts.init(document.getElementById("lines"));
myChart.setOption({
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
            saveAsImage: {}
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
    series: [
        {
            name: '邮件营销',
            type: 'line',
            data: []
        },
        {
            name: '联盟广告',
            type: 'line',
            data: []
        },
        {
            name: '视频广告',
            type: 'line',
            data: []
        },
        {
            name: '直接访问',
            type: 'line',
            data: []
        },
        {
            name: '搜索引擎',
            type: 'line',
            data: []
        },
    ]
});
myChart.showLoading();
const names = [];
const series1 = [];
const series2 = [];
$.ajax({  //TODO
    type: 'get',
    url: '../static/danjuan3.json',
    dataType: "json",
    success: function (result) {
        $.each(result.items, function (index, item) {
            names.push(item.date);
            series1.push(item.percentage);
        });
        myChart.hideLoading();
        myChart.setOption({
            xAxis: {
                data: names
            },
            series: [
                {
                    data: series1
                },
                {
                    data: series1
                }
            ]
        })
    },
    error: function () {
        alert("图表请求数据失败！");
        myChart.hideLoading();
    }
});