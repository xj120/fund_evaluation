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
                {field: 'v_id', title: '组合号', width: 110, fixed: 'left'}
                , {field: 'group_id', title: '组合名字', width: 170}
                , {field: 'gains', title: '涨幅(%)', width: 120, sort: true}
                , {field: 'max_retracement', title: '最大回撤(%)', width: 140, sort: true}
                , {field: 'sharpe_ratio', title: '夏普率(%)', width: 120, sort: true}
                , {field: 'annualized_volatility', title: '年化波动率(%)', width: 150, sort: true}
                , {field: 'fans_num', title: '粉丝数(人)', width: 130, sort: true}
                , {field: 'hold_time', title: '持有时间()', width: 130, sort: true}
                , {field: 'adjust_level', title: '调仓水平', width: 130, sort: true}
            ]]
        });
    });
});
