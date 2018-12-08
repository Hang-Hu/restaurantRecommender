import React, {Component} from 'react';
import LinearProgress from '@material-ui/core/LinearProgress';

export default class LoadingBar extends Component {
    constructor(props) {
        super(props);
    }
    render(){
        return (
            <div style={{flexGrow: '1'}}>
              <LinearProgress />
              <br />
              <LinearProgress color="secondary" />
            </div>
        );
    }
}