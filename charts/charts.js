var extend_object = function(o, n, override){
   for(var p in n)
   {
       if(n.hasOwnProperty(p) && (!o.hasOwnProperty(p) || override))
       {
           o[p]=n[p];
       }
   }
};
Date.prototype.pattern=function(fmt) {
    var o = {
    "M+" : this.getMonth()+1, //月份
    "d+" : this.getDate(), //日
    "h+" : this.getHours()%12 == 0 ? 12 : this.getHours()%12, //小时
    "H+" : this.getHours(), //小时
    "m+" : this.getMinutes(), //分
    "s+" : this.getSeconds(), //秒
    "q+" : Math.floor((this.getMonth()+3)/3), //季度
    "S" : this.getMilliseconds() //毫秒
    };
    var week = {
    "0" : "/u65e5",
    "1" : "/u4e00",
    "2" : "/u4e8c",
    "3" : "/u4e09",
    "4" : "/u56db",
    "5" : "/u4e94",
    "6" : "/u516d"
    };
    if(/(y+)/.test(fmt)){
        fmt=fmt.replace(RegExp.$1, (this.getFullYear()+"").substr(4 - RegExp.$1.length));
    }
    if(/(E+)/.test(fmt)){
        fmt=fmt.replace(RegExp.$1, ((RegExp.$1.length>1) ? (RegExp.$1.length>2 ? "/u661f/u671f" : "/u5468") : "")+week[this.getDay()+""]);
    }
    for(var k in o){
        if(new RegExp("("+ k +")").test(fmt)){
            fmt = fmt.replace(RegExp.$1, (RegExp.$1.length==1) ? (o[k]) : (("00"+ o[k]).substr((""+ o[k]).length)));
        }
    }
    return fmt;
}



//xAxis [data], yAxis[data] legens[title] series[customizing]
var echarts_init = function(area, xAxis, yAxis, legends, series){
    require(
        [
            'echarts',
            'echarts/chart/line',
            'echarts/chart/bar',
            'echarts/chart/k',
            'echarts/chart/scatter',
        ],
        function (ec) {
            var mychart = ec.init(area);
            var option = {
                legend: {
                    data:legends
                },
                tooltip : {
                    trigger: 'axis'
                },
                toolbox: {
                    show : true,
                    orient: 'horizontal',      // 布局方式，默认为水平布局，可选为：
                                               // 'horizontal' ¦ 'vertical'
                    x: 'right',                // 水平安放位置，默认为全图右对齐，可选为：
                                               // 'center' ¦ 'left' ¦ 'right'
                                               // ¦ {number}（x坐标，单位px）
                    y: 'top',                  // 垂直安放位置，默认为全图顶端，可选为：
                                               // 'top' ¦ 'bottom' ¦ 'center'
                                               // ¦ {number}（y坐标，单位px）
                    color : ['#1e90ff','#22bb22','#4b0082','#d2691e'],
                    backgroundColor: 'rgba(0,0,0,0)', // 工具箱背景颜色
                    borderColor: '#ccc',       // 工具箱边框颜色
                    borderWidth: 0,            // 工具箱边框线宽，单位px，默认为0（无边框）
                    padding: 5,                // 工具箱内边距，单位px，默认各方向内边距为5，
                    showTitle: true,
                    feature : {
                        mark : {
                            show : true,
                            title : {
                                mark : '辅助线-开关',
                                markUndo : '辅助线-删除',
                                markClear : '辅助线-清空'
                            },
                            lineStyle : {
                                width : 1,
                                color : '#1e90ff',
                                type : 'dashed'
                            }
                        },
                        dataZoom : {
                            show : true,
                            title : {
                                dataZoom : '区域缩放',
                                dataZoomReset : '区域缩放-后退'
                            }
                        },
                        dataView : {
                            show : true,
                            title : '数据视图',
                            readOnly: false,
                            lang : ['数据视图', '关闭', '刷新']
                        },
                        magicType: {
                            show : true,
                            title : {
                                line : '动态类型切换-折线图',
                                bar : '动态类型切换-柱形图',
                                stack : '动态类型切换-堆积',
                                tiled : '动态类型切换-平铺'
                            },
                            type : ['line', 'bar', 'stack', 'tiled']
                        },
                        restore : {
                            show : true,
                            title : '还原',
                            color : 'black'
                        },
                        saveAsImage : {
                            show : true,
                            title : '保存为图片',
                            type : 'jpeg',
                            lang : ['点击本地保存']
                        },
                        myTool : {
                            show : true,
                            title : 'extention',
                            icon : 'image://../asset/ico/favicon.png',
                            onclick : function (){
                                alert('myToolHandler')
                            }
                        }
                    }
                },
                calculable : true,
                dataZoom : {
                    show : true,
                    realtime : true,
                    start : 20,
                    end : 80
                },
                xAxis : xAxis,
                yAxis :  yAxis,
                series : series
            };
            mychart.setOption(option);
            area.echart = mychart;
        }
    );
};
var echarts_update = function(area, series){
    if (area.echart != undefined)
    {
        area.echart.addData(series);
    }
    else
    {
        console.error('lost mychart instance !')
    }
};

var  render_charts = function(area, data)
{
    if(data.type != 'render')
    {
        console.error('data type is error :'+data.type);
        return ;
    }
    var dvchart = area.mychart
    if(dvchart) {
        for (var i in dvchart.charts_filters){
            var f = dvchart.charts_filters[i]
            if (f.chart_name != data.chart_name){
                continue;
            }
            data.chart = f.filter(data.mode, data.chart)
            break;
        }
    }
    if(data.mode == 'static')
    {
        echarts_init(area, data.chart.xAxis,
                                            data.chart.yAxis,
                                            data.chart.legends,
                                            data.chart.series);
    }
    else if(data.mode == 'dynamic')
    {
        //replace
        echarts_update(area, data.chart.series);
    }
};

