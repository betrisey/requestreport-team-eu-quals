import React, { Component } from "react";
import { RequestInfo } from "./request-info";

export class RequestsPage extends Component {
  constructor(props) {
    super(props);
    this.state = { ...props };
  }

  render() {
    return (
      <div className="card card-w-title card-body">
        {this.props.user !== null && this.props.user !== undefined && this.props.user.requests[this.props.user.selectedRequest] === undefined && (
          <div className="grid">
            <div className="col-12">
              <h1>Awaiting requests</h1>
              <p>How to make a request:</p>
              <code>curl {this.props.user.url}</code>
              <br />
              <br />
              <code>curl -X POST --data hello {this.props.user.url}</code>
              <br />
              <br />
              <code>echo RCE | curl -d @- {this.props.user.url}</code>
              <br />
              <br />
              <code>wget --post-data "$(echo RCE)" -O- {this.props.user.url}</code>
              <br />
              <br />
              <p>Check out the Response tab to edit your HTTP Response.</p>
            </div>
          </div>
        )}
        {this.props.user !== null && this.props.user !== undefined && this.props.user.requests[this.props.user.selectedRequest] !== undefined && (
          <RequestInfo request={this.props.user.requests[this.props.user.selectedRequest]} />
        )}
      </div>
    );
  }
}
