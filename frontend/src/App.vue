<template>
  <div class="app-frame">
    <aside class="sidebar">
      <div class="brand-block">
        <div class="brand-mark">LR</div>
        <div>
          <h1>LowAlt-RouteLab</h1>
          <p>Grid + Level + TimeSlot</p>
        </div>
      </div>
      <el-menu :default-active="activeView" class="nav-menu" @select="selectView">
        <el-menu-item index="task"><ClipboardList :size="18" />任务创建</el-menu-item>
        <el-menu-item index="route"><Map :size="18" />航线展示</el-menu-item>
        <el-menu-item index="risk"><ShieldAlert :size="18" />风险评估</el-menu-item>
        <el-menu-item index="compare"><BarChart3 :size="18" />算法对比</el-menu-item>
        <el-menu-item index="skygrid"><RadioTower :size="18" />SkyGrid 联动</el-menu-item>
      </el-menu>
      <div class="service-box">
        <span>algorithm-service</span>
        <strong>127.0.0.1:8001</strong>
        <span>route-adapter-service</span>
        <strong>127.0.0.1:8081</strong>
      </div>
    </aside>

    <main class="workspace">
      <header class="topbar">
        <div>
          <h2>{{ viewTitle }}</h2>
          <p>{{ viewSubtitle }}</p>
        </div>
        <div class="top-actions">
          <el-button :icon="RefreshCw" @click="loadMap" />
          <el-tag :type="currentTask?.status === 'PLANNED' ? 'success' : 'info'">
            {{ currentTask?.status ?? 'READY' }}
          </el-tag>
        </div>
      </header>

      <section v-show="activeView === 'task'" class="view-grid task-layout">
        <div class="panel form-panel">
          <el-form label-position="top" :model="taskForm">
            <div class="form-grid">
              <el-form-item label="任务名称">
                <el-input v-model="taskForm.taskName" />
              </el-form-item>
              <el-form-item label="任务类型">
                <el-select v-model="taskForm.taskType">
                  <el-option label="电力巡检" value="POWER_LINE_INSPECTION" />
                  <el-option label="物流配送" value="LOGISTICS_DELIVERY" />
                  <el-option label="应急救援" value="EMERGENCY_RESCUE" />
                </el-select>
              </el-form-item>
              <el-form-item label="起点">
                <el-input v-model="taskForm.startGrid" />
              </el-form-item>
              <el-form-item label="终点">
                <el-input v-model="taskForm.endGrid" />
              </el-form-item>
              <el-form-item label="高度层">
                <el-select v-model="taskForm.startLevel">
                  <el-option v-for="level in mapData?.levels ?? levels" :key="level" :label="level" :value="level" />
                </el-select>
              </el-form-item>
              <el-form-item label="算法">
                <el-select v-model="taskForm.algorithm">
                  <el-option label="A*" value="A_STAR" />
                  <el-option label="Dijkstra" value="DIJKSTRA" />
                  <el-option label="Theta*" value="THETA_STAR" />
                </el-select>
              </el-form-item>
              <el-form-item label="起飞时间">
                <el-input v-model="taskForm.startTime" />
              </el-form-item>
              <el-form-item label="速度 m/s">
                <el-input-number v-model="taskForm.speedMps" :min="1" :max="40" />
              </el-form-item>
            </div>
            <div class="switch-row">
              <el-checkbox v-model="taskForm.avoidRisk">规避风险</el-checkbox>
              <el-checkbox v-model="taskForm.allowDiagonal">允许斜向</el-checkbox>
              <el-checkbox v-model="taskForm.connectSkyGrid">连接 SkyGrid</el-checkbox>
            </div>
            <div class="command-row">
              <el-button type="primary" :icon="Play" :loading="busy" @click="createAndPlan">开始规划</el-button>
              <el-button :icon="FilePlus2" @click="createOnly">只创建任务</el-button>
              <el-button :icon="RouteIcon" :disabled="!currentTask" @click="runPlan">重新规划</el-button>
            </div>
          </el-form>
        </div>
        <RouteGrid
          class="panel"
          :map-data="mapData"
          :path="currentTask?.plan?.path ?? []"
          :start-grid="taskForm.startGrid"
          :end-grid="taskForm.endGrid"
          :conflicts="currentTask?.conflictCheck?.conflicts ?? []"
        />
      </section>

      <section v-show="activeView === 'route'" class="view-grid route-layout">
        <RouteGrid
          class="panel"
          :map-data="mapData"
          :path="currentTask?.plan?.path ?? []"
          :start-grid="taskForm.startGrid"
          :end-grid="taskForm.endGrid"
          :conflicts="currentTask?.conflictCheck?.conflicts ?? []"
        />
        <div class="panel detail-panel">
          <MetricStrip :metrics="routeMetrics" />
          <el-table :data="pathRows" height="390" size="small">
            <el-table-column prop="seq" label="#" width="60" />
            <el-table-column prop="gridId" label="Grid" />
          </el-table>
        </div>
      </section>

      <section v-show="activeView === 'risk'" class="view-grid risk-layout">
        <div class="panel">
          <MetricStrip :metrics="riskMetrics" />
          <div class="risk-gauge">
            <div class="gauge-fill" :style="{ width: `${riskPercent}%` }"></div>
            <span>{{ currentTask?.plan?.riskLevel ?? 'LOW' }}</span>
          </div>
          <el-table :data="riskRows" size="small">
            <el-table-column prop="factor" label="风险因素" />
          </el-table>
        </div>
        <RouteGrid
          class="panel"
          :map-data="mapData"
          :path="currentTask?.plan?.path ?? []"
          :start-grid="taskForm.startGrid"
          :end-grid="taskForm.endGrid"
          :conflicts="currentTask?.conflictCheck?.conflicts ?? []"
        />
      </section>

      <section v-show="activeView === 'compare'" class="view-grid compare-layout">
        <div class="panel">
          <div class="command-row">
            <el-button type="primary" :icon="BarChart3" :loading="busy" @click="runCompare">执行对比</el-button>
            <el-checkbox-group v-model="compareAlgorithmsSelected">
              <el-checkbox label="DIJKSTRA" />
              <el-checkbox label="A_STAR" />
              <el-checkbox label="THETA_STAR" />
            </el-checkbox-group>
          </div>
          <CompareChart :results="compareResults" />
        </div>
        <div class="panel">
          <el-table :data="compareResults" size="small" height="460">
            <el-table-column prop="algorithm" label="算法" width="110" />
            <el-table-column prop="distance" label="距离 m" />
            <el-table-column prop="planningTimeMs" label="耗时 ms" />
            <el-table-column prop="turnCount" label="转弯" />
            <el-table-column prop="riskScore" label="风险" />
          </el-table>
        </div>
      </section>

      <section v-show="activeView === 'skygrid'" class="view-grid skygrid-layout">
        <div class="panel">
          <div class="command-row">
            <el-button type="primary" :icon="ScanSearch" :disabled="!currentTask?.plan" @click="runConflictCheck">
              冲突检查
            </el-button>
            <el-button :icon="Send" :disabled="!currentTask?.plan" @click="runSubmit">提交预约</el-button>
          </div>
          <MetricStrip :metrics="skygridMetrics" />
          <el-table :data="currentTask?.occupancyUnits ?? []" height="390" size="small">
            <el-table-column prop="sequenceNo" label="#" width="60" />
            <el-table-column prop="gridId" label="Grid" />
            <el-table-column prop="levelId" label="Level" />
            <el-table-column prop="slotStart" label="Slot Start" />
            <el-table-column prop="slotEnd" label="Slot End" />
          </el-table>
        </div>
        <div class="panel">
          <RouteGrid
            :map-data="mapData"
            :path="currentTask?.plan?.path ?? []"
            :start-grid="taskForm.startGrid"
            :end-grid="taskForm.endGrid"
            :conflicts="currentTask?.conflictCheck?.conflicts ?? []"
          />
        </div>
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue';
import { ElMessage } from 'element-plus';
import {
  BarChart3,
  ClipboardList,
  FilePlus2,
  Map,
  Play,
  RadioTower,
  RefreshCw,
  Route as RouteIcon,
  ScanSearch,
  Send,
  ShieldAlert
} from '@lucide/vue';
import RouteGrid from './components/RouteGrid.vue';
import MetricStrip from './components/MetricStrip.vue';
import CompareChart from './components/CompareChart.vue';
import {
  checkConflict,
  compareAlgorithms,
  createTask,
  fetchMap,
  planTask,
  submitSkyGrid
} from './services/api';
import type { CreateRouteTaskRequest, GridMap, RoutePlanSnapshot, RouteTaskResponse } from './types/api';

