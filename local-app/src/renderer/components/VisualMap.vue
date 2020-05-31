<template>
    <div>
      <div id="visualmap" style="width: 100wh;height:50vh;">
        {{userData}}
        {{solverData}}
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
      backgroundColor: '#E0F7FA',
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
    updateVisualMapNodes(userData) {
      if (!userData || !userData.locations || !myChart) return;

      let new_nodes = this.transformUserDataToVisualDataNodes(userData.locations)
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
    
    updateVisualMapLinks(solverData) {
      if (!solverData || solverData === 'error' || !myChart) return;
      console.log('solverdata from visual map');
      console.log(solverData)
      let new_links = this.transformUserDataToVisualDataLinks(solverData.routes)
      data.links = new_links;
      myChart.setOption({
        series: [
          {
            name: 'visual-map',
            nodes: data.nodes,
            links: data.links
          }
        ]
      })
    },
    
    transformUserDataToVisualDataNodes(locations) {
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
    },

    transformUserDataToVisualDataLinks(routes) {
      let color = [
        '#F57F17',
        '#388E3C',
        '#827717',
        '#6200EA',
        '#5C6BC0',
        '#64B5F6'
      ]
      let new_links = []
      routes.forEach((value, idx) => {
        let c = color[idx % color.length]
        let sub_route = value.sub_route;
        for (let idx = 1; idx < sub_route.length; idx++) {
          new_links.push({
            'source': String(sub_route[idx - 1].from),
            'target': String(sub_route[idx].from),
            'lineStyle': {
              'color': c
            }
          })
        }
      });

      return new_links
    }
  },

  computed: {
    userData() {
      this.updateVisualMapNodes(this.$store.getters.getUserInputData)
      return this.$store.getters.getUserInputData
    },
    solverData() {
      this.updateVisualMapLinks(this.$store.getters.getSolverOutputData)
      return this.$store.getters.getSolverOutputData
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

