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
        type: 'time',
        boundaryGap: false
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
            start: 0,
            end: 20,
            bottom: 0,
        },
        {
            type: 'inside',
            start: 0,
            end: 20,
            bottom: 0,
        },
    ],
    series: []
}
let data1 = [0, 0];
myChart.showLoading();
$.ajax({
    type: 'get',
    url: '../static/data/line.json',
    dataType: "json",
    success: function (result) {
        if (result.data.length > 0) {
            for (let i = 0; i < result.data.length; i++) {
                //在数组中找到符合条件的第一个元素，返回该元素
                let found = option.series.find(element => result.data[i].name === element.name);
                if (typeof found == "undefined") {//此处为了避免下面if里面的found.name报未定义
                    found = {
                        name: '我是测试名字'//给一个基本不会有的数据就行
                    }
                }
                if (result.data[i].name === found.name) {//如果series数组中有data当前对象的名称，直接添加
                    data1 = [0, 0];
                    data1[0] = result.data[i].date;
                    data1[1] = result.data[i].daily_rise_drop;
                    found.data.push(data1);
                } else {//如果没有，就新push一个series元素,此处要注意series数据结构理解
                    option.series.push(
                        {
                            name: result.data[i].name,
                            type: 'line',
                            data: []
                        }
                    )
                    //重复上面if里面的内容
                    data1 = [0, 0];
                    let sFound = option.series.find(element => result.data[i].name === element.name);
                    data1[0] = result.data[i].date;
                    data1[1] = result.data[i].daily_rise_drop;
                    sFound.data.push(data1);
                }
            }
            myChart.setOption(option);
        } else {
            alert("数据不存在，无法生成图表！")
        }
        myChart.hideLoading();
    },
    error: function () {
        alert("图表请求数据失败！");
        myChart.hideLoading();
    }
});