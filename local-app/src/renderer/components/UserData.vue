<template>
  <div>
    <el-container v-loading="calculating" direction="vertical">
        <el-row >

        </el-row>
        <!-- <el-switch
            v-model="isImport"
            :disabled="calculating"
            active-text="导入数据"
            inactive-text="输入数据">
        </el-switch> -->
        <el-row class="container">
            <import-data v-if="isImport"/>
            <input-data v-else />
        </el-row>
    </el-container>
    <el-row>
      <el-button type="primary" size="medium" :loading="calculating" @click="startTransform"> {{calButtonText}} </el-button>
    </el-row>
  </div>
</template>

<script>
import InputData from "./InputData.vue";
import ImportData from "./ImportData.vue";
import cmd from 'node-cmd';
import { mapGetters, mapMutations } from "vuex";

export default {
    components: {
      InputData,
      ImportData
    },

    data() {
        return {
            isImport: true,
            calButtonText: "计算",
            calculating: false
        }
    },

    watch: {
      isImport: function(newVal, oldVal) {
        console.log(`newVal: ${newVal}, oldVal: ${oldVal}`)
      }
    },

    methods: {
        ...mapMutations(['changeUserInputData', 'changeSolverOutputData']),

        async startTransform() {
            this.calculating = true
            let text = this.calButtonText;
            this.calButtonText = "计算中"
            let promise = new Promise((resolve, reject) => {
              cmd.get(`.\\solver.exe "${JSON.stringify(this.getUserInputData)}"`, (err, data, stderr) => {
                if (err || stderr) {
                  this.$message({
                    type: 'error',
                    message: '计算错误'
                  })
                  resolve()
                }
                data = data.replace(/\'/g, '\"')
                console.log(`solver's data: ${data}`)
                this.changeSolverOutputData({
                    'data': JSON.parse(data)
                  })
                resolve()
              })
            });

            await promise
            this.calculating = false;
            this.calButtonText = text;
        }
    },
    
    computed: {
      ...mapGetters(['getUserInputData', 'getSolverOutputData'])
    }
}
</script>

<style lang="scss">
.container {
    margin-top: 3rem;
}

.el-row {
  margin-top: 3rem;
}
</style>