import React from 'react';
import Navbar from '../utils/Navbar';
import foggyBlueForest from '../static/foggy_blue_forest.jpg';
import whispering from '../static/whispering.jpg';

const Dashboard = () => {
	return (
		<div className="container">
			<Navbar />
			<div className="row">
				<div className="col-md-12">
					<h1 className="text-center welcome-message">Welcome to Whisperer</h1>
					<p className="text-center shadows">Where the shadows come alive...</p>
					<img src={foggyBlueForest} alt="Mysterious Background" className="img-fluid" />
					<div className="join-us-container">
						<p className="text-center join-us">Join our community of whispers, where you can share your thoughts and connect with others who share your interests.</p>
						<img src={whispering} alt="Whispering" className="img-fluid" />
					</div>
				</div>
			</div>
		</div>
	);
};

export default Dashboard;
