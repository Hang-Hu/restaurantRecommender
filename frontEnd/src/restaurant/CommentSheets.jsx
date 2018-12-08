import React, {Component} from 'react';
import CommentPaper from './CommentPaper';

export default class CommentSheets extends Component {
    constructor(props) {
        super(props);
    }
    render(){
        return (
            <div>
                {
                    this.props.comments.length > 0 &&
                    <div className="row" style={{ margin: '10px 0 0 10px' }}>
                        <div className="col-sm-12">
                            <h3 style={{ color: '#3F51B5' }}>Tips</h3>
                        </div>
                    </div>
                }
                
                {
                    this.props.comments && this.props.comments.map((comment, index) => (
                        <CommentPaper
                            key={ index }
                            date={ comment.date }
                            text={ comment.text }
                            userId={ comment.user_id }
                        />
                    ))
                }
            </div>
        );
    }
}