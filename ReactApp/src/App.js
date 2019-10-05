import React, { Component } from 'react'
import Chat from './components/Chat'
import Send from './components/Send'
import './App.css';
import uuid from 'uuid';

class App extends Component{

  state = {
    send: true,
    username: "Neeserg",
    userId: uuid.v4(),
    nextTurn: "bot",
    messages : [
    ]
  }

  addMessage = (message) =>{
    let thisTurn = this.state.nextTurn;
    if (this.state.nextTurn === 'user'){
      this.setState({
        nextTurn : 'bot'
      })
    }
    else{
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
    fetch('https://jsonplaceholder.typicode.com/todos/1')
    .then(response => response.json())
    .then(json => setTimeout(() => this.addMessage(json.title), 5000) );
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
