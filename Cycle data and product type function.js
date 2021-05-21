var data = msg.payload;
for (var j = 0; j < data.length; j++) {
  if (data.charAt(j) == '-'){
      char = j;
  }
} 

productPre = data.substr(char+1, data.length-1);
cyclePre = data.substr(2, char-2);
var noMin = 1;
for (var m = 0; m < cyclePre.length; m++) {
  if (cyclePre.charAt(m) == 'm'){
      var min = m;
      noMin = 0;
  }
}
if (noMin == 0){
    cycle = (parseInt(cyclePre.substr(0,min))*60 + parseInt(cyclePre.substr(min+1,cyclePre.length-3))).toString();
} else{
    cycle = (cyclePre.substr(0,cyclePre.length-1));
}

if (productPre == "MB16"){
    product = 1;
} else if (productPre == "MB16T"){
    product = 2;
} else if (productPre == "MB20"){
    product = 3;
} else if (productPre == "MB24"){
    product = 4;
}

var send = [product, cycle];
msg.payload = "";
for (var i = 0; i < send.length; i++) {
  msg.payload = msg.payload+"field"+(i+1).toString()+"="+send[i]+"&";
}
msg.payload = msg.payload + "status=MQTTPUBLISH";
// Return the message so it can be sent on
return msg;