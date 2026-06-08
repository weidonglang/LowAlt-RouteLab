export interface ApiResponse<T> {
  code: number;
  message: string;
  data: T;
}

export interface RoutePlanSnapshot {
  id: number;
  algorithm: string;
  success: boolean;
  path: string[];
  distance: number;
  estimatedTimeSeconds: number;
  turnCount: number;
  planningTimeMs: number;
  visitedCount: number;
  riskScore: number;
  riskLevel: string;
  riskFactors: string[];
  estimatedBatteryUsage: number;
  batteryLimit: number;
  energySafe: boolean;
  error?: string | null;
}

export interface OccupancyUnit {
  gridId: string;
  levelId: string;
  slotStart: string;
  slotEnd: string;
  sequenceNo: number;
}

export interface ConflictItem {
  gridId: string;
  levelId: string;
  slotStart: string;
  slotEnd: string;
  conflictType: string;
  description: string;
}

export interface ConflictCheckResult {
  conflictStatus: string;
  conflictCount: number;
  conflicts: ConflictItem[];
}

export interface SkyGridSubmitResult {
  bookingStatus: string;
  bookingId: string;
  message: string;
}

export interface RouteTaskResponse {
  id: number;
  taskName: string;
  taskType: string;
  mapId: string;
  startGrid: string;
  endGrid: string;
  startLevel: string;
  droneModel?: string | null;
  algorithm: string;
  avoidRisk: boolean;
  allowDiagonal: boolean;
  connectSkyGrid: boolean;
  startTime: string;
  speedMps: number;
  gridSizeMeters: number;
  slotMinutes: number;
  status: string;
  plan?: RoutePlanSnapshot | null;
  occupancyUnits: OccupancyUnit[];
  conflictCheck?: ConflictCheckResult | null;
  skyGridSubmit?: SkyGridSubmitResult | null;
}

export interface CreateRouteTaskRequest {
  taskName: string;
  taskType: string;
  mapId?: string;
  startGrid: string;
  endGrid: string;
  startLevel: string;
  droneModel?: string;
  algorithm: string;
  avoidRisk: boolean;
  allowDiagonal: boolean;
  connectSkyGrid: boolean;
  startTime: string;
  speedMps: number;
  gridSizeMeters: number;
  slotMinutes: number;
}

export interface PlanCompareResult {
  results: RoutePlanSnapshot[];
}

export interface GridMap {
  mapId: string;
  width: number;
  height: number;
  gridSizeMeters: number;
  levels: string[];
  grids: Array<{
    gridId: string;
    x: number;
    y: number;
    terrainType: string;
    riskBase: number;
    isNoFly: boolean;
    isObstacle: boolean;
  }>;
  noFlyZones: Array<{ gridIds: string[] }>;
  obstacles: Array<{ gridIds: string[]; blockedLevels: string[] }>;
  riskZones: Array<{ gridIds: string[]; riskWeight: number; riskType: string }>;
}

