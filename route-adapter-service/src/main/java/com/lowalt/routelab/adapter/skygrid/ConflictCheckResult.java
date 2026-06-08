package com.lowalt.routelab.adapter.skygrid;

import java.util.List;

public record ConflictCheckResult(
        String conflictStatus,
        int conflictCount,
        List<ConflictItem> conflicts
) {
    public record ConflictItem(
            String gridId,
            String levelId,
            String slotStart,
            String slotEnd,
            String conflictType,
            String description
    ) {
    }
}

