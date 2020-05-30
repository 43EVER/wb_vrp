<template>
  <div>
      <el-upload
        :auto-upload="false"
        :on-change="fileChange"
        ref="upload"
        class="upload-demo"
        action="#"
        :limit="1"
        accept=".txt">
        <el-button slot="trigger" size="mini" type="success" plain>选取文件</el-button>
        <i slot="tip" class="el-upload__tip el-icon-info">只能选取txt</i>
    </el-upload>
  </div>
</template>

<script>
import { Message } from 'element-ui';
import { mapMutations } from 'vuex'

export default {
    methods: {
        ...mapMutations([
            'changeUserInputData'
        ]),

        async fileChange(f) {
            let reader = new FileReader();
            reader.readAsText(f.raw);
            let promise = new Promise((resolve, reject) => {
                reader.onload = () => {
                    resolve(reader.result);
                }
            });

            let raw_data = await promise;
            let data = this.transformData(raw_data);
            
            this.changeUserInputData({data});

            Message({
                message: "文件读取成功",
                type: "success"
            })
            console.log(JSON.stringify(data))
        },

        transformData(raw_data) {
            let lines = raw_data.split('\n');

            let gen = function* () {
                let inner_data = [];
                for (let idx = 0; idx < lines.length; idx++) {
                    if (lines[idx].trim() === "") {
                        yield inner_data;
                        inner_data = [];
                        continue;
                    }
                    inner_data.push(lines[idx].split(' '));
                }
                yield inner_data;
            }


            // 添加坐标和需求，并进行单位转换，KM -> M，T -> Kg
            let locations = [];
            let demands = [];
            let gl = gen();
            let tmp = gl.next().value;
            tmp.forEach((raw_arr) => {
                let arr = raw_arr.map(value => (Number(value) * 1000));
                locations.push([arr[0], arr[1]]);
                demands.push(arr[2])
            });
            console.log("坐标数据(m)");
            console.log(locations);

            console.log("需求数据(kg)");
            console.log(demands);

            // 添加时间窗口
            let time_windows = [];
            tmp = gl.next().value;
            tmp.forEach((raw_arr) => {
                let arr = raw_arr.map(value => Number(value));
                time_windows.push([arr[0], arr[1]]);
            });
            console.log("时间窗口");
            console.log(time_windows);

            // 添加车辆
            let vehicle_capacity = []
            tmp = gl.next().value;
            vehicle_capacity = (tmp[0]).map(value => Number(value));
            console.log("车辆容量");
            console.log(vehicle_capacity);

            // 车辆最大行驶距离
            let max_dis_per_vehicle = NaN;
            tmp = gl.next().value;
            max_dis_per_vehicle = Number(tmp[0][0] * 1000);
            console.log("最大行驶距离（m）");
            console.log(max_dis_per_vehicle);

            // 车辆行驶速度
            let vehicle_speed = NaN;
            tmp = gl.next().value;
            vehicle_speed = Math.ceil(Number(tmp[0][0]) * 1000 / 60);
            console.log("行驶速度");
            console.log(vehicle_speed);

            // 下货时间
            let time_per_location = NaN;
            tmp = gl.next().value;
            time_per_location = Number(tmp[0][0]);
            console.log("下货时间");
            console.log(time_per_location);

            return {
                locations,
                max_dis_per_vehicle,

                time_windows,
                time_per_location,
                vehicle_speed,

                demands,
                vehicle_capacity
            };
        }
    }
}
</script>
