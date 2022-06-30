$(function () {
    layui.use('table', function () {
        let table = layui.table;
        //第一个实例
        table.render({
            elem: '#datatable'
            , method: 'get'
            , url: '../static/data/table.json'
            , height: 510
            , toolbar: true
            , page: false //分页
            , cols: [[ //表头
                {field: 'v_id', title: '组合ID', width: 100, fixed: 'left'}
                , {field: 'manager_name', title: '大V名字', width: 100}
                , {field: 'group_id', title: '组合名字', width: 100}
                , {field: 'gains', title: '涨幅(%)', width: 100, sort: true}
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
});
