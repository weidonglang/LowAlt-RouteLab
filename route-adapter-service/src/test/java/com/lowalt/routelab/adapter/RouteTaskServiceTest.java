package com.lowalt.routelab.adapter;

import com.lowalt.routelab.adapter.algorithm.AlgorithmClient;
import com.lowalt.routelab.adapter.algorithm.AlgorithmPlanRequest;
import com.lowalt.routelab.adapter.algorithm.AlgorithmPlanResult;
import com.lowalt.routelab.adapter.algorithm.TimeSlotConvertRequest;
import com.lowalt.routelab.adapter.algorithm.TimeSlotConvertResult;
import com.lowalt.routelab.adapter.skygrid.ConflictCheckResult;
import com.lowalt.routelab.adapter.skygrid.MockSkyGridClient;
import com.lowalt.routelab.adapter.skygrid.SkyGridSubmitResult;
import com.lowalt.routelab.adapter.task.CreateRouteTaskRequest;
import com.lowalt.routelab.adapter.task.InMemoryRouteTaskRepository;
import com.lowalt.routelab.adapter.task.RouteTaskResponse;
import com.lowalt.routelab.adapter.task.RouteTaskService;
import org.junit.jupiter.api.Test;

import java.time.LocalDateTime;
import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

class RouteTaskServiceTest {

    @Test
    void createTaskUsesDefaults() {
        RouteTaskService service = serviceWithMockAlgorithmClient(mock(AlgorithmClient.class));

        RouteTaskResponse response = service.createTask(createRequest());

        assertThat(response.id()).isEqualTo(1);
        assertThat(response.mapId()).isEqualTo("demo-city-20x20");
        assertThat(response.algorithm()).isEqualTo("A_STAR");
        assertThat(response.status()).isEqualTo("CREATED");
        assertThat(response.speedMps()).isEqualTo(10.0);
    }

    @Test
    void planTaskCallsAlgorithmAndConvertsTimeslots() {
        AlgorithmClient algorithmClient = mock(AlgorithmClient.class);
        when(algorithmClient.plan(any(AlgorithmPlanRequest.class))).thenReturn(planResult());
        when(algorithmClient.convertTimeSlot(any(TimeSlotConvertRequest.class))).thenReturn(timeSlotResult());
        RouteTaskService service = serviceWithMockAlgorithmClient(algorithmClient);
        RouteTaskResponse created = service.createTask(createRequest());

        RouteTaskResponse planned = service.planTask(created.id());

        assertThat(planned.status()).isEqualTo("PLANNED");
        assertThat(planned.plan()).isNotNull();
        assertThat(planned.plan().algorithm()).isEqualTo("A_STAR");
        assertThat(planned.occupancyUnits()).hasSize(2);
        verify(algorithmClient).plan(any(AlgorithmPlanRequest.class));
        verify(algorithmClient).convertTimeSlot(any(TimeSlotConvertRequest.class));
    }

    @Test
    void checkConflictAndSubmitUseMockSkyGrid() {
        AlgorithmClient algorithmClient = mock(AlgorithmClient.class);
        when(algorithmClient.plan(any(AlgorithmPlanRequest.class))).thenReturn(planResult());
        when(algorithmClient.convertTimeSlot(any(TimeSlotConvertRequest.class))).thenReturn(timeSlotResult());
        RouteTaskService service = serviceWithMockAlgorithmClient(algorithmClient);
        long taskId = service.createTask(createRequest()).id();
        service.planTask(taskId);

        ConflictCheckResult conflict = service.checkConflict(taskId);
        SkyGridSubmitResult submit = service.submitSkyGrid(taskId);
        RouteTaskResponse loaded = service.getTask(taskId);

        assertThat(conflict.conflictStatus()).isEqualTo("RISK_CONFLICT");
        assertThat(conflict.conflictCount()).isEqualTo(1);
        assertThat(submit.bookingStatus()).isEqualTo("MOCK_SUBMITTED");
        assertThat(loaded.status()).isEqualTo("SUBMITTED_TO_SKYGRID");
    }

    private static RouteTaskService serviceWithMockAlgorithmClient(AlgorithmClient algorithmClient) {
        return new RouteTaskService(
                new InMemoryRouteTaskRepository(),
                algorithmClient,
                new MockSkyGridClient()
        );
    }

    private static CreateRouteTaskRequest createRequest() {
        return new CreateRouteTaskRequest(
                "demo task",
                "POWER_LINE_INSPECTION",
                null,
                "G-01-01",
                "G-18-16",
                "L120",
                "M30",
                null,
                true,
                true,
                true,
                LocalDateTime.of(2026, 6, 8, 10, 0),
                null,
                null,
                null
        );
    }

    private static AlgorithmPlanResult planResult() {
        return new AlgorithmPlanResult(
                true,
                "A_STAR",
                List.of("G-01-01", "G-01-02"),
                100.0,
                10,
                0,
                2,
                4,
                0.12,
                "LOW",
                List.of("no risk-zone grid detected on current path"),
                1.0,
                80.0,
                true,
                null
        );
    }

    private static TimeSlotConvertResult timeSlotResult() {
        return new TimeSlotConvertResult(List.of(
                new TimeSlotConvertResult.OccupancyUnit(
                        "G-01-01",
                        "L120",
                        "2026-06-08T10:00:00",
                        "2026-06-08T10:05:00",
                        1
                ),
                new TimeSlotConvertResult.OccupancyUnit(
                        "G-01-02",
                        "L120",
                        "2026-06-08T10:00:00",
                        "2026-06-08T10:05:00",
                        2
                )
        ));
    }
}

