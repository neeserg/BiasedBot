const url = window.location.href;
let prompt_id = "climate_initial"


const button = document.getElementById("send");

function thinking(){
    document.getElementById("exampleFormControlTextarea1").value ="";
    document.getElementById("exampleFormControlTextarea1").setAttribute("disabled", "disabled");
    const container = document.createElement("div");
    container.classList.add(`bot_container`);
    container.setAttribute("id", "thought_container")
    const message_bot = document.createElement("div");
    message_bot.classList.add(`message_bot`);
    const thought = document.createElement("p");
    thought.setAttribute("id", "thinking");
    thought.textContent = "oooo";
    message_bot.appendChild(thought);
    container.appendChild(message_bot);
    document.getElementById("chatwindow").appendChild(container);
    let chatWindow = document.getElementById("chatwindow");
    chatWindow.scrollTop = chatWindow.scrollHeight;
    container.focus()

}


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

    thinking();
    setTimeout(() => {
        fetch(url+'/resources/'+prompt_id, option)
        .then(response => response.json())
        .then(json =>{
            document.getElementById("thought_container").remove();
            insert_bot(json);

        });

    }, 5000);
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
    document.getElementById("exampleFormControlTextarea1").removeAttribute("disabled");
    document.getElementById("exampleFormControlTextarea1").select();
}


//Get initial message from the server
thinking()
setTimeout(()=>{
    fetch(url+'/resources/'+prompt_id)
    .then(res =>res.json())
    .then(res => {
        document.getElementById("thought_container").remove();
        insert_bot(res);
        prompt_id = prompt_id;
    });

}, 5000);

// send on press of the button




button.addEventListener("click",()=>{

    const message = document.getElementById("exampleFormControlTextarea1").value;
    if(message == null || message === ""){
        return;
    }
    insert_user( message);
    sendMessage(message);
});

// send on press of enter
function sendOnEnter(event){
    var key = event.keyCode;
    if(key === 13){
        const message = document.getElementById("exampleFormControlTextarea1").value;
        insert_user( message);
        sendMessage(message);
    }
}