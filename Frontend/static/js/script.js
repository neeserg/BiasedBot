const url = window.location.href;
let prompt_id = "climate_initial"


const button = document.getElementById("send");




function sendMessage(message){

    const body= {
        userId: userId,
        message: message,
        prompt_id: prompt_id
    }
    
    const option = {
        method: "POST",
        body: JSON.stringify(body),
        headers: {
            'Content-Type': 'application/json'
        }
    }
    fetch(url+'resources/'+prompt_id, option)
        .then(response => response.json())
        .then(json =>{
            insert_bot(json);
        });
}


function insert_user(message){
    const container = document.createElement("div");
    container.classList.add(`user_container`);
    const displayMessage = document.createTextNode(message);
    const message_user = document.createElement("div");
    message_user.classList.add(`message_user`);
    message_user.appendChild(displayMessage);
    container.appendChild(message_user);
    document.getElementById("chatwindow").appendChild(container);
    let chatWindow = document.getElementById("chatwindow");
    chatWindow.scrollTop = chatWindow.scrollHeight;
}




function insert_bot(message){
    document.getElementById("exampleFormControlTextarea1").value ="";
    prompt_id = message.prompt_id;
    if(message.type === "choice"){
        const container = document.createElement("div");
        container.classList.add(`bot_container`);
        const displayMessage = document.createTextNode(message.prompt);
        const message_bot = document.createElement("div");
        message_bot.classList.add(`message_bot`);
        message_bot.appendChild(displayMessage);
        container.appendChild(message_bot);

        
        // Now display the choices shown to user and attach buttons to it
        const choice_container = document.createElement("div");
        choice_container.classList.add('choice_container');
        


        message.choice.forEach(element => {
        
        const button = document.createElement("button");
        button.textContent = element
        button.addEventListener("click",()=>{
            insert_user(element);
            sendMessage(element)
        })
        choice_container.appendChild(button)
        container.appendChild(choice_container); 
            
        });

        document.getElementById("chatwindow").appendChild(container);

    }
    //just normal conversation
    else{

    const container = document.createElement("div");
    container.classList.add(`bot_container`);
    const displayMessage = document.createTextNode(message.prompt);
    const message_bot = document.createElement("div");
    message_bot.classList.add(`message_bot`);
    message_bot.appendChild(displayMessage);
    container.appendChild(message_bot);
    document.getElementById("chatwindow").appendChild(container);

    }

    let chatWindow = document.getElementById("chatwindow");
    chatWindow.scrollTop = chatWindow.scrollHeight;
}


//Get initial message from the server
fetch(url+'resources/'+prompt_id)
    .then(res =>res.json())
    .then(res => {
        insert_bot(res)
        prompt_id = prompt_id
    });

button.addEventListener("click",()=>{

    const message = document.getElementById("exampleFormControlTextarea1").value;
    if(message == null || message === ""){
        return;
    }
    insert_user( message);
    sendMessage(message);
});


function sendOnEnter(event){
    var key = event.keyCode;
    if(key === 13){
        const message = document.getElementById("exampleFormControlTextarea1").value;
        insert_user( message);
        sendMessage(message);
    }
}