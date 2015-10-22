//url, listener, reconnect, onopen, onclose, onerr
function WSClient(options)
{
    //return object
    var ws = new WebSocket(options.uri);
    ws.onmessage = function (evt) {
        console.log('recv msg:'+evt.data);
        objmsg = eval('('+evt.data+')');
        for(i in wsc.listener)
        {
            if(wsc.listener[i].type == objmsg.type)
            {
                console.log('listener handle msg .type:'+objmsg.type)
                wsc.listener[i].handler(objmsg.data);
            }
        }
    };
    ws.onclose = function(evt){
        console.log('websocket close , evt:'+evt.toString());
        if(options.onclose != undefined)
        {
            options.onclose(evt);
        }
        if(ws.heart_beat_timer != undefined)
        {
            clearInterval(ws.heart_beat_timer);
            ws.heart_beat_timer = undefined;
        }
    };
    ws.onerror = function (evt){
        console.error('socket error !');
        if(options.onerr != undefined)
        {
            options.onerr(evt);
        }
        if(ws.heart_beat_timer != undefined)
        {
            clearInterval(ws.heart_beat_timer);
            ws.heart_beat_timer = undefined;
        }
    };
    ws.onopen = function() {
        console.log('open websocket success!');
        if (options.onopen != undefined) {
            options.onopen();
        }
        if(options.heart_beat_time == undefined ||
            options.heart_beat_time < 5000)
        {
            options.heart_beat_time = 5000;
        }
        //set heart-beat-msg
        ws.heart_beat_timer = setInterval(function(){
            wsc.send('ping', '-*-heart-beat-*-');
        }, options.heart_beat_time);
    };

    var wsc = {socket : ws,
            listener: [{type:'',
                        handler:function(msg){
                            console.log('dummy msg received!');
                        }
                      },
            ],
            add_listener :function(type, handler){
                this.listener.push({type: type, handler: handler});
            },
            send: function (type, msg){
                var objmsg = {'data':msg, 'type':type};
                var jmsg = JSON.stringify(objmsg);
                return this.socket.send(jmsg);
            },
            onready: function( func ){
                if (this.socket.readyState == WebSocket.OPEN)
                {
                    func();
                }
                else if(this.socket.readyState == WebSocket.CONNECTING)
                {
                    //when open do
                    var oldfunc = this.socket.onopen;
                    this.socket.onopen = function(){
                        if(oldfunc != undefined)
                        {
                            oldfunc();
                        }
                        func()
                    }
                }
                else
                {
                    console.error('error state :' + (this.socket.readyState));
                }
            }
    };
    return wsc;
}

