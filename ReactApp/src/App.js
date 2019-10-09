import React, { Component } from 'react'
import Chat from './components/Chat'
import Send from './components/Send'
import './App.css';

class App extends Component{

  state = {
    send: true,
    username: "Neeserg",
    userId: window.userId,
    nextTurn: "bot",
    messages : [
    ]
  }

  go_to_End = ()=>{
    let domain = "http://" + window.location.host +"/end/" +this.state.userId
    window.location.assign(domain)
  }

  get_latest = ()=>{
    if (this.state.messages.length ==0){
      return "hi"
    }
    else{
      let len = this.state.messages.length -1
      return this.state.messages[len].message

    }
  }



  addMessage = (message) =>{
    let thisTurn = this.state.nextTurn;
    if (this.state.nextTurn === 'user'){
      this.setState({
        nextTurn : 'bot'
      })
    }
    else{
      if (message === "End Of Conversation"){
        this.go_to_End()
      }
      this.setState({
        nextTurn : 'user'
      })
    }
    this.setState({
      messages : [...this.state.messages, {message: message, who: thisTurn}]
    });

    console.log(this.state)
  }





  render() { 
    if (this.state.nextTurn === 'bot'){
    fetch(window.location.href,{
      method: 'POST',
      headers:{
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      userId: this.state.userId,
      message: this.get_latest()
    })
    })
    .then(response => response.json())
    .then(json => this.addMessage(json.message));
    return (
      <div><Chat key={this.state.userId} messages={this.state.messages} /></div>
    
  );
}
else{
  return (
    <div><Chat key={this.state.userId} messages={this.state.messages} />
    <Send addMessage = {this.addMessage}/></div>
  
);
}
    
  }
}

export default App;
