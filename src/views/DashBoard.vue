<template>
    <div class="dashboard">
        <div class="line"></div>
        <div class = 'startrow'>
            <div class = 'stat-box'>
                <div>总访问</div>
                <div class="icon-container">
                    <el-icon ><Promotion /></el-icon>
                </div>
                
            </div>
            <div class = 'stat-box'>
                <div>已借阅</div>
            </div>
            <div class = 'stat-box'>
                <div>图书数</div>
            </div>
            <div class = 'stat-box'>
                <div>用户数</div>
            </div>
        </div>
        <div class="time-row">
            当前时间：{{currentTime}}
        </div>
        <el-card class="chart-card">
            <div ref="chartRef" class="chart"></div>
        </el-card>
    </div>
</template>

<script setup>
import {ref , onMounted, onUnmounted, watch} from 'vue'
import * as echarts from 'echarts'

const currentTime = ref('')
const chartRef = ref(null)
const chartData = {
    categories: ['借阅数', '访问数', '图书数', '用户数'],
    values: [120, 230, 150, 80]
}
let chartInstance = null

function updateTime(){
    const now = new Date()
    currentTime.value = now.toLocaleString()
}

let timer = null
onMounted(() => {
    updateTime()
    timer = setInterval(updateTime, 1000)

    chartInstance = echarts.init(chartRef.value)
    chartInstance.setOption({
        title: {
        text: '平台统计',
        left: 'center'
        },
        tooltip: {},
        xAxis: {
        type: 'category',
        data: chartData.categories
        },
        yAxis: {
        type: 'value'
        },
        series: [
        {
            name: '数量',
            type: 'bar',
            data: chartData.values,
            itemStyle: {
            color: function(params){
                const colors = ['#409EFF', '#67C23A', '#F56C6C', '#909399']
                return colors[params.dataIndex]
            }
        }
    }
        ]
    })

    // 自适应
    window.addEventListener('resize', resizeChart)
})

onUnmounted(() => {
    clearInterval(timer)
    window.removeEventListener('resize', resizeChart)
    chartInstance && chartInstance.dispose()
})

function resizeChart(){
    if(chartInstance){
        chartInstance.resize()
    }
}


</script>


<style>
.dashboard{
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

.line{
    height: 1px;
    background-color: gray;
}
.startrow{
    display: flex;
    gap: 80px;
    justify-content: space-between;
    margin-bottom: 20px;
}
.stat-box{
    display: flex;
    flex-direction: column;
    flex:1;
    border: 1px solid gray;
    border-radius: 10px;
    padding: 20px;
    margin: 5px;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s ease;;
}
.icon-container{
    text-align: center;
}
.time-row{
    margin-top: 20px;
    margin-bottom: 10px;
}
.chart-card {
  padding: 20px;
  box-sizing: border-box;
}

.chart {
  width: 100%;
  height: 600px;
}
</style>