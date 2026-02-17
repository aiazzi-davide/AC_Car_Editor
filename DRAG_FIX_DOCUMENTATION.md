# Curve Editor Fix - Prevent Graph Movement During Drag

## Issue

**Italian:** "se trascino un punto e lo muovo al bordo il grafico si muove e cambia forma, questo non deve succedere"

**English:** When dragging a point to the edge of the visible area, the graph would move and change shape, which should not happen.

## Root Cause

When a point is dragged during editing, the `plot_curve()` method is called repeatedly to update the visualization. This method:

1. Calls `ax.clear()` to reset the plot
2. Redraws all points and curves
3. Matplotlib automatically adjusts axis limits based on the data

When a point is dragged near the edge of the plot, matplotlib's auto-scaling would kick in, causing the entire view to shift or zoom to accommodate the new point position. This was disorienting for users who were trying to precisely position points.

## Solution

The fix implements axis limit preservation during drag operations:

### 1. Store Axis Limits on Drag Start

When the user clicks on a point to start dragging (in `on_mouse_press()`):
```python
# Store current axis limits to prevent auto-scaling during drag
self.drag_axis_limits = {
    'xlim': self.ax.get_xlim(),
    'ylim': self.ax.get_ylim()
}
```

### 2. Restore Limits During Drag

In the `plot_curve()` method, after redrawing:
```python
# Restore axis limits if dragging to prevent auto-scaling
if self.drag_axis_limits is not None:
    self.ax.set_xlim(self.drag_axis_limits['xlim'])
    self.ax.set_ylim(self.drag_axis_limits['ylim'])
```

### 3. Clear Limits on Drag End

When the user releases the mouse button (in `on_mouse_release()`):
```python
self.drag_axis_limits = None  # Clear stored limits after drag completes
```

## Code Changes

**File:** `src/gui/curve_editor_widget.py`

**Lines modified:**
- Line 43: Added `self.drag_axis_limits = None` instance variable
- Lines 238-242: Store axis limits when drag starts
- Lines 199-202: Restore axis limits during drag
- Line 257: Clear stored limits when drag ends

## Behavior

### Before Fix
1. User clicks and drags point toward edge
2. Graph auto-scales to fit new point position
3. View shifts/zooms unexpectedly
4. User loses context of where they are on the graph

### After Fix
1. User clicks point → Current view is locked
2. User drags point anywhere (including to edge)
3. View remains stable and fixed
4. User releases point → View unlocks, returns to normal
5. Normal auto-scaling resumes for other operations

## Testing

All existing tests continue to pass (37/37):
- The fix is transparent to the API
- No changes needed to test cases
- Behavior is UI-only

## Edge Cases Handled

1. **Drag beyond visible area**: View stays locked at original limits
2. **Multiple rapid drags**: Each drag gets fresh limits
3. **Cancelled drag**: Limits are cleared on release regardless
4. **Zoom during drag**: Not possible (toolbar disabled during drag)

## User Experience

The fix provides a stable, predictable editing experience:
- Users can confidently drag points to any position
- The graph context remains consistent
- No unexpected view changes distract from the editing task
- More precise point positioning is possible

## Related Features

This fix works in conjunction with other curve editor improvements:
- Toolbar mode disabled during drag (prevents pan conflicts)
- Integer-only values (prevents sub-pixel jitter)
- Mouse wheel zoom (still works normally when not dragging)
- Keyboard zoom (+/-) (still works normally when not dragging)

## Future Enhancements

Potential improvements that could build on this fix:
1. Option to extend graph limits if dragging beyond edge
2. Visual indicator when dragging near limits
3. Snap-to-grid during drag for even more precision
4. Animation to smoothly adjust view after drag completes
