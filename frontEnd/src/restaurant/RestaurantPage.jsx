import React, {Component} from 'react';
import handleErrors from './../utils/errors.js'
import ImageGallery from './../components/ImageGallery';
import Jumbotron from './../components/Jumbotron';
import InfoPanel from './InfoPanel';
import CommentSheets from './CommentSheets';
export default class RestaurantPage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            businessLoading: false,
            commentsLoading: false,
            name: '',
            imageUrls: '',
            url: '',
            phone: '',
            rating: NaN,
            location: '',
            comments: []
        };
        this.getBusinessDetailedInfo = this.getBusinessDetailedInfo.bind(this);
        this.getComments = this.getComments.bind(this);
    }
    getBusinessDetailedInfo(){
        let url = `http://127.0.0.1:8000/business/business_detailed_info/${this.props.businessId}/`;
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
            let info = data.business_info;
            this.setState({
                businessLoading: false,
                name: info.name,
                imageUrls: info.photos,
                url: info.url,
                phone: info.display_phone,
                rating: info.rating,
                location: info.location
            });
        }.bind(this))
        .catch(function(err){
            console.log(err);
            this.setState({
                businessLoading: false
            });
        }.bind(this));

    }
    getComments(){
        let url = `http://127.0.0.1:8000/business/tips/${this.props.businessId}/`;
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
                commentsLoading: false,
                comments: data.tips
            });
        }.bind(this))
        .catch(function(err){
            console.log(err);
            this.setState({
                commentsLoading: false
            });
        }.bind(this));

    }
    componentDidMount(){
        this.getBusinessDetailedInfo();
        this.getComments();
    }
    componentDidUpdate(prevProps){
        if(prevProps.businessId !== this.props.businessId){
            this.getBusinessDetailedInfo();
            this.getComments();
        }
    }
    render(){
        return (
            <div>
                <ImageGallery
                    imageUrls={ this.state.imageUrls }
                />
                <Jumbotron value={ this.state.name } />
                <InfoPanel
                    phone={ this.state.phone }
                    rating={ this.state.rating }
                    location={ this.state.location }
                />
                <CommentSheets
                    comments={ this.state.comments }
                />
            </div>
        );
    }
}