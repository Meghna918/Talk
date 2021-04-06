var currentRecipient = '';

function updateuserslist(){
$.getJSON( "http://127.0.0.1:8000/chat/talkapi/user/", function( data ) {
   for (let i = 0; i < data.length; i++) {
   let user=data[i]['username']
  $('#myTable').append("<tr><td>"+user+"<tr/></td>");
}
$("#myInput").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#myTable tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
  $( "td" ).click(function() {
 
    //$("#chat-log").value=''
    setCurrentRecipient($(this).text());

});
});
}


function getmessages(recipient){
$.getJSON("http://127.0.0.1:8000/chat/talkapi/chat/?recipientName="+recipient,function(data,status){
     $('#messages').children('p').remove();
     for (let i = 0; i < data.length; i++){
          messages=data[i]
          displaymessages(messages)

     }

})

}
function setCurrentRecipient(username) {
    currentRecipient = username;

    getmessages(currentRecipient);

}
function displaymessages(message){
    const msg=`${message.user}:${message.content}`

    $("#messages").append("<p>"+msg+"</p>")


}

function sendMessage(recipient, content) {

    $.post('http://127.0.0.1:8000/chat/talkapi/chat/', {
        "recipient": recipient,
        "content": content
     }).fail(function () {
        alert('Error! Check console!');
    });
}
function getMessageById(message) {
    id = JSON.parse(message).message
    console.log(id)
    $.getJSON("http://127.0.0.1:8000/chat/talkapi/chat/"+id+"/", function (data) {
        if (data.user === currentRecipient ||
            (data.recipient === currentRecipient && data.user == currentUser)) {
            displaymessages(data);
        }

    });
}

$(document).ready(function () {
updateuserslist()
var socket = new WebSocket(
        'ws://' + window.location.host +
        '/ws?session_key=${sessionKey}')

$("#chat-message-input").keyup(function (e) {
        if (e.keyCode == 13)
            $("#chat-message-submit").click();
    });

$("#chat-message-submit").click(function () {
        if ($("#chat-message-input").length > 0) {
           sendMessage(currentRecipient, $("#chat-message-input").val());
            $("#chat-message-input").val('');
        }
    });
socket.onmessage = function (e) {
        getMessageById(e.data);
    };
 socket.onclose = function(e) {
            console.error('Chat socket closed unexpectedly');
        };
})