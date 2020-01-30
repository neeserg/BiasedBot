const url = window.location.href;
let LatestMessage = "hi"


const button = document.getElementById("send");




function sendMessage(message){
    LatestMessage = message;
    const body= {
        userId: userId,
        message: LatestMessage
    }
    
    const option = {
        method: "POST",
        body: JSON.stringify(body),
        headers: {
            'Content-Type': 'application/json'
        }
    }
    fetch(url, option)
        .then(response => response.json())
        .then(json =>{
            insert_message("bot", json.message);
        });
}


function insert_message(user, message){
    const container = document.createElement("div");
    container.classList.add(`${user}_container`);
    const displayMessage = document.createTextNode(message);
    const message_user = document.createElement("div");
    message_user.classList.add(`message_${user}`);
    message_user.appendChild(displayMessage);
    container.appendChild(message_user);
    document.getElementById("chatWindow").appendChild(container);
}






sendMessage(LatestMessage);

button.addEventListener("click",()=>{

    const message = document.getElementById("exampleFormControlTextarea1").value;
    if(message == null || message === ""){
        return;
    }
    insert_message("user", message);
    sendMessage(message);
});


