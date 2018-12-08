import React, {Component} from 'react';
import ImageCard from './ImageCard';

export default class ImageGallery extends Component {
    constructor(props) {
        super(props);
        this.state = {

        };
    }

    render(){
        let width = `${100/this.props.imageUrls.length}%`;
        return (
            <div>
                {
                    this.props.imageUrls && this.props.imageUrls.map((url, index) => (
                        <ImageCard
                            key={ index }
                            url={ url }
                            width={ width }
                        />
                    ))
                }
            </div>
        );
    }
}