$(document).ready(function() {
    var data_act;
    var visdata = new vis.DataSet(); // vis dataset
    var checkbox_array = [];
    var labels = {};
    var stringTopic = [];
    var check_pause = false;
    var socket = io.connect('http://127.0.0.1:5000');

    function _update_time(){
        var launch = document.getElementById("command").value;
        socket.send(launch);
        if (check_pause == false){
            setTimeout(() => {  
                _update_time();
            }, 2000);
        }

    }
    $('#LIVE').on('click', function() {
        document.getElementById("live_func").style.display = "none";
        document.getElementById("recording").style.display = "block";

        _update_time();
    });
    
    socket.on('message', function(msg) {
        mainFunc(msg);
    });

    $('#pause').on('click', function() {
        check_pause = true;
        document.getElementById("UpdateButton").style.display = "block";
        document.getElementById("container").style.display = "block";
        document.getElementById("selectTopics").style.display = "block";
        document.getElementById("resume").style.display = "block";
        document.getElementById("pause").style.display = "none";
    });

    $('#resume').on('click', function() {
        document.getElementById("pause").style.display = "block";
        document.getElementById("UpdateButton").style.display = "none";
        document.getElementById("container").style.display = "none";
        document.getElementById("selectTopics").style.display = "none";
        document.getElementById("resume").style.display = "none";
        check_pause = false;
        _update_time();
    });

    async function mainFunc(msgdata){
        await new Promise(resolve => setTimeout(resolve, 100));
        var jsonfile = msgdata;
        data_act = JSON.parse(jsonfile);
        var actual_data = JsonVisData(data_act, visdata, true);
        chart(actual_data, 'visualization');
        document.getElementById("topicsLabel").style.display = "block";
        document.getElementById("legendText").style.display = "block";
        document.getElementById("btnHome").style.display = "block";
        document.getElementById("visualization").style.display = "block";
        if (check_pause == false){
            document.getElementById("selectTopics").style.display = "none";
            document.getElementById("container").style.display = "none";
            document.getElementById("UpdateButton").style.display = "none";
            document.getElementById("resume").style.display = "none";
            document.getElementById("pause").style.display = "block";
        }
    }
    
    $('#UpdateButton').on('click', function() {
        var new_data_act = Array.from(data_act);
        stringTopic.forEach(item => {
            new_data_act.forEach(row => {
                new_data_act=new_data_act.filter(function(itm){return itm.Topic!==item.substring(6,)});
            });
        });
        var actual_data = JsonVisData(new_data_act, visdata, false);
        chart(actual_data, 'visualization');
        return new_data_act;
    });
    
    function JsonVisData(data_act1, visdata, checking){
        labels = {};
        visdata.clear();
        data_act1.forEach(row => {
            Date_split = row.Time.split(" ");
            Time_split = Date_split[3].split(":");
            const Dat = parseInt(Date_split[0]);
            const Month = parseInt(Date_split[1]);
            const Year = parseInt(Date_split[2]);
            const Hour = parseInt(Time_split[0]);
            const Min = parseInt(Time_split[1]);
            const Sec = parseInt(Time_split[2]);
            const Nsec = parseInt(Date_split[4]);
            const Msec = parseInt(Nsec/Math.pow(10, 4));
            const DateTime = new Date(Year, Month-1, Dat, Hour, Min, Sec, Msec);
            const Topic = row.Topic;
            const Msg = row.Message.trim();
            const Color = row.Color.replace(/\s/g,'');
            if (Msg == 'e_stopped' || Msg == 'e_stop'){
                injectStyles(Color, 'circle')
                var classcolor = Color.replace('(', '').replace(')', '').replace(/,/g,'');
                const Title = '<table border="1"><tr><td>Topic : '+ Topic + '</td></tr><tr><td>Message : ' + Msg + '</td></tr><tr><td>Timestamp : ' + Dat + "/" + Month + "/" + Year + " " + Date_split[3] + " " + Nsec + '</td></tr></table>';
                var items = [{start:DateTime, content: '', className: classcolor + '_circle', title: Title, selectable: true, editable:{remove:false}}];
                labels["  " + Topic] = Color;
                visdata.add(items);
                if (checking == true){
                    checkbox_array.push("check_" + Topic);
                }
            }else if (Msg == 'e_start'){
                injectStyles(Color, 'square')
                var classcolor = Color.replace('(', '').replace(')', '').replace(/,/g,'');
                const Title = '<table border="1"><tr><td>Topic : '+ Topic + '</td></tr><tr><td>Message : ' + Msg + '</td></tr><tr><td>Timestamp : ' + Dat + "/" + Month + "/" + Year + " " + Date_split[3] + " " + Nsec + '</td></tr></table>';
                var items = [{start:DateTime, content: '', className: classcolor + '_square', title: Title, selectable: true, editable:{remove:false}}];
                labels["  " + Topic] = Color;
                visdata.add(items);
                if (checking == true){
                    checkbox_array.push("check_" + Topic);
                }
            }else if (Msg == 'e_success'){
                injectStyles(Color, 'oval')
                var classcolor = Color.replace('(', '').replace(')', '').replace(/,/g,'');
                const Title = '<table border="1"><tr><td>Topic : '+ Topic + '</td></tr><tr><td>Message : ' + Msg + '</td></tr><tr><td>Timestamp : ' + Dat + "/" + Month + "/" + Year + " " + Date_split[3] + " " + Nsec + '</td></tr></table>';
                var items = [{start:DateTime, content: '.', className: classcolor + '_oval', title: Title, selectable: true, editable:{remove:false}}];
                labels["  " + Topic] = Color;
                visdata.add(items);
                if (checking == true){
                    checkbox_array.push("check_" + Topic);
                }
            }
        });
        if (checking == true){
            checkMain(checkbox_array);
        }
        return visdata;
    }

    function checkMain(checkbox_array){
        document.getElementById('container').innerHTML = "";
        checkbox_array = Array.from(new Set(checkbox_array))
        checkbox_array.forEach(ele => {
            addCheckbox(ele.substring(6,));
        });  
    }
    var options = {
        editable: true
    };

    function chart(visdata, divID){
        // Creates timeline graph
        document.getElementById(divID).innerHTML = "";
        var container = document.getElementById(divID);
        var options = {
            editable: true
        };
        timeline = new vis.Timeline(container, visdata, options);
        colorize(labels);
    }

    function colorize(colorList) {
        var container = document.getElementById('legend');
        document.getElementById('legend').innerHTML = "";                
        for (var key in colorList) {
            var boxContainer = document.createElement("DIV");
            var box = document.createElement("DIV");
            var label = document.createElement("SPAN");
            label.innerHTML = key;
            box.className = "box";
            box.style.backgroundColor = 'rgb' + colorList[key].substring(6,);

            boxContainer.appendChild(box);
            boxContainer.appendChild(label);
            container.appendChild(boxContainer);
        }
    }

    $('#container').on('click', function() {
        stringTopic = [];
        selectedTopic = []; 
        checkbox_array.forEach(ele => {
            var checkBox = document.getElementById(ele);
            if (checkBox.checked == true){
                selectedTopic.push(ele)
            } else {                    
            }
        });
        stringTopic = checkbox_array.filter(function(obj) { return selectedTopic.indexOf(obj) == -1; });
        return stringTopic;
    });

    function addCheckbox(Topic){    
        var node = document.createElement('div');        
        node.innerHTML = '<input type="checkbox" checked=true id="check_' + Topic + '" name="check' + Topic + '"><label for="check' + Topic + '">'+ Topic +'</label>';       
        document.getElementById('container').appendChild(node);
    }

    $('#selectall').on('click', function() {
        var selectall = document.getElementById('selectall');
        if (selectall.checked == true){
            checkbox_array.forEach(ele => {
                document.getElementById(ele).checked = true;
            });
        } else {
            checkbox_array.forEach(ele => {
                document.getElementById(ele).checked = false;
            });            
        }
        stringTopic = [];
        selectedTopic = []; 
        checkbox_array.forEach(ele => {
            var checkBox = document.getElementById(ele);
            if (checkBox.checked == true){
                selectedTopic.push(ele)
            } else {                    
            }
        });
        stringTopic = checkbox_array.filter(function(obj) { return selectedTopic.indexOf(obj) == -1; });
        return stringTopic;
    });

    function injectStyles(colors, shape) {
        var style = document.createElement('style');
        style.type = 'text/css';
        var classcolor = colors.replace('(', '').replace(')', '').replace(/,/g,'');
        if (shape == 'circle'){
            style.innerHTML = '.vis-item.' + classcolor + '_circle' + '{ background-color: rgb'+ colors.substring(6,) + '; border-radius: 50%; border-color: black; color: white; }';
            document.getElementsByTagName('head')[0].appendChild(style);
        }else if (shape == 'square'){
            style.innerHTML = '.vis-item.' + classcolor + '_square' + '{ background-color: rgb'+ colors.substring(6,) + '; border-color: black; color: white; }';
            document.getElementsByTagName('head')[0].appendChild(style);
        }else if (shape == 'oval'){
            style.innerHTML = '.vis-item.' + classcolor + '_oval' + '{ background-color: rgb'+ colors.substring(6,) + '; border-color: black; color: rgb'+ colors.substring(6,) + '; }';
            document.getElementsByTagName('head')[0].appendChild(style);
        }
    }

    function homeFunction() {
        document.getElementById("btnHome").style.color = "black";
    }

});
