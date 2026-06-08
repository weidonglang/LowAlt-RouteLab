package com.lowalt.routelab.adapter.task;

import com.lowalt.routelab.adapter.algorithm.AlgorithmClient;
import com.lowalt.routelab.adapter.algorithm.AlgorithmPlanRequest;
import com.lowalt.routelab.adapter.algorithm.AlgorithmPlanResult;
import com.lowalt.routelab.adapter.algorithm.TimeSlotConvertRequest;
import com.lowalt.routelab.adapter.algorithm.TimeSlotConvertResult;
import com.lowalt.routelab.adapter.skygrid.ConflictCheckResult;
import com.lowalt.routelab.adapter.skygrid.SkyGridClient;
import com.lowalt.routelab.adapter.skygrid.SkyGridSubmitResult;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.concurrent.atomic.AtomicLong;

@Service
public class RouteTaskService {

    private static final DateTimeFormatter DATE_TIME_FORMATTER = DateTimeFormatter.ISO_LOCAL_DATE_TIME;

    private final InMemoryRouteTaskRepository repository;
    private final AlgorithmClient algorithmClient;
    private final SkyGridClient skyGridClient;
    private final AtomicLong planIdSequence = new AtomicLong(1);

    public RouteTaskService(
            InMemoryRouteTaskRepository repository,
            AlgorithmClient algorithmClient,
            SkyGridClient skyGridClient
    ) {
        this.repository = repository;
        this.algorithmClient = algorithmClient;
        this.skyGridClient = skyGridClient;
    }

    public RouteTaskResponse createTask(CreateRouteTaskRequest request) {
        return RouteTaskResponse.from(repository.create(request));
    }

    public RouteTaskResponse getTask(long taskId) {
        return RouteTaskResponse.from(requireTask(taskId));
    }

    public RouteTaskResponse planTask(long taskId) {
        RouteTask task = requireTask(taskId);
        AlgorithmPlanResult planResult = algorithmClient.plan(new AlgorithmPlanRequest(
                task.mapId(),
                task.taskType(),
                task.startGrid(),
                task.endGrid(),
                task.startLevel(),
                task.algorithm(),
                task.avoidRisk(),
                task.allowDiagonal()
        ));

        RoutePlanSnapshot plan = RoutePlanSnapshot.from(planIdSequence.getAndIncrement(), planResult);
        List<TimeSlotConvertResult.OccupancyUnit> occupancyUnits = List.of();

        if (planResult.success() && planResult.path() != null && !planResult.path().isEmpty()) {
            occupancyUnits = algorithmClient.convertTimeSlot(new TimeSlotConvertRequest(
                    planResult.path(),
                    task.startLevel(),
                    DATE_TIME_FORMATTER.format(task.startTime()),
                    task.speedMps(),
                    task.gridSizeMeters(),
                    task.slotMinutes()
            )).occupancyUnits();
        }

        task.markPlanned(plan, occupancyUnits);
        return RouteTaskResponse.from(task);
    }

    public ConflictCheckResult checkConflict(long taskId) {
        RouteTask task = requireTask(taskId);
        requireSuccessfulPlan(task);
        ConflictCheckResult result = skyGridClient.checkConflict(task.occupancyUnits());
        task.markConflictChecked(result);
        return result;
    }

    public SkyGridSubmitResult submitSkyGrid(long taskId) {
        RouteTask task = requireTask(taskId);
        requireSuccessfulPlan(task);
        SkyGridSubmitResult result = skyGridClient.submitBooking(
                task.id(),
                task.plan().id(),
                task.occupancyUnits()
        );
        task.markSubmitted(result);
        return result;
    }

    private RouteTask requireTask(long taskId) {
        return repository.findById(taskId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "route task not found: " + taskId));
    }

    private static void requireSuccessfulPlan(RouteTask task) {
        if (task.plan() == null || !task.plan().success()) {
            throw new ResponseStatusException(
                    HttpStatus.CONFLICT,
                    "task must have a successful plan before this operation"
            );
        }
    }
}

