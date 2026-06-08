import axios from 'axios';
import type {
  ApiResponse,
  ConflictCheckResult,
  CreateRouteTaskRequest,
  GridMap,
  PlanCompareResult,
  RouteTaskResponse,
  SkyGridSubmitResult
} from '../types/api';

const adapter = axios.create({ baseURL: '/adapter-api' });
const algorithm = axios.create({ baseURL: '/algorithm-api' });

async function unwrap<T>(promise: Promise<{ data: ApiResponse<T> }>): Promise<T> {
  const response = await promise;
  return response.data.data;
}

export function fetchMap(mapId: string): Promise<GridMap> {
  return unwrap(algorithm.get(`/api/maps/${mapId}`));
}

export function createTask(payload: CreateRouteTaskRequest): Promise<RouteTaskResponse> {
  return unwrap(adapter.post('/api/tasks', payload));
}

export function planTask(taskId: number): Promise<RouteTaskResponse> {
  return unwrap(adapter.post(`/api/tasks/${taskId}/plan`));
}

export function getTask(taskId: number): Promise<RouteTaskResponse> {
  return unwrap(adapter.get(`/api/tasks/${taskId}`));
}

export function checkConflict(taskId: number): Promise<ConflictCheckResult> {
  return unwrap(adapter.post(`/api/tasks/${taskId}/check-conflict`));
}

export function submitSkyGrid(taskId: number): Promise<SkyGridSubmitResult> {
  return unwrap(adapter.post(`/api/tasks/${taskId}/submit-skygrid`));
}

export function compareAlgorithms(payload: {
  mapId: string;
  startGrid: string;
  endGrid: string;
  level: string;
  algorithms: string[];
  avoidRisk: boolean;
  allowDiagonal: boolean;
}): Promise<PlanCompareResult> {
  return unwrap(algorithm.post('/api/plan/compare', payload));
}

