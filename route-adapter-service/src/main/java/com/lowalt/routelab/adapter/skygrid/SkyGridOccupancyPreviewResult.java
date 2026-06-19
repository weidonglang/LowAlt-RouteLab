package com.lowalt.routelab.adapter.skygrid;

public record SkyGridOccupancyPreviewResult(
        String previewStatus,
        int occupancyCount,
        String message
) {
}
