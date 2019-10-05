import React, { Component } from 'react'

export class Send extends Component {
    state = {
        prompt : ''
    }

    onSubmit = (e) => {
        e.preventDefault();
        this.props.addMessage(this.state.prompt)
        this.setState({prompt: ''})
    }

    onChange = (e) => this.setState({ prompt: e.target.value });


    render() {
        return (
            <div>
                <form onSubmit={this.onSubmit}>
                    <input type ="text" 
                           name = "prompt"
                           value = {this.state.prompt}
                           onChange = {this.onChange}/>
                    <input 
                    type="submit" 
                    value="Submit" 
                    className="btn"/>
                </form>                
            </div>
        )
    }
}

export default Send
