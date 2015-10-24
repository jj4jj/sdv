#SDV#

[SDV][1] is a simple realtime data visualization solutions with Python and HTML5.

##structure##
* front end

  * cavas render library echarts for chart rendering

  * websocket for realtime data pushing

* back end
 * python tornado  for websocketserver

 * mysql for data persistence (history)

 * redis for a publisher-subscriber supporting




### install && run ###

    
    sudo apt-get install mysql-server redis libmysqlclient-dev
    pip install tornado 
    pip install mysql-python
    pip install redis
    git clone https://github.com/jj4jj/sdv.git    
    cd sdv
    vim config.py #edit the config file for log , db and  redis settings
    vim charts/charts.html
    python main.py
    cp -rf charts/*.* <websesrver_doc>/
    visit : http://<host>/pathto/charts/charts.html



###test "online" demo###
![online][2]




Any usage problems can send me email resc@vip.qq.com

[1]: https://github.com/jj4jj/sdv
[2]: https://github.com/jj4jj/sdv/blob/master/online.png
