package com.lowalt.routelab.adapter.task;

import com.lowalt.routelab.adapter.algorithm.TimeSlotConvertResult;
import com.lowalt.routelab.adapter.skygrid.ConflictCheckResult;
import com.lowalt.routelab.adapter.skygrid.SkyGridSubmitResult;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

public class RouteTask {

    private final long id;
    private final String taskName;
    private final String taskType;
    private final String mapId;
    private final String startGrid;
    private final String endGrid;
    private final String startLevel;
    private final String droneModel;
    private final String algorithm;
    private final boolean avoidRisk;
    private final boolean allowDiagonal;
    private final boolean connectSkyGrid;
    private final LocalDateTime startTime;
    private final double speedMps;
    private final double gridSizeMeters;
    private final int slotMinutes;
    private final LocalDateTime createdAt;
    private LocalDateTime updatedAt;
    private String status;
    private RoutePlanSnapshot plan;
    private List<TimeSlotConvertResult.OccupancyUnit> occupancyUnits = new ArrayList<>();
    private ConflictCheckResult conflictCheck;
    private SkyGridSubmitResult skyGridSubmit;

    public RouteTask(long id, CreateRouteTaskRequest request) {
        this.id = id;
        this.taskName = request.taskName();
        this.taskType = request.taskType();
        this.mapId = defaultString(request.mapId(), "demo-city-20x20");
        this.startGrid = request.startGrid();
        this.endGrid = request.endGrid();
        this.startLevel = request.startLevel();
        this.droneModel = request.droneModel();
        this.algorithm = defaultString(request.algorithm(), "A_STAR");
        this.avoidRisk = request.avoidRisk() == null || request.avoidRisk();
        this.allowDiagonal = request.allowDiagonal() == null || request.allowDiagonal();
        this.connectSkyGrid = request.connectSkyGrid() == null || request.connectSkyGrid();
        this.startTime = request.startTime();
        this.speedMps = request.speedMps() == null ? 10.0 : request.speedMps();
        this.gridSizeMeters = request.gridSizeMeters() == null ? 100.0 : request.gridSizeMeters();
        this.slotMinutes = request.slotMinutes() == null ? 5 : request.slotMinutes();
        this.status = "CREATED";
        this.createdAt = LocalDateTime.now();
        this.updatedAt = this.createdAt;
    }

    public long id() {
        return id;
    }

    public String taskName() {
        return taskName;
    }

    public String taskType() {
        return taskType;
    }

    public String mapId() {
        return mapId;
    }

    public String startGrid() {
        return startGrid;
    }

    public String endGrid() {
        return endGrid;
    }

    public String startLevel() {
        return startLevel;
    }

    public String droneModel() {
        return droneModel;
    }

    public String algorithm() {
        return algorithm;
    }

    public boolean avoidRisk() {
        return avoidRisk;
    }

    public boolean allowDiagonal() {
        return allowDiagonal;
    }

    public boolean connectSkyGrid() {
        return connectSkyGrid;
    }

    public LocalDateTime startTime() {
        return startTime;
    }

    public double speedMps() {
        return speedMps;
    }

    public double gridSizeMeters() {
        return gridSizeMeters;
    }

    public int slotMinutes() {
        return slotMinutes;
    }

    public LocalDateTime createdAt() {
        return createdAt;
    }

    public LocalDateTime updatedAt() {
        return updatedAt;
    }

    public String status() {
        return status;
    }

    public RoutePlanSnapshot plan() {
        return plan;
    }

    public List<TimeSlotConvertResult.OccupancyUnit> occupancyUnits() {
        return occupancyUnits;
    }

    public ConflictCheckResult conflictCheck() {
        return conflictCheck;
    }

    public SkyGridSubmitResult skyGridSubmit() {
        return skyGridSubmit;
    }

    public void markPlanned(RoutePlanSnapshot plan, List<TimeSlotConvertResult.OccupancyUnit> occupancyUnits) {
        this.plan = plan;
        this.occupancyUnits = List.copyOf(occupancyUnits);
        this.status = plan.success() ? "PLANNED" : "PLAN_FAILED";
        touch();
    }

    public void markConflictChecked(ConflictCheckResult result) {
        this.conflictCheck = result;
        this.status = "CONFLICT_CHECKED";
        touch();
    }

    public void markSubmitted(SkyGridSubmitResult result) {
        this.skyGridSubmit = result;
        this.status = "SUBMITTED_TO_SKYGRID";
        touch();
    }

    private void touch() {
        this.updatedAt = LocalDateTime.now();
    }

    private static String defaultString(String value, String defaultValue) {
        return value == null || value.isBlank() ? defaultValue : value;
    }
}

