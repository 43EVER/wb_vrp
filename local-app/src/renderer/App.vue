<template>
  <div id="app">
    <el-container>
        <el-main><user-data /></el-main>
        <el-main><visual-map /></el-main>
    </el-container>
    <div class="detail-data">
        <el-row v-for="(item, idx) in getSolverOutputData.routes" :key="idx">
        <el-tag>车辆编号：{{item.vehicle_idx}}</el-tag>
        <el-tag>路线距离：{{`${item.route_dis} m`}}</el-tag>
        <el-tag>装载货物：{{`${item.route_load} Kg`}}</el-tag>
        <el-tag>车辆最大载重：{{`${getUserInputData.vehicle_capacity[item.vehicle_idx] * 1000} Kg`}}</el-tag>
        <br />
        <el-steps>
          <el-step status="process" v-for="(sub_item, idx) in item.sub_route" :key="idx" icon="el-icon-truck" :title="`${sub_item.from}`" :description="`窗口：${sub_item.time_window[0]}, ${sub_item.time_window[1]}`"></el-step>
        </el-steps>
      </el-row>
      <el-row>
        <el-tag>总距离：{{getSolverOutputData.total_distance}} m</el-tag>
      </el-row>
    </div>
  </div>
</template>

<script>
import UserData from './components/UserData.vue'
import VisualMap from './components/VisualMap.vue'
import { mapGetters } from "vuex";

export default {
  name: 'app',
  components: {
    UserData,
    VisualMap
  },
  computed: {
    ...mapGetters(["getUserInputData", "getSolverOutputData"])
  },

  methods: {
    transData(data) {
          let str = ''
          str += `(${data[0].time_window[0]}, ${data[0].time_window[1]}) ${data[0].from}`
          for (let idx = 1; idx < data.length; idx++) {
            str += `      ->      (${data[idx].time_window[0]}, ${data[idx].time_window[1]}) ${data[idx].from}`
          }
          return str
        },
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
}

.detail-data {
  padding: 4rem;
}
</style>>
