import React, {Component} from 'react';
import AppBar from '@material-ui/core/AppBar';
import Tabs from '@material-ui/core/Tabs';
import NoSsr from '@material-ui/core/NoSsr';
import Tab from '@material-ui/core/Tab';


function LinkTab(props) {
    return <Tab component="a" onClick={event => event.preventDefault()} {...props} />;
}

  
export default class NavBar extends Component {
    constructor(props) {
        super(props);
    }
    render(){
        return (
        <NoSsr>
            <div className={ this.props.className }>
              <AppBar position="static">
                <Tabs fullWidth value={ this.props.value } onChange={this.props.handleNavBarClick}>
                  <LinkTab label="Recommend" href="recommend" value='recommend' />
                  {/* <LinkTab label="Page Two" href="page2" value='2' /> */}
                  <LinkTab label="User" href="page3" value='user' />
                </Tabs>
              </AppBar>
            </div>
        </NoSsr>
        );
    }
}