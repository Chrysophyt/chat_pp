var i = 0
function counter(){
    console.log(i++)
    setTimeout(counter, 1000)
}

function changeStatus(string){
    document.getElementById("status").innerHTML = string
}

function readCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}

function createChat(name, message){
    var card = document.createElement('div')
    card.className = 'card'

    var card_name = document.createElement('div')
    var card_message = document.createElement('div')

    card_name.className = 'name'
    card_message.className = 'message'

    card_name.innerHTML = name
    card_message.innerHTML = message

    card.appendChild(card_name)
    card.appendChild(card_message)

    document.getElementsByClassName("card-row")[0].appendChild(card)

    var objDiv = document.getElementsByClassName('card-row')[0]
    objDiv.scrollTop = objDiv.scrollHeight;
}

function constructRequest(){

    // username = document.getElementById('username').value
    var jwtPayload = JSON.parse(window.atob(readCookie('access-token').split('.')[1]))


    var username_data = {'username': jwtPayload['username']}

    var message_data ={}
    var message = $(document.getElementById('text_field')).serializeArray()

    $.map(message, (n, i)=>{
        message_data[n['name']] = n['value']
    })


    data = Object.assign(username_data, message_data)

    if (!/\S/.test(message_data['message'])){
        console.log("Only empty space, not sending data!")
        document.getElementById('text_field').reset()
        return
    }
    console.log(data)

    $.ajax({
        type: 'POST',
        url: "api/send_message",
        data: JSON.stringify(data),
        contentType: "application/json",
        success: (d)=>{
            console.log(d)
            changeStatus("Connected")
            document.getElementById('text_field').reset()
        },
        error: changeStatus("Sorry, Connection Problem")
    });
    //NGINX reverse proxy
    // location / {
    //     root   html;
    //     index  index.html index.htm;
    // }

    // location /api/ {
    //     proxy_pass http://localhost:5000; //alamat flask api
    // }
}

var interval = 1000
var current_status = 0
var current_message_shown = 0
function getStatusRequest(){
    $.ajax({
        type: 'GET',
        url: 'api/get_status',
        success: function (data) {
            if(current_status==0){
                getMessageRequest(10, data['status'])
                return
            }
            if(data['status']> current_status){
                console.log(data['status']-current_status)
                getMessageRequest(data['status']-current_status, data['status'])
            }
        },
        complete: function (data) {
                // Schedule the next
                //current_status = data['status']
                setTimeout(getStatusRequest, interval);
        }
    });
}

function getMessageRequest(messageAmount, status){

    $.ajax({
        type: 'GET',
        url: 'api/get_message',
        data: { 
            amount: messageAmount
        },
        success: function (data) {
                var messages = data.reverse()
                for(x in messages){
                    //console.log(messages[x])
                    createChat(messages[x][1], messages[x][2])
                }
        },
        complete: function (data){
            current_status = status
            //console.log(current_status)
            
            // current_message_shown += messageAmount
            // console.log(current_message_shown)

        }
    });
}

function getAuthentication(){
    $.ajax({
        type: 'GET',
        url: 'api/validate',
        complete: (d)=>{
            if(d.status!=200){
                element = document.getElementsByClassName("chat_box")[0];
                element.parentNode.removeChild(element);
                changeStatus(d.responseJSON['error']+" Please <a href='user/login.html'>Login</a> to Continue Chatting. ")

            }
            var jwtPayload = JSON.parse(window.atob(readCookie('access-token').split('.')[1]))
            var seconds = parseInt(jwtPayload['exp'])*1000
            document.getElementById("info").innerHTML = "You're Logged in as "+jwtPayload['username']+"<br>Session Will Expire on <br>"+ new Date(seconds).toString()
        }
    })
}