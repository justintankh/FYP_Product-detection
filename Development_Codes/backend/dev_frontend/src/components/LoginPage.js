import React, { Component } from "react";

export default class LoginPage extends Component {
	constructor(props) {
		super(props);
		this.state = {
			roomCode: "",
			error: "",
		};
	}

	render() {
		return (
			<div>
				<p>This is the join room page</p>
				<button>
					<a href="/frontend/">Home</a>
				</button>
				<button>
					<a href="/frontend/create">Create</a>
				</button>
			</div>
		);
	}
}
