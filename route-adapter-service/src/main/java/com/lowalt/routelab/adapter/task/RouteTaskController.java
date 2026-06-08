package com.lowalt.routelab.adapter.task;

import com.lowalt.routelab.adapter.common.ApiResponse;
import com.lowalt.routelab.adapter.skygrid.ConflictCheckResult;
import com.lowalt.routelab.adapter.skygrid.SkyGridSubmitResult;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/tasks")
public class RouteTaskController {

    private final RouteTaskService service;

    public RouteTaskController(RouteTaskService service) {
        this.service = service;
    }

    @PostMapping
    public ApiResponse<RouteTaskResponse> createTask(@Valid @RequestBody CreateRouteTaskRequest request) {
        return ApiResponse.success("task created successfully", service.createTask(request));
    }

    @PostMapping("/{taskId}/plan")
    public ApiResponse<RouteTaskResponse> planTask(@PathVariable long taskId) {
        return ApiResponse.success("task planned successfully", service.planTask(taskId));
    }

    @PostMapping("/{taskId}/check-conflict")
    public ApiResponse<ConflictCheckResult> checkConflict(@PathVariable long taskId) {
        return ApiResponse.success("conflict checked successfully", service.checkConflict(taskId));
    }

    @PostMapping("/{taskId}/submit-skygrid")
    public ApiResponse<SkyGridSubmitResult> submitSkyGrid(@PathVariable long taskId) {
        return ApiResponse.success("skygrid submitted successfully", service.submitSkyGrid(taskId));
    }

    @GetMapping("/{taskId}")
    public ApiResponse<RouteTaskResponse> getTask(@PathVariable long taskId) {
        return ApiResponse.success("task loaded successfully", service.getTask(taskId));
    }
}

