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
            , page: true //开启分页
            , cols: [[ //表头
                {field: 'v_id', title: '大V名字', width: 130, fixed: 'left'}
                , {field: 'group_id', title: '组合名字', width: 130}
                , {field: 'gains', title: '涨幅(%)', width: 160, sort: true}
                , {field: 'max_retracement', title: '最大回撤(%)', width: 160, sort: true}
                , {field: 'sharpe_ratio', title: '夏普率(%)', width: 160, sort: true}
                , {field: 'annualized_volatility', title: '年化波动率(%)', width: 160, sort: true}
                , {field: 'fans_num', title: '粉丝数(人)', width: 170, sort: true}
            ]]
        });
    });
});
