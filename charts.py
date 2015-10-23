#coding:utf8
import log
import threading

#title , point sets
"""
data.chart.xAxis =  [
                    {
                        type : 'category',
                        data : ["衬衫","羊毛衫","雪纺衫","裤子","高跟鞋","袜子"]
                    }
                ],
data.chart.yAxis =  [
                    {
                        type : 'value'
                    }
                ],
data.chart.legends = ['title1','title2'],
data.chart.series =  [
                    {
                        "name":"销量",
                        "type":"bar",
                        "data":[5, 20, 40, 10, 10, 20]
                    }
                ]
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
"""



class ChartAgent:
    def __init__(self, client, chart_id, chart_name):
        #{u'chart_id': u'chart', u'type': u'line', u'mode': u'static'}
        self.client = client
        self.chart_id = chart_id
        self.chart_name = chart_name
        self.chart = {}

    def _draw(self, titles, names, types, datasets):
        self.chart['legends'] = titles
        self.chart['xAxis'] = map(
            lambda dataset: {'type': 'category',
                'data': [d[0] for d in dataset]}, datasets)

        self.chart['yAxis'] = [
            {'type': 'value'} for d in datasets
        ]
        series = []
        for i in xrange(len(datasets)):
            series.append({
                'name': names[i],
                'type': types[i],
                'data': [d[1] for d in datasets[i]]
            })
        self.chart['series'] = series
        ####################################################
        msg = {'type': 'render',
               'mode': 'static',
               'chart': self.chart,
               'chart_id': self.chart_id,
               'chart_name': self.chart_name}
        self.client.reply('charts', msg)

    def draw_line(self, title, name, dataset):
        self._draw([title], [name], ['line'], [dataset])


    def draw_ohlc(self, title, name, dataset):
        """
        :param dataset: [time open high low close]
        :return:
        """
        self._draw([title], [name], ['k'], [dataset])

    def draw_bar(self,title, name, dataset):
        self._draw([title], [name], ['bar'], [dataset])

    def draw_scatter_point(self, title, name, dataset):
        self._draw([title], [name], ['scatter'], [dataset])

    def data(self):
        return self.chart

    def format_series(self, points):
        series = []
        for i in xrange(0, len(points)):
            series.append([i, points[i][1], False, True, points[i][0]])
        return {'series': series}

    #send client addition
    def update(self, point):
        log.debug('update point:'+str(point))
        update_data = self.format_series([point])
        msg = {'type': 'render',
               'mode': 'dynamic',
               'chart': update_data,
               'chart_id': self.chart_id,
               'chart_name': self.chart_name}
        self.client.reply('charts', msg)


    #############################################################################
    def test(self, chart_id):
        self.draw_line(chart_id, 'hello', 'name', [[1, 2], [2, 3], [4, 5], ['hf', 24]])

if __name__ == '__main__':
    mychart = ChartAgent('')
    mychart.draw_line('chart_id', 'hello', 'name', [[1, 2], [2, 3], [4, 5], ['hf', 24]])
    print mychart.data()