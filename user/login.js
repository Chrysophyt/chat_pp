function changeStatus(message){
    document.getElementById("error_msg").innerHTML = message
}
function serializeFormToJSON(){
    var form_data ={}            
    var arr = $(document.getElementById("login")).serializeArray()

    $.map(arr, (n, i)=>{
        form_data[n['name']] = n['value']
    })
    return form_data // {id: "id yang diketik", password: "password yang ada"} agar mudah jadi JSON dan di send ke REST API
}

function validate(data){
    usernameRegex = /^[a-z_-]{3,15}$/   
    validation = true
    data['username'] = data['username'].toString().toLowerCase()   //tidak case sensitive

    if(usernameRegex.test(data['username'])){
        console.log("user name detected")
    }else{
        validation = false
        console.log("sorry error")
    }

    if(validation){
        changeStatus("")
    }else{
        changeStatus("Sorry, Your input data is not valid.")
    }
    return validation
}

function requestlogin(){
    data = serializeFormToJSON()
    console.log(data)

    if(validate(data)){
        $.ajax({
            type: 'POST',
            url: "../api/login",
            data: JSON.stringify(data),
            contentType: "application/json",
            success: (d)=>{
                alert('Login Successful.')
                
                var start = new Date().getTime();
                var end = start;
                while(end < start + 1000) {
                    end = new Date().getTime();
                }

                window.location = '../'
            },
            error: (d)=>{
                console.log(d)
                changeStatus(d.responseJSON['error'])
            }
        });
    }
    
}