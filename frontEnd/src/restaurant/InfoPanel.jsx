import React, {Component} from 'react';
import Card from '@material-ui/core/Card';
import CardActionArea from '@material-ui/core/CardActionArea';
import CardContent from '@material-ui/core/CardContent';
import Typography from '@material-ui/core/Typography';
import ReactStars from 'react-stars'

export default class InfoPanel extends Component {
    constructor(props) {
        super(props);
    }
    render(){
        return (
            <Card style={{ width: '100%', display: 'inline-block' }}>
                <CardActionArea style={{margin: 'auto'}}>
                    <ReactStars
                        value={ this.props.rating }
                        size={ 40 }
                        edit={ false }
                    />
                    <CardContent>
                        <Typography>
                            Location: { this.props.location.city }
                        </Typography>
                        <Typography>
                            Phone: { this.props.phone }
                        </Typography>
                    </CardContent>
                </CardActionArea >
            </Card>
            );
    }
}