const activeView = ref('task');
const busy = ref(false);
const mapData = ref<GridMap | null>(null);
const currentTask = ref<RouteTaskResponse | null>(null);
const compareResults = ref<RoutePlanSnapshot[]>([]);
const compareAlgorithmsSelected = ref(['DIJKSTRA', 'A_STAR', 'THETA_STAR']);
const levels = ['L60', 'L90', 'L120', 'L150', 'L180'];

const taskForm = reactive<CreateRouteTaskRequest>({
  taskName: 'power inspection demo',
  taskType: 'POWER_LINE_INSPECTION',
  mapId: 'demo-city-20x20',
  startGrid: 'G-01-01',
  endGrid: 'G-18-16',
  startLevel: 'L120',
  droneModel: 'M30',
  algorithm: 'A_STAR',
  avoidRisk: true,
  allowDiagonal: true,
  connectSkyGrid: true,
  startTime: '2026-06-08T10:00:00',
  speedMps: 10,
  gridSizeMeters: 100,
  slotMinutes: 5
});

const viewTitle = computed(() => ({
  task: '任务创建',
  route: '航线规划展示',
  risk: '风险评估',
  compare: '算法对比',
  skygrid: 'SkyGrid 联动'
})[activeView.value] ?? '任务创建');

const viewSubtitle = computed(() => ({
  task: '配置低空任务参数并触发规划',
  route: '查看网格地图、限制区和规划航线',
  risk: '查看风险评分、解释和能耗安全性',
  compare: '比较 Dijkstra、A*、Theta* 的距离和耗时',
  skygrid: '查看 TimeSlot 占用、冲突检查和模拟预约'
})[activeView.value] ?? '');

