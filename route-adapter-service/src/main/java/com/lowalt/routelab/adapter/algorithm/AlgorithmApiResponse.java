package com.lowalt.routelab.adapter.algorithm;

public record AlgorithmApiResponse<T>(
        int code,
        String message,
        T data
) {
}

