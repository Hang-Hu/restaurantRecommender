import React, { Component } from 'react';
import './App.css';
import NavBar from './components/NavBar';
import UserPage from './user/UserPage';
import RecommendPage from './recommend/RecommendPage';


class App extends Component {
  constructor(props){
    super(props);
    this.state = {
      tab: 'user',
      userId: 1
    }
    this.handleNavBarClick = this.handleNavBarClick.bind(this);
    this.changeUserId = this.changeUserId.bind(this);
  }
  handleNavBarClick(event, value){
    this.setState({
        tab: value
    });
  }
  changeUserId(newUserId){
    this.setState({
      userId: newUserId
    });
  }
  render() {
    return (
      <div className="App">
        <NavBar
          handleNavBarClick={this.handleNavBarClick}
          value={ this.state.tab }
          className="NavBar"
        />
        {this.state.tab === 'recommend' && <RecommendPage userId={this.state.userId} />}
        {this.state.tab === 'user' && <UserPage userId={ this.state.userId } changeUserId={ this.changeUserId } />}

      </div>
    );
  }
}

export default App;
