<template>
  <div id="app">
    <el-container>
      <el-main>
        <user-data />
      </el-main>
      <el-main>
        <visual-map />
      </el-main>
    </el-container>
  </div>
</template>

<script>
import UserData from './components/UserData.vue'
import VisualMap from './components/VisualMap.vue'

export default {
  name: 'app',
  components: {
    UserData,
    VisualMap
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
}
</style>>
