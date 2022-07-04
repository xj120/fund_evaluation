function renderTime(elem, value, range) {
    layui.laydate.render({
        elem: elem, //绑定元素
        value: value, //默认值
        range: range, //是否开启时间范围
        done: function (value, date, endDate) {
            //console.log(date); //得到日期时间对象：{year: 2022, month: 8, date: 18, hours: 0, minutes: 0, seconds: 0}
            //console.log(endDate); //得结束的日期时间对象，开启范围选择（range: true）才会返回。对象成员同上。
            let s_year = date['year'];
            let s_month = date['month'];
            let s_day = date['date'];
            let e_year = endDate['year'];
            let e_month = endDate['month'];
            let e_day = endDate['date'];
            $.ajax({
                url: "/testAjax/s_year=" + s_year + "&s_month=" + s_month + "&s_day=" + s_day + "&e_year=" + e_year + "&e_month=" + e_month + "&e_day=" + e_day,
                type: 'GET',
                dataType: 'json',//表示返回的数据必须为json，否则：会走下面error对应的方法。
                success: function (data) {
                    if (data['success'] === 'true') {
                        redrawTable()
                        initLine()
                    }
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


function redrawTable() {
    layui.use('table', function () {
        let table = layui.table;
        //第一个实例
        table.render({
            elem: '#datatable'
            , method: 'GET'
            , url: '/redrawTable'
            , height: 510
            , toolbar: true
            , page: false //分页
            , cols: [[ //表头
                {field: 'v_id', title: '组合ID', width: 100, fixed: 'left'}
                , {field: 'manager_name', title: '大V名字', width: 100}
                , {field: 'group_id', title: '组合名字', width: 100}
                , {field: 'gains', title: '累计涨幅(%)', width: 123, sort: true}
                , {field: 'max_retracement', title: '最大回撤(%)', width: 123, sort: true}
                , {field: 'sharpe_ratio', title: '夏普率(%)', width: 110, sort: true}
                , {field: 'annualized_volatility', title: '年化波动率(%)', width: 138, sort: true}
                , {field: 'rate_per_ann', title: '年化收益率(%)', width: 138, sort: true}
                , {field: 'fans_num', title: '粉丝数(人)', width: 115, sort: true}
                , {field: 'average_holding_time', title: '持有时间(月)', width: 125, sort: true}
                , {field: 'reposition_level', title: '调仓水平', width: 110, sort: true}
            ]]
        });

    });
}


function initLine() {
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
            width: 1100,
            itemWidth: 16
        },
        xAxis: {
            data: [],
            type: 'time',
            boundaryGap: false
        },
        yAxis: {
            name: '累计涨幅(%)',
            type: 'value',
            nameTextStyle: {
                padding: [0, 0, -225, -150],
                fontSize: 14,
                color: '#000000'
            },
        },
        series: []
    }
    let data1 = [0, 0];
    myChart.showLoading();
    $.ajax({
        type: 'GET',
        url: '/redrawLine',
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
                                data: [],
                                showSymbol: false
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
}