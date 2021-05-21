var date = msg.payload;
msg.payload = "A"+date;
// Return the message so it can be sent on
return msg;