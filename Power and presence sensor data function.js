var newData = msg.payload;
if (newData.charAt(0) == "A"){
    data1 = newData.substr(1, newData.length-1);
} else if (newData.charAt(0) == "B"){
    data2 = newData.substr(1, newData.length-1);
} else if (newData.charAt(0) == "C"){
    data3 = newData.substr(1, newData.length-1);
}
if (data3 == "TRUE"){
    send = 1;
} else{
    send = 0;
}
var power = (parseFloat(data1)+parseFloat(data2)).toString();

var data = [data1,send];
msg.payload = "";
for (var i = 0; i < data.length; i++) {
  msg.payload = msg.payload+"field"+(i+1).toString()+"="+data[i]+"&";
}
msg.payload = msg.payload + "status=MQTTPUBLISH";
// Return the message so it can be sent on
return msg;