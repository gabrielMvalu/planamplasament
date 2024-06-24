from shapely.geometry import box

def is_rect_inside_polygon(rect, polygon):
    rect_box = box(rect[0], rect[1], rect[0] + rect[2], rect[1] + rect[3])
    return polygon.contains(rect_box)

def is_rect_overlap(rect1, rect2):
    rect1_box = box(rect1[0], rect1[1], rect1[0] + rect1[2], rect1[1] + rect1[3])
    rect2_box = box(rect2[0], rect2[1], rect2[0] + rect2[2], rect2[1] + rect2[3])
    return rect1_box.intersects(rect2_box)
