import glm


class AbstractAABB():
    top_right: glm.vec3
    """The furthest positive corner of the AABB"""
    bottom_left: glm.vec3
    """The furthest negative corner of the AABB"""
    a: ...
    """Binary child 1"""
    b: ...
    """Binary child 2"""
        
class AbstractBVH():
    root: AbstractAABB
    """Root aabb used for the start of all collisions"""
    
    def add(self) -> None: ...
    
    def remove(self, obj: AbstractAABB) -> None: ...
    
    def rotate(self) -> None: ...
    
    def build(self) -> None: ...
    
    def get(self) -> AbstractAABB: ...