<template>
  <div>
    <el-container v-loading="calculating" direction="vertical">
        <el-row >
        <el-switch
            v-model="isImport"
            :disabled="calculating"
            active-text="导入数据"
            inactive-text="输入数据">
        </el-switch>
        </el-row>
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
        async startTransform() {
            this.calculating = true
            let text = this.calButtonText;
            this.calButtonText = "计算中"
            let promise = new Promise((resolve, reject) => {
                // 开始计算
                
            })
            await promise
            this.calculating = false;
            this.calButtonText = text;
        }
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