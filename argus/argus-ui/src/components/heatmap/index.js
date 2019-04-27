import { h, Component } from 'preact';
import style from './style';
import hm from '../../assets/vendor/heatmap.min';

export default class Heatmap extends Component {
  constructor(props) {
    super(props);

    this.aps = props.aps;
    this.loc = props.loc;
    this.scale = {};
    this.pointCount = 0;
  }

  componentDidMount() {
    this.heatmap = hm.create({
      container: this.heatmapEle,
      radius: 56
    });

    const { height, width } = this.heatmapEle.getBoundingClientRect();

    this.scale.x = width / this.loc.ranges.x.max;
    this.scale.y = height / this.loc.ranges.y.max;

    this.heatmap.setData({
      max: this.loc.ranges.time.max,
      min: this.loc.ranges.time.min,
      data: []
    });

    Object.values(this.aps).forEach(ap => {
      const apDim = ap.ele.getBoundingClientRect();
      ap.ele.style.top = Math.min(ap.y * this.scale.y, height - apDim.height) + 'px';
      ap.ele.style.left = Math.min(ap.x * this.scale.x, width - apDim.width) + 'px'
    });
  }

  componentDidUpdate(prevProps, prevState) {
    this.pointCount += this.props.loc.points.length;
    if (this.props.loc.points[0].reset) {
      this.heatmap.setData({
        max: this.loc.ranges.time.max,
        min: this.loc.ranges.time.min,
        data: []
      });

      this.pointCount = 0;
    } else {
      this.heatmap.addData(this.createHeatmapPoints(this.props.loc.points));
    }

    this.heatmap.repaint();
  }

  createHeatmapPoints(points) {
    return points.map(p => ({
      x: Math.round(p.location[0] * this.scale.x),
      y: Math.round(p.location[1] * this.scale.y),
      value: p.timestamp
    }));
  }

  render() {
    return (
      <div class={style.heatmap}>
        <span id='argus1' class={style.ap} ref={a => this.aps.argus1.ele = a}>1</span>
        <span id='argus2' class={style.ap} ref={a => this.aps.argus2.ele = a}>2</span>
        <span id='argus3' class={style.ap} ref={a => this.aps.argus3.ele = a}>3</span>
        <div ref={e => this.heatmapEle = e}></div>

        <figure class={style.legend}>
          <figcaption class={style.ap}>#</figcaption>
          <figcaption>: Id of Argus Access Point</figcaption>
        </figure>
      </div>
    );
  }


}
