package com.lowalt.routelab.adapter.skygrid;

public record ConflictResolutionSuggestion(
        String conflictId,
        String conflictType,
        String gridId,
        String levelId,
        String timeSlotId,
        String suggestedAction,
        String suggestion
) {
}
