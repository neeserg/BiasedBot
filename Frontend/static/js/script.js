const button = document.getElementById("send");


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

button.addEventListener("click",()=>{

    const message = document.getElementById("exampleFormControlTextarea1").value;
    insert_message("user", message);
    fetch('https://jsonplaceholder.typicode.com/todos/1')
        .then(response => response.json())
        .then(json =>{
            insert_message("bot", json.title);
        });
});


