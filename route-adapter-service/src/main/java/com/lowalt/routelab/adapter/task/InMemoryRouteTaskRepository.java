package com.lowalt.routelab.adapter.task;

import org.springframework.stereotype.Repository;

import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

@Repository
public class InMemoryRouteTaskRepository {

    private final AtomicLong taskIdSequence = new AtomicLong(1);
    private final ConcurrentHashMap<Long, RouteTask> tasks = new ConcurrentHashMap<>();

    public RouteTask create(CreateRouteTaskRequest request) {
        RouteTask task = new RouteTask(taskIdSequence.getAndIncrement(), request);
        tasks.put(task.id(), task);
        return task;
    }

    public Optional<RouteTask> findById(long id) {
        return Optional.ofNullable(tasks.get(id));
    }
}

