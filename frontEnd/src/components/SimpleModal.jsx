import React, {Component} from 'react';
import Modal from '@material-ui/core/Modal';
import ChangeUserIdPanel from './../user/ChangeUserIdPanel';

export default class SimpleModal extends Component {
    constructor(props) {
        super(props);
    }
    render(){
        return (
            <Modal
                aria-labelledby="simple-modal-title"
                aria-describedby="simple-modal-description"
                open={this.props.open}
                onClose={this.props.handleModalClose}
            >
                <div style={{ position: 'absolute', top: '50%', left: '50%', backgroundColor: 'white', transform: 'translate(-50%, -50%)' }}>
                    <ChangeUserIdPanel
                        userId={ this.props.userId }
                        minUserId={ this.props.minUserId }
                        maxUserId={ this.props.maxUserId }
                        changeUserId={ this.props.changeUserId }
                        handleModalClose={ this.props.handleModalClose }
                    />
                </div>
            </Modal>
        );
    }
}