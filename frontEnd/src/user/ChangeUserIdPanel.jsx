import React, {Component} from 'react';
import Typography from '@material-ui/core/Typography';
import TextField from '@material-ui/core/TextField';

export default class ChangeUserIdPanel extends Component {
    constructor(props) {
        super(props);
        this.state = {
            newUserId: this.props.userId
        };
        this.handleUserIdInputChange = this.handleUserIdInputChange.bind(this);
        this.handleSubmitClick = this.handleSubmitClick.bind(this);
    }
    handleUserIdInputChange(e){
        this.setState({
            newUserId: e.currentTarget.value
        });
    }
    handleSubmitClick(){
        if(this.state.newUserId && this.state.newUserId !== this.props.userId){
            this.props.changeUserId(this.state.newUserId);
        }
        this.props.handleModalClose();
    }
    render(){
        return (
            <div>
                <Typography>
                    New User Id:
                </Typography>
                 <TextField
                    label="Number"
                    value={this.state.newUserId}
                    onChange={this.handleUserIdInputChange}
                    type="number"
                    InputLabelProps={{
                        shrink: true,
                    }}
                    margin="normal"
                />
                <div style={{ textAlign: 'center'}}>
                    <a
                        className="btn btn-primary"
                        onClick={ this.props.handleModalClose }
                    >Cancel</a>
                    <a
                        className="btn btn-primary"
                        onClick={ this.handleSubmitClick }
                    >Submit</a>
                </div>
            </div>
        );
    }
}