const routeMetrics = computed(() => {
  const plan = currentTask.value?.plan;
  return [
    { label: '距离 m', value: plan?.distance?.toFixed(1) ?? '-' },
    { label: '耗时 s', value: plan?.estimatedTimeSeconds ?? '-' },
    { label: '转弯', value: plan?.turnCount ?? '-' },
    { label: '规划 ms', value: plan?.planningTimeMs ?? '-' }
  ];
});

const riskMetrics = computed(() => {
  const plan = currentTask.value?.plan;
  return [
    { label: '风险分', value: plan?.riskScore?.toFixed(3) ?? '-' },
    { label: '风险等级', value: plan?.riskLevel ?? '-' },
    { label: '电池消耗', value: plan ? `${plan.estimatedBatteryUsage.toFixed(2)} / ${plan.batteryLimit}` : '-' },
    { label: '能耗安全', value: plan?.energySafe ? 'YES' : '-' }
  ];
});

const skygridMetrics = computed(() => [
  { label: '占用单元', value: currentTask.value?.occupancyUnits?.length ?? 0 },
  { label: '冲突状态', value: currentTask.value?.conflictCheck?.conflictStatus ?? '-' },
  { label: '冲突数', value: currentTask.value?.conflictCheck?.conflictCount ?? 0 },
  { label: '预约状态', value: currentTask.value?.skyGridSubmit?.bookingStatus ?? '-' }
]);

const pathRows = computed(() =>
  (currentTask.value?.plan?.path ?? []).map((gridId, index) => ({ seq: index + 1, gridId }))
);

const riskRows = computed(() =>
  (currentTask.value?.plan?.riskFactors ?? []).map((factor) => ({ factor }))
);

const riskPercent = computed(() => Math.min((currentTask.value?.plan?.riskScore ?? 0) * 100, 100));

async function loadMap() {
  mapData.value = await fetchMap(taskForm.mapId ?? 'demo-city-20x20');
}

async function createOnly() {
  await withBusy(async () => {
    currentTask.value = await createTask(taskForm);
    ElMessage.success('任务已创建');
  });
}

async function createAndPlan() {
  await withBusy(async () => {
    const task = await createTask(taskForm);
    currentTask.value = await planTask(task.id);
    activeView.value = 'route';
    ElMessage.success('规划完成');
  });
}

async function runPlan() {
  if (!currentTask.value) return;
  await withBusy(async () => {
    currentTask.value = await planTask(currentTask.value!.id);
    ElMessage.success('规划已刷新');
  });
}

async function runCompare() {
  await withBusy(async () => {
    const result = await compareAlgorithms({
      mapId: taskForm.mapId ?? 'demo-city-20x20',
      startGrid: taskForm.startGrid,
      endGrid: taskForm.endGrid,
      level: taskForm.startLevel,
      algorithms: compareAlgorithmsSelected.value,
      avoidRisk: taskForm.avoidRisk,
      allowDiagonal: taskForm.allowDiagonal
    });
    compareResults.value = result.results;
  });
}

async function runConflictCheck() {
  if (!currentTask.value) return;
  await withBusy(async () => {
    const conflict = await checkConflict(currentTask.value!.id);
    currentTask.value = { ...currentTask.value!, conflictCheck: conflict, status: 'CONFLICT_CHECKED' };
    ElMessage.success('冲突检查完成');
  });
}

async function runSubmit() {
  if (!currentTask.value) return;
  await withBusy(async () => {
    const submit = await submitSkyGrid(currentTask.value!.id);
    currentTask.value = { ...currentTask.value!, skyGridSubmit: submit, status: 'SUBMITTED_TO_SKYGRID' };
    ElMessage.success('已提交 Mock SkyGrid');
  });
}

async function withBusy(action: () => Promise<void>) {
  try {
    busy.value = true;
    await action();
  } catch (error) {
    ElMessage.error(error instanceof Error ? error.message : '操作失败');
  } finally {
    busy.value = false;
  }
}

function selectView(index: string) {
  activeView.value = index;
}

onMounted(async () => {
  await loadMap();
  await runCompare();
});
</script>
