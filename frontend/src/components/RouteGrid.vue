<template>
  <div class="grid-shell">
    <svg
      class="route-grid"
      :viewBox="`0 0 ${viewSize} ${viewSize}`"
      role="img"
      aria-label="low altitude grid map"
    >
      <g>
        <rect
          v-for="cell in cells"
          :key="cell.gridId"
          :x="(cell.x - 1) * cellSize"
          :y="(cell.y - 1) * cellSize"
          :width="cellSize"
          :height="cellSize"
          :class="cellClass(cell.gridId)"
        />
      </g>
      <polyline
        v-if="routePoints.length > 1"
        :points="routePoints"
        class="route-line"
        fill="none"
      />
      <circle
        v-for="point in pathPointCenters"
        :key="point.gridId"
        :cx="point.cx"
        :cy="point.cy"
        :r="point.gridId === startGrid || point.gridId === endGrid ? 5.2 : 2.4"
        :class="pointClass(point.gridId)"
      />
      <rect
        v-for="point in conflictCenters"
        :key="point.gridId"
        :x="point.cx - 6"
        :y="point.cy - 6"
        width="12"
        height="12"
        class="conflict-marker"
      />
    </svg>
    <div class="legend-row">
      <span><i class="legend start"></i>起点</span>
      <span><i class="legend end"></i>终点</span>
      <span><i class="legend route"></i>航线</span>
      <span><i class="legend nofly"></i>禁飞区</span>
      <span><i class="legend obstacle"></i>障碍物</span>
      <span><i class="legend risk"></i>风险区</span>
      <span><i class="legend conflict"></i>冲突</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { ConflictItem, GridMap } from '../types/api';

const props = defineProps<{
  mapData: GridMap | null;
  path: string[];
  startGrid: string;
  endGrid: string;
  conflicts?: ConflictItem[];
}>();

const cellSize = 18;
const viewSize = computed(() => (props.mapData?.width ?? 20) * cellSize);
const noFlySet = computed(() => new Set(props.mapData?.noFlyZones.flatMap((zone) => zone.gridIds) ?? []));
const obstacleSet = computed(() => new Set(props.mapData?.obstacles.flatMap((item) => item.gridIds) ?? []));
const riskSet = computed(() => new Set(props.mapData?.riskZones.flatMap((zone) => zone.gridIds) ?? []));
const pathSet = computed(() => new Set(props.path));
const conflictSet = computed(() => new Set((props.conflicts ?? []).map((item) => item.gridId)));
const cells = computed(() => props.mapData?.grids ?? []);

const centerByGrid = computed(() => {
  const centers = new Map<string, { cx: number; cy: number; gridId: string }>();
  for (const cell of cells.value) {
    centers.set(cell.gridId, {
      gridId: cell.gridId,
      cx: (cell.x - 0.5) * cellSize,
      cy: (cell.y - 0.5) * cellSize
    });
  }
  return centers;
});

const pathPointCenters = computed(() =>
  props.path
    .map((gridId) => centerByGrid.value.get(gridId))
    .filter((point): point is { cx: number; cy: number; gridId: string } => Boolean(point))
);

const conflictCenters = computed(() =>
  Array.from(conflictSet.value)
    .map((gridId) => centerByGrid.value.get(gridId))
    .filter((point): point is { cx: number; cy: number; gridId: string } => Boolean(point))
);

const routePoints = computed(() => pathPointCenters.value.map((point) => `${point.cx},${point.cy}`).join(' '));

function cellClass(gridId: string) {
  return {
    cell: true,
    'cell-nofly': noFlySet.value.has(gridId),
    'cell-obstacle': obstacleSet.value.has(gridId),
    'cell-risk': riskSet.value.has(gridId),
    'cell-route': pathSet.value.has(gridId)
  };
}

function pointClass(gridId: string) {
  return {
    'point-node': true,
    'point-start': gridId === props.startGrid,
    'point-end': gridId === props.endGrid,
    'point-route': gridId !== props.startGrid && gridId !== props.endGrid
  };
}
</script>

