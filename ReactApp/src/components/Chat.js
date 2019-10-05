import React, { Component } from 'react'
import Message from './Message'

export class Chat extends Component {
    render() {
        return this.props.messages.map( (message) => (
                <Message key={message.message} message={message}/>
                ));
        
    }
}

export default Chat
