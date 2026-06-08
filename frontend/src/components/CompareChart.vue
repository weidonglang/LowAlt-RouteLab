<template>
  <div ref="chartEl" class="compare-chart"></div>
</template>

<script setup lang="ts">
import * as echarts from 'echarts';
import { onBeforeUnmount, onMounted, ref, watch } from 'vue';
import type { RoutePlanSnapshot } from '../types/api';

const props = defineProps<{ results: RoutePlanSnapshot[] }>();
const chartEl = ref<HTMLDivElement | null>(null);
let chart: echarts.ECharts | null = null;

function renderChart() {
  if (!chartEl.value) return;
  if (!chart) chart = echarts.init(chartEl.value);
  const names = props.results.map((item) => item.algorithm);
  chart.setOption({
    tooltip: { trigger: 'axis' },
    legend: { top: 0 },
    grid: { left: 48, right: 24, top: 42, bottom: 32 },
    xAxis: { type: 'category', data: names },
    yAxis: [
      { type: 'value', name: 'm / ms' },
      { type: 'value', name: 'risk', min: 0, max: 1 }
    ],
    series: [
      { name: '距离', type: 'bar', data: props.results.map((item) => item.distance) },
      { name: '耗时', type: 'bar', data: props.results.map((item) => item.planningTimeMs) },
      { name: '风险', type: 'line', yAxisIndex: 1, data: props.results.map((item) => item.riskScore) }
    ]
  });
}

onMounted(() => {
  renderChart();
  window.addEventListener('resize', resize);
});

watch(() => props.results, renderChart, { deep: true });

function resize() {
  chart?.resize();
}

onBeforeUnmount(() => {
  window.removeEventListener('resize', resize);
  chart?.dispose();
});
</script>

