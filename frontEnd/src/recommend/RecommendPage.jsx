import React, {Component} from 'react';
import RestaurantsCollectionPage from './../restaurant/RestaurantsCollectionPage';
import RestaurantPage from './../restaurant/RestaurantPage';

export default class RecommendPage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            selected: 'collection',
            selectedBusinessId: ''
        };
        this.handleBusinessCardClick = this.handleBusinessCardClick.bind(this);
    }
    handleBusinessCardClick(businessId){
        this.setState({
            selected: 'one',
            selectedBusinessId: businessId
        });
    }
    render(){
        return (
            <div>
                { 
                    this.state.selected === 'collection' &&
                    <RestaurantsCollectionPage
                        handleBusinessCardClick={ this.handleBusinessCardClick }
                        userId={ this.props.userId }
                    />
                    }
                { this.state.selected === 'one' && <RestaurantPage businessId={ this.state.selectedBusinessId } />}
            </div>
        );
    }
}