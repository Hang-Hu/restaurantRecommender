import React, {Component} from 'react';
import Jumbotron from './../components/Jumbotron';
import SimpleModal from './../components/SimpleModal';
import handleErrors from './../utils/errors.js'

export default class UserPage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            modalOpen: false,
            loading: false,
            minUserId: NaN,
            maxUserId: NaN

        };
        this.handleButtonClick = this.handleButtonClick.bind(this);
        this.closeModal = this.closeModal.bind(this);
        this.getAvailableUserIdList = this.getAvailableUserIdList.bind(this);

    }
    componentDidMount(){
        this.getAvailableUserIdList();
    }
    getAvailableUserIdList(){
        let url = 'http://localhost:8000/business/user_id_list/';
        fetch(url, {
            method: 'GET',
            headers: {
            }
        })
        .then(handleErrors)
        .then(function(response){
            return response.json();
        })
        .then(function(data){
            this.setState({
                loading: false,
                minUserId: data.user_id_list[0],
                maxUserId: data.user_id_list[1]
            });
        }.bind(this))
        .catch(function(err){
            console.log(err);
            this.setState({
                loading: false
            });
        }.bind(this));

    }
    handleButtonClick(){
        this.setState({
            modalOpen: true
        });
    }
    closeModal(){
        this.setState({
            modalOpen: false
        });
    }
    render(){
        return (
            <div>
                <Jumbotron value={ 'User ID: '+this.props.userId } />
                <a
                    className="btn btn-primary btn-lg"
                    role="button"
                    onClick={ this.handleButtonClick }
                >
                    Change User ID
                </a>
                <SimpleModal
                    open={ this.state.modalOpen }
                    handleModalClose={ this.closeModal }
                    userId={ this.props.userId }
                    minUserId={ this.state.minUserId }
                    maxUserId={ this.state.maxUserId }
                    changeUserId={ this.props.changeUserId }
                />
            </div>
        );
    }
}