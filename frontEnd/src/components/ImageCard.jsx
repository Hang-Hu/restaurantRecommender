import React, {Component} from 'react';
import Card from '@material-ui/core/Card';
import CardActionArea from '@material-ui/core/CardActionArea';

export default class ImageCard extends Component{
    constructor(props){
        super(props);

    }
    render(){
        return (
            <Card style={{ width: this.props.width, display: 'inline-block' }}>
                <CardActionArea style={{margin: 'auto'}}>
                    <img
                        src={ this.props.url }
                        width='100%'
                        height='250'
                        alt=''
                    />
                </CardActionArea >
            </Card>
        );
    }
}