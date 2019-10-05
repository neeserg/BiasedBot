import React, { Component } from 'react'

export class Message extends Component {
    render() {
        return (
            <div>
                <p> {this.props.message.who} : {this.props.message.message}</p>
            </div>
        )
    }
}

export default Message
