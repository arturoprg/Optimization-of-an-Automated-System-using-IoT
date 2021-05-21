var newData = msg.payload;
if (newData.charAt(0) == "A"){
    data1 = newData.substr(1, newData.length-1);
} else if (newData.charAt(0) == "B"){
    data2 = newData.substr(1, newData.length-1);
} else if (newData.charAt(0) == "C"){
    data3 = newData.substr(1, newData.length-1);
} else if (newData.charAt(0) == "D"){
    data4 = newData.substr(1, newData.length-1);
} else if (newData.charAt(0) == "E"){
    data5 = newData.substr(1, newData.length-1);
} else if (newData.charAt(0) == "F"){
    data6 = newData.substr(1, newData.length-1);
} else if (newData.charAt(0) == "G"){
    data7 = newData.substr(1, newData.length-1);
} else if (newData.charAt(0) == "H"){
    data8 = newData.substr(1, newData.length-1);
}
var data = [data1,data2,data3,data4,data5,data6,data7,data8];
msg.payload = "";
for (var i = 0; i < data.length; i++) {
  msg.payload = msg.payload+"field"+(i+1).toString()+"="+data[i]+"&";
}
msg.payload = msg.payload + "status=MQTTPUBLISH";
// Return the message so it can be sent on
return msg;