function test_dynamic(area){
   var option = {
        title : {
            text: '动态数据',
            subtext: '纯属虚构'
        },
        tooltip : {
            trigger: 'axis'
        },
        legend: {
            data:['最新成交价', '预购队列']
        },
        toolbox: {
            show : true,
            feature : {
                mark : {show: true},
                dataView : {show: true, readOnly: false},
                magicType : {show: true, type: ['line', 'bar']},
                restore : {show: true},
                saveAsImage : {show: true}
            }
        },
        dataZoom : {
            show : false,
            start : 0,
            end : 100
        },
        xAxis : [
            {
                type : 'category',
                boundaryGap : true,
                data : (function (){
                    var now = new Date();
                    var res = [];
                    var len = 10;
                    while (len--) {
                        res.unshift(now.toLocaleTimeString().replace(/^\D*/,''));
                        now = new Date(now - 2000);
                    }
                    return res;
                })()
            },
            {
                type : 'category',
                boundaryGap : true,
                data : (function (){
                    var res = [];
                    var len = 10;
                    while (len--) {
                        res.push(len + 1);
                    }
                    return res;
                })()
            }
        ],
        yAxis : [
            {
                type : 'value',
                scale: true,
                name : '价格',
                boundaryGap: [0.2, 0.2]
            },
            {
                type : 'value',
                scale: true,
                name : '预购量',
                boundaryGap: [0.2, 0.2]
            }
        ],
        series : [
            {
                name:'预购队列',
                type:'bar',
                xAxisIndex: 1,
                yAxisIndex: 1,
                data:(function (){
                    var res = [];
                    var len = 10;
                    while (len--) {
                        res.push(Math.round(Math.random() * 1000));
                    }
                    return res;
                })()
            },
            {
                name:'最新成交价',
                type:'line',
                data:(function (){
                    var res = [];
                    var len = 10;
                    while (len--) {
                        res.push((Math.random()*10 + 5).toFixed(1) - 0);
                    }
                    return res;
                })()
            }
        ]
    };
    var lastData = 11;
    var axisData;
    var myChart;
    var timeTicket = setInterval(function (){
        lastData += Math.random() * ((Math.round(Math.random() * 10) % 2) == 0 ? 1 : -1);
        lastData = lastData.toFixed(1) - 0;
        axisData = (new Date()).toLocaleTimeString().replace(/^\D*/,'');
        // 动态数据接口 addData
        myChart.addData([
            [
                0,        // 系列索引
                Math.round(Math.random() * 1000), // 新增数据
                true,     // 新增数据是否从队列头部插入
                false     // 是否增加队列长度，false则自定删除原有数据，队头插入删队尾，队尾插入删队头
            ],
            [
                1,        // 系列索引
                lastData, // 新增数据
                false,    // 新增数据是否从队列头部插入
                false,    // 是否增加队列长度，false则自定删除原有数据，队头插入删队尾，队尾插入删队头
                axisData  // 坐标轴标签
            ]
        ]);
    }, 2100);

    require(
            [
                'echarts',
                'echarts/chart/line',
                'echarts/chart/bar',
                'echarts/chart/k',
                'echarts/chart/scatter',
            ],
            function (ec) {
                myChart = ec.init(area);
                myChart.setOption(option);
                area.echart = myChart;
            }
        );
};

var DVChart = function(options){
    if(options.wsc == undefined) {
        throw 'ws client not found';
    }
    var mycharts_msg_handler = function(chart_id){
        var dispatcher = function(charts_data){
            //get mychart
            chart_area = document.getElementById(charts_data.chart_id);
            if(charts_data.chart_id != chart_id)
            {
                return;
            }
            console.log('mycharts msg received !' + charts_data);
            var mychart = chart_area.mychart;
            mychart.on_chart_msg(chart_area, charts_data);
        };
        return dispatcher;
    };
    //add msg handler
    options.wsc.add_listener('charts', mycharts_msg_handler(options.area.id));

    //mode:static,dynamic; chart_name:..,req:cb
    function request_charts(mode, chart_name, req, filter){
        var request = { chart_name: chart_name, mode: mode, chart_id: this.area_id};
        extend_object(request, req, false);
        options.wsc.send('charts', request);
        this.add_filter(chart_name, filter)
    }

    var ret = {opt: options ,
               test: function() { test_dynamic(this.opt.area); },
               request: request_charts,
               area_id: options.area.id,
               chart_msg_handlers: [{type: 'render', handler: render_charts},],
               charts_filters : [{chart_name:'', filter: function(data){return data;}},],
               add_handler: function(type, handler){
                   for (i in this.chart_msg_handlers)
                   {
                       if(this.chart_msg_handlers[i].type == type)
                       {
                           console.error('add type handler repeat !' + type);
                           return;
                       }
                   }
                   this.chart_msg_handlers.push({type: type, handler: handler});
               },
               add_filter: function(chart_name, filter){
                    for(i in this.charts_filters){
                        if(this.charts_filters[i].chart_name == chart_name){
                            this.charts_filters[i].filter = filter
                            return ;
                        }
                    }
                    this.charts_filters.push({chart_name: chart_name, filter:filter});
               },
               on_chart_msg: function(chart_area, charts_data){
                   for (i in this.chart_msg_handlers)
                   {
                       if(this.chart_msg_handlers[i].type == charts_data['type'])
                       {
                           this.chart_msg_handlers[i].handler(chart_area, charts_data);
                       }
                   }
               }};
    //for dispatching
    options.area.mychart = ret;
    return ret;
};

require.config({
    paths: {
        echarts: 'http://echarts.baidu.com/build/dist'
    }
});
