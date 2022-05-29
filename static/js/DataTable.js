layui.use('table', function () {
    const table = layui.table;
    //第一个实例
    table.render({
        elem: '#datatable'
        , title: '数据表格'
        , height: 510
        , toolbar: true
        , page: true //开启分页
        , data: [
            { //TODO
                'v_id': 10,
                'group_id': 20,
                'gains': 1,
                'max_retracement': 2,
                'sharp_ratio': 3,
                'annualized_volatility': 4,
                'fans_num': 100
            },
            {
                'v_id': 666,
                'group_id': 777,
                'gains': 888,
                'max_retracement': 999,
                'sharp_ratio': 7,
                'annualized_volatility': 5,
                'fans_num': 1300
            }
        ]
        , cols: [[ //表头
            {field: 'v_id', title: '大V名字', width: 130, fixed: 'left'}
            , {field: 'group_id', title: '组合名字', width: 130}
            , {field: 'gains', title: '涨幅(%)', width: 160, sort: true}
            , {field: 'max_retracement', title: '最大回撤(%)', width: 160, sort: true}
            , {field: 'sharp_ratio', title: '夏普率(%)', width: 160, sort: true}
            , {field: 'annualized_volatility', title: '年化波动率(%)', width: 160, sort: true}
            , {field: 'fans_num', title: '粉丝数(人)', width: 170, sort: true}
        ]]
    });
});