var i = 0
function counter(){
    console.log(i++)
    //setTimeout(counter, 1000)
}

function changeStatus(string){
    document.getElementById("status").innerHTML = string
}

function constructRequest(){

    var message_data ={}

    var message = $(document.getElementById('text_field')).serializeArray()

    $.map(message, (n, i)=>{
        message_data[n['name']] = n['value']
    })

    var sendMessage = $.ajax({
        type: 'POST',
        url: "api/send_message",
        data: JSON.stringify(message_data),
        contentType: "application/json",
        success: (d)=>{
            console.log(d)
            changeStatus("Connected")
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