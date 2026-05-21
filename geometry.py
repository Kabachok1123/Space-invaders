def clamp(value: float, min_value: float, max_value: float) -> float:
    return max(min_value, min(value, max_value))


def rectangles_intersect(first, second) -> bool:
    return (
        first.x < second.right
        and first.right > second.x
        and first.y < second.bottom
        and first.bottom > second.y
    )


def point_inside_rect(point_x: float, point_y: float, rect) -> bool:
    return rect.x <= point_x <= rect.right and rect.y <= point_y <= rect.bottom


def bullet_path_hits_point(
    start_x: float,
    start_y: float,
    end_x: float,
    end_y: float,
    point_x: float,
    point_y: float,
) -> bool:
    min_x = min(start_x, end_x)
    max_x = max(start_x, end_x)
    min_y = min(start_y, end_y)
    max_y = max(start_y, end_y)
    return min_x <= point_x <= max_x and min_y <= point_y <= max_y
