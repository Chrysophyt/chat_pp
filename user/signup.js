function changeStatus(message){
    document.getElementById("error_msg").innerHTML = message
}
function serializeFormToJSON(){
    var form_data ={}            
    var arr = $(document.getElementById("signup")).serializeArray()

    $.map(arr, (n, i)=>{
        form_data[n['name']] = n['value']
    })
    return form_data // {id: "id yang diketik", password: "password yang ada"} agar mudah jadi JSON dan di send ke REST API
}

function validate(data){
    usernameRegex = /^[a-z_-]{3,15}$/   
    validation = true
    data['username'] = data['username'].toLowerCase()   //tidak case sensitive

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

function requestSignUp(){
    data = serializeFormToJSON()
    console.log(data)

    if(validate(data)){
        $.ajax({
            type: 'POST',
            url: "../api/create_account",
            data: JSON.stringify(data),
            contentType: "application/json",
            success: (d, XmlHttpRequest)=>{
                alert('Registered Completed Redirecting you to the login page.')
                
                var start = new Date().getTime();
                var end = start;
                while(end < start + 1000) {
                    end = new Date().getTime();
                }

                window.location = 'login.html'
            },
            error: (d)=>{
                changeStatus(d.responseJSON['status'])
            }
        });
    }
    
}