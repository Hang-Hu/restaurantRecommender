import React, {Component} from 'react';
import RestaurantCard from './RestaurantCard'
import handleErrors from '../utils/errors.js'
import Jumbotron from '../components/Jumbotron';
import LoadingBar from './../components/LoadingBar'

export default class RestaurantsCollectionPage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            loading: false,
            businessIdList: []
        };
        this.getRecommendList = this.getRecommendList.bind(this);
    }
    getRecommendList(){
        let url = `http://127.0.0.1:8000/business/recommend/${this.props.userId}/`;
        this.setState({
                loading: true
        }, () => {
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
                    businessIdList: data.business_id_list
                });
            }.bind(this))
            .catch(function(err){
                console.log(err);
                this.setState({
                    loading: false
                });
            }.bind(this));        
        });
        
    }
    componentDidMount(){
        this.getRecommendList();
    }
    componentDidUpdate(prevProps){
        if(prevProps.userId !== this.props.userId){
            this.getRecommendList();
        }
    }
    render(){
        let width = `${100/4}%`;

        return (
            <div>
                {
                    this.state.businessIdList && this.state.businessIdList.map(businessId => (
                        <RestaurantCard
                            key={businessId}
                            businessId={businessId}
                            handleBusinessCardClick={ this.props.handleBusinessCardClick }
                            width={ width }
                        />
                    ))
                }
                {
                    !this.state.loading && this.state.businessIdList.length === 0 && <Jumbotron value='No Recommendations' />
                }
                {
                    this.state.loading && <LoadingBar />
                }
            </div>
        );
    }
}