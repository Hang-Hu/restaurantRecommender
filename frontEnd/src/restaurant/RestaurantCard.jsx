import React, {Component} from 'react';
import handleErrors from '../utils/errors.js'
import Card from '@material-ui/core/Card';
import CardActionArea from '@material-ui/core/CardActionArea';
import CardContent from '@material-ui/core/CardContent';
import Typography from '@material-ui/core/Typography';
import CategoryLine from '../recommend/CategoryLine';  
import './RestaurantCard.css';
import ReactStars from 'react-stars'
import generateColor from './../utils/colors';


export default class RestaurantCard extends Component {
    constructor(props) {
        super(props);
        this.state = {
            loading: false,
            name: '',
            city: '',
            stars: NaN,
            review_count: '',
            categories: '',
            businessId: ''
        };
        this.getBusinessInfo = this.getBusinessInfo.bind(this);
    }
    getBusinessInfo(){
        let url = `http://127.0.0.1:8000/business/business_info/${this.props.businessId}/`;
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
            // console.log(data);
            let business = data.business_info;
            this.setState({
                loading: false,
                name: business.name,
                city: business.city,
                stars: +business.stars,
                review_count: business.review_count,
                categories: business.categories,
            });
        }.bind(this))
        .catch(function(err){
            console.log(err);
            this.setState({
                loading: false
            });
        }.bind(this));

    }
    componentDidMount(){
        this.getBusinessInfo();
    }
    componentDidUpdate(prevProps){
        if(prevProps.businessId !== this.props.businessId){
            this.getBusinessInfo();
        }
    }
    render(){
        return (
            <Card
                style={{ width: this.props.width, display: 'inline-block', backgroundColor: generateColor() }}
                onClick={ () => this.props.handleBusinessCardClick(this.props.businessId) }
                className='RestaurantCard'
            >
                <CardActionArea style={{margin: 'auto'}}>
                    <CardContent>
                        <Typography>
                            { this.state.name }
                        </Typography>
                        <ReactStars
                            value={ this.state.stars }
                            size={ 20 }
                            edit={ false }
                        />
                        <CategoryLine value={ this.state.categories } />
                    </CardContent>
                </CardActionArea >
            </Card>
        );
    }
}