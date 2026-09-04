"""
ExamHub Hotspot Question Engine
Determines whether candidate click coordinates fall inside an arbitrary target polygon on an image.
"""

from typing import List
from backend.app.question_engines.schemas import (
    Point2D,
    HotspotGradingRequest,
    HotspotGradingResponse,
)


class HotspotEngine:
    """
    Ray-casting algorithm to test point-in-polygon containment for hotspot questions.
    """

    @classmethod
    def point_in_polygon(cls, point: Point2D, polygon: List[Point2D]) -> bool:
        """
        Ray-casting algorithm: Cast ray to the right from point (x, y)
        and count intersections with polygon edges. Odd count = inside, Even = outside.
        """
        x = point.x
        y = point.y
        n = len(polygon)
        if n < 3:
            return False

        inside = False
        p1 = polygon[0]

        for i in range(1, n + 1):
            p2 = polygon[i % n]
            if y > min(p1.y, p2.y):
                if y <= max(p1.y, p2.y):
                    if x <= max(p1.x, p2.x):
                        if p1.y != p2.y:
                            x_inters = (y - p1.y) * (p2.x - p1.x) / (p2.y - p1.y) + p1.x
                        if p1.x == p2.x or x <= x_inters:
                            inside = not inside
            p1 = p2

        return inside

    @classmethod
    def evaluate(cls, req: HotspotGradingRequest) -> HotspotGradingResponse:
        is_hit = cls.point_in_polygon(req.click_point, req.target_polygon)
        return HotspotGradingResponse(
            is_hit=is_hit,
            score=1.0 if is_hit else 0.0,
            click_coordinates=req.click_point
        )
