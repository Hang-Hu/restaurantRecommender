import React, {Component} from 'react';

export default class Jumbotron extends Component {
    constructor(props) {
        super(props);
    }
    render(){
        return (
            <div className="jumbotron">
                <h1 className="display-4">{ this.props.value }</h1>
            </div>
        );
    }
}