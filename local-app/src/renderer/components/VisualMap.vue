<template>
    <div>
      <div id="visualmap" style="width: 40wh;height:40vh;">
        {{userData}}
      </div>
    </div>
</template>

<script>
import { mapGetters } from 'vuex';

let myChart = null;
let data = {}
data.nodes = [
]
data.links = []

export default {

  mounted() {
    myChart = this.$echarts.init(document.getElementById('visualmap'));

    // 使用刚指定的配置项和数据显示图表。


    myChart.setOption({
      series: [
        {
          name: 'visual-map',
          type: 'graph',
          hoverAnimation: true,
          legendHoverLink: true,
          symbol: 'circle',
          edgeSymbol: ['none', 'arrow'],
          roam: true,
          symbolSize: 15,
          itemStyle: {

          },
          lineStyle: {
          },
          nodeScaleRatio: 0.2,
          
          label: {
            normal: {
              show: true,
              position: 'inside',
            }
          },

          nodes: data.nodes,
          links: data.links
        }
      ]
    })
  },

  methods: {
    updateVisualMap(userData) {
      if (!userData || !userData.locations || !myChart) return;

      let new_nodes = this.transformUserDataToVisualData(userData.locations)
      data.nodes = new_nodes
      myChart.setOption({
        series: [
          {
            name: 'visual-map',
            nodes: data.nodes,
            links: data.links
          }
        ]
      })
      console.log("update data")
      console.log(data.nodes)
    },
    transformUserDataToVisualData(locations) {
      let new_nodes = []
      locations.forEach((value, idx) => {
        new_nodes.push({
          name: String(idx),
          x: value[0],
          y: value[1]
        });
      });
      if (new_nodes.length === 0) return new_nodes;
      new_nodes[0].itemStyle = {
        color: '#000'
      };
      return new_nodes
    }
  },

  computed: {
    userData() {
      this.updateVisualMap(this.$store.getters.getUserInputData)
      return this.$store.getters.getUserInputData
    }
  },

}
</script>

<style lang="scss">
* {
  margin: 0;
  padding: 0;
}
</style>

