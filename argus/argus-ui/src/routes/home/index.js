import { h, Component } from 'preact';
import style from './style';
import capture from '../../../processing/output.json';
import Heatmap from '../../components/heatmap';

export default class Home extends Component {
	constructor(props) {
		super(props);

		this.apLocations = {
			argus1: {
				x: -145.84,
				y: -43.36
			},
			argus2: {
				x: 111.66,
				y: -43.36
			},
			argus3: {
				x: 34.17,
				y: 86.7
			}
		};

		this.timePoints = {};

		this.state = {
			points: [],
			ranges: {
				time: {},
				x: {},
				y: {}
			}
		};

		this.retrieveLocations = this.retrieveLocations.bind(this);
		this.retrieveLocations();
	}

	componentDidMount() {
		let pointCount = 0;

		const heatmapLapse = () => {
			Object.keys(this.timePoints).sort().forEach((stamp, j) => {
				this.timePoints[stamp].forEach((point, i) => {
					setTimeout(() => {
						pointCount++;
						this.setState(prev => Object.assign({}, prev, {
							points: [point]
						}));

						if (pointCount === capture.loc_updates.length) {
							this.setState(prev => Object.assign({}, prev, {
								points: [{ reset: true }]
							}));

							pointCount = 0;

							heatmapLapse();
						}
					}, ((150 * (j + 1)) + (100 * (i + 1))) * .35);
				});
			});
		};

		heatmapLapse();
	}

	retrieveLocations() {
		const locations = capture.loc_updates;
		let minTime = Math.round(locations[0].timestamp);
		let maxTime = Math.round(locations[0].timestamp);

		const { argus1, argus2, argus3 } = this.apLocations;
		let minX = Math.min(argus1.x, argus2.x, argus3.x);
		let maxX = Math.max(argus1.x, argus2.x, argus3.x);

		let minY = Math.min(argus1.y, argus2.y, argus3.y);
		let maxY = Math.max(argus1.y, argus2.y, argus3.y);


		const timePoints = {};

		// Retrieve mins and maxes
		locations.forEach(l => {
			l.timestamp = Math.round(l.timestamp);
		  if (l.timestamp < minTime) minTime = l.timestamp;
		  else if (l.timestamp > maxTime) maxTime = l.timestamp;

		  const x = l.location[0];
		  const y = l.location[1];

		  if (x < minX) minX = x;
		  else if (x > maxX) maxX = x;

		  if (y < minY) minY = y;
		  else if (y > maxY) maxY = y;

			if (this.timePoints[l.timestamp]) this.timePoints[l.timestamp].push(shiftLocations(l));
			else this.timePoints[l.timestamp] = [shiftLocations(l)];
		});

		// Shift APs
		this.apLocations.argus1.x -= minX;
		this.apLocations.argus1.y -= minY;

		this.apLocations.argus2.x -= minX;
		this.apLocations.argus2.y -= minY;

		this.apLocations.argus3.x -= minX;
		this.apLocations.argus3.y -= minY;

		this.capturePoints = locations.map(shiftLocations);

		this.setState(prev => Object.assign({}, prev, {
			ranges: {
				time: {
					min: minTime,
					max: maxTime
				},
				x: {
					min: 0,
					max: Math.round(maxX - minX)
				},
				y: {
					min: 0,
					max: Math.round(maxY - minY)
				}
			}
		}));

		function shiftLocations(p) {
			return Object.assign({}, p, {
				location: [Math.round(p.location[0] -= minX), Math.round(p.location[1] -= minY)]
			});
		}
	}

	render() {
		return (
			<div class={style.home}>
				<h3>Conference Heatmap</h3>
				<Heatmap aps={this.apLocations} loc={this.state} />
			</div>
		);
	}
}
