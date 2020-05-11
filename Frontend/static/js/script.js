let prompt_id = "initial";
const url = window.location.origin + `/resources/${experiment}/${bot_type}/${topic}/`;

const button = document.getElementById("send");
var body = document.body; // Safari
var html = document.documentElement; // Chrome, Firefox, IE and Opera places the overflow at the <html> level, unless else is specified. Therefore, we use the documentElement property for these browsers
 
body.scrollTop += body.scrollHeight;
html.scrollTop += html.scrollHeight;
function thinking(){
    document.getElementById("textMessage").value ="";
    document.getElementById("textMessage").setAttribute("disabled", "disabled");
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
    let chatWindow = document.getElementById("chatwindow");
    chatWindow.appendChild(container);
    chatWindow.scrollTop = chatWindow.scrollHeight;

    
}

function insertChoices(choices){
    const choice_container = document.createElement("div");
        choice_container.id = "choice_container"
        
        choices.forEach(element => {
        
        const button = document.createElement("button");
        button.classList.add("option");
        button.textContent = element;
        button.addEventListener("click",()=>{
            insert_user(element);
            sendMessage(element);
        })
        choice_container.appendChild(button) 
            
        });

        document.getElementById("interface").prepend(choice_container)


}

function sendMessage(message){

    const body= {
        user_id: user_id,
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
    let choice_cont = document.getElementById("choice_container");
    if(choice_cont){
        choice_cont.remove();
    }
    

    thinking();
    setTimeout(() => {
        fetch(url+prompt_id, option)
        .then(response => response.json())
        .then(json =>{
            document.getElementById("thought_container").remove();
            insert_bot(json);

        });

    }, 3000);
}


function insert_user(message){
    const container = document.createElement("div");
    container.classList.add(`user_container`);
    const displayMessage = document.createTextNode(message);
    const message_user = document.createElement("div");
    message_user.classList.add(`message_user`);
    message_user.appendChild(displayMessage);
    container.appendChild(message_user);
    let chatWindow = document.getElementById("chatwindow");
    chatWindow.appendChild(container);
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
        insertChoices(message.choice);

        let chatWindow = document.getElementById("chatwindow");
        chatWindow.appendChild(container);
        chatWindow.scrollTop = chatWindow.scrollHeight;
        
        document.getElementById("textMessage").removeAttribute("disabled");
        document.getElementById("textMessage").select();
        

    }

    else if(message.type === "followup"){


        const container = document.createElement("div");
        container.classList.add(`bot_container`);
        const displayMessage = document.createTextNode(message.prompt);
        const message_bot = document.createElement("div");
        message_bot.classList.add(`message_bot`);
        message_bot.appendChild(displayMessage);
        container.appendChild(message_bot);
        let chatWindow = document.getElementById("chatwindow");
        chatWindow.appendChild(container);
        chatWindow.scrollTop = chatWindow.scrollHeight;
        
        document.getElementById("textMessage").removeAttribute("disabled");
        document.getElementById("textMessage").select();
        sendMessage("");



    }
    //just normal conversation
    else{

        const container = document.createElement("div");
        container.classList.add(`bot_container`);
        const displayMessage = document.createTextNode(message.prompt);
        const message_bot = document.createElement("div");
        message_bot.classList.add(`message_bot`);
        message_bot.appendChild(displayMessage);
        if("url" in message){
            const link = message.url;
            let anch = document.createElement("a");
            const url_text = document.createTextNode(message.url_text);
            anch.appendChild (url_text);
            anch.href = link;
            message_bot.appendChild(anch);
        }
        
        container.appendChild(message_bot);
        let chatWindow = document.getElementById("chatwindow");
        chatWindow.appendChild(container);
        chatWindow.scrollTop = chatWindow.scrollHeight;
        
        document.getElementById("textMessage").removeAttribute("disabled");
        document.getElementById("textMessage").select();

    }

}//end function


//Get initial message from the server
thinking()
setTimeout(()=>{
    fetch(url+prompt_id)
    .then(res =>res.json())
    .then(res => {
        document.getElementById("thought_container").remove();
        insert_bot(res);
        prompt_id = prompt_id;
    });

}, 3000);

// send on press of the button




button.addEventListener("click",()=>{

    const message = document.getElementById("textMessage").value;
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
        const message = document.getElementById("textMessage").value;
        insert_user( message);
        sendMessage(message);
    }
}
