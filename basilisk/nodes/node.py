import glm
import numpy as np
from ..render.mesh import Mesh
from ..render.material import Material
from ..physics.physics_body import PhysicsBody
from ..collisions.collider import Collider

class Node():
    position: glm.vec3
    """The position of the node in meters with swizzle xyz"""
    scale: glm.vec3
    """The scale of the node in meters in each direction"""
    rotation: glm.quat
    """The rotation of the node"""
    forward: glm.vec3
    """The forward facing vector of the node"""
    mesh: Mesh
    """The mesh of the node stored as a basilisk mesh object"""
    material: Material
    """The mesh of the node stored as a basilisk material object"""
    velocity: glm.vec3
    """The translational velocity of the node"""
    rotational_velocity: glm.quat 
    """The rotational velocity of the node"""
    physics: bool
    """Allows the node's movement to be affected by the physics engine and collisions"""
    mass: float
    """The mass of the node in kg"""
    collisions: bool
    """Gives the node collision with other nodes in the scene""" 
    collider: str
    """The collider type of the node. Can be either 'box' or 'mesh'"""
    static_friction: float
    """Determines the friction of the node when still: recommended value 0.0 - 1.0"""
    kinetic_friction: float
    """Determines the friction of the node when moving: recommended value 0.0 - 1.0"""  
    elasticity: float
    """Determines how bouncy an object is: recommended value 0.0 - 1.0"""
    collision_group: str
    """Nodes of the same collision group do not collide with each other"""
    name: str
    """The name of the node for reference"""  
    tags: list[str]
    """Tags are used to sort nodes into separate groups"""
    children: list
    """List of nodes that this node is a parent of"""

    def __init__(self, 
            position: glm.vec3=None, 
            scale: glm.vec3=None, 
            rotation: glm.quat=None, 
            forward: glm.vec3=None, 
            mesh: Mesh=None, 
            material: None=None, 
            velocity: glm.vec3=None, 
            rotational_velocity: glm.quat=None, 
            physics: bool=False, 
            mass: float=None, 
            collisions: bool=False, 
            collider: str=None, 
            static_friction: float=None, 
            kinetic_friction: float=None, 
            elasticity: float=None, 
            collision_group :float=None, 
            name: str='', 
            tags: list[str]=None
        ) -> None:
        """
        Basilisk node object. 
        Contains mesh data, translation, material, physics, collider, and descriptive information. 
        Base building block for populating a Basilisk scene.
        """
        
        self.position = position if position else glm.vec3(0, 0, 0)
        self.scale    = scale    if scale    else glm.vec3(1, 1, 1)
        self.rotation = rotation if rotation else glm.quat(1, 0, 0, 0)
        self.forward  = forward  if forward  else glm.vec3(1, 0, 0)
        self.mesh     = mesh     if mesh     else None # TODO add default cube mesh
        self.material = material if material else None # TODO add default base material
        self.velocity = velocity if velocity else glm.vec3(0, 0, 0)
        self.rotational_velocity = rotational_velocity if rotational_velocity else glm.quat(1, 0, 0, 0)
        
        if physics: self.physics_body: PhysicsBody = PhysicsBody(mass = mass)
        elif mass: raise ValueError('Node cannot have mass if it does not have physics')
        else: self.physics_body = None
        
        if collisions: self.collider: Collider = ...
        elif collider:         raise ValueError('Node cannot have collider mesh if it does not allow collisions')
        elif static_friction:  raise ValueError('Node cannot have static friction if it does not allow collisions')
        elif kinetic_friction: raise ValueError('Node cannot have kinetic friction if it does not allow collisions')
        elif elasticity:       raise ValueError('Node cannot have elasticity if it does not allow collisions')
        elif collision_group:  raise ValueError('Node cannot have collider group if it does not allow collisions')
        else: self.collider = None
        
        self.name = name
        self.tags = tags if tags else []
        self.children = []

    def __repr__(self) -> str:
        """
        Returns a string representation of the node
        """

        return f'<Bailisk Node | {self.name}, {self.mesh}, ({self.position})>'
    
    @property
    def position(self): return self._position
    @property
    def scale(self):    return self._scale
    @property
    def rotation(self): return self._rotation
    @property
    def forward(self):  return self._forward
    # TODO add property for Mesh
    # TODO add property for Material
    @property
    def velocity(self): return self._velocity
    @property
    def rotational_velocity(self): return self._rotational_velocity
    @property
    def mass(self): 
        if self.physics_body: return self.physics_body.mass
        raise RuntimeError('Node: Cannot access the mass of a node that has no physics body')
    @property
    def static_friction(self):
        if self.collider: return self.collider.static_friction
        raise RuntimeError('Node: Cannot access the static friction of a node that has no collider')
    @property
    def kinetic_friction(self):
        if self.collider: return self.collider.kinetic_friction
        raise RuntimeError('Node: Cannot access the kinetic friction of a node that has no collider')
    @property
    def elasticity(self):
        if self.collider: return self.collider.elasticity
        raise RuntimeError('Node: Cannot access the elasticity of a node that has no collider')
    @property
    def collision_group(self):
        if self.collider: return self.collider.collision_group
        raise RuntimeError('Node: Cannot access the collision_group of a node that has no collider')
    @property
    def name(self): return self._name
    @property
    def tags(self): return self._tags
    @property
    def x(self): return self._position.x # TODO test these functions
    @property
    def y(self): return self._position.y
    @property
    def z(self): return self._position.z
    
    @position.setter
    def position(self, value: tuple | list | glm.vec3 | np.ndarray):
        if isinstance(value, glm.vec3): self._position = glm.vec3(value)
        elif isinstance(value, tuple) or isinstance(value, list) or isinstance(value, np.ndarray):
            if len(value) != 3: raise ValueError(f'Node: Invalid number of values for position. Expected 3, got {len(value)}')
            self._position = glm.vec3(value)
        else: raise TypeError(f'Node: Invalid position value type {type(value)}')
    
    @scale.setter
    def scale(self, value: tuple | list | glm.vec3 | np.ndarray):
        if isinstance(value, glm.vec3): self._scale = glm.vec3(value)
        elif isinstance(value, tuple) or isinstance(value, list) or isinstance(value, np.ndarray):
            if len(value) != 3: raise ValueError(f'Node: Invalid number of values for scale. Expected 3, got {len(value)}')
            self._scale = glm.vec3(value)
        else: raise TypeError(f'Node: Invalid scale value type {type(value)}')
        
    @rotation.setter
    def rotation(self, value: tuple | list | glm.vec3 | glm.quat | glm.vec4 | np.ndarray):
        if isinstance(value, glm.quat) or isinstance(value, glm.vec4) or isinstance(value, glm.vec3): self._rotation = glm.quat(value)
        elif isinstance(value, tuple) or isinstance(value, list) or isinstance(value, np.ndarray):
            if len(value) == 3: self._rotation = glm.quat(glm.vec3(*value))
            elif len(value) == 4: self._rotation = glm.quat(*value)
            else: raise ValueError(f'Node: Invalid number of values for rotation. Expected 3 or 4, got {len(value)}')
        else: raise TypeError(f'Node: Invalid rotation value type {type(value)}')
        
    @forward.setter
    def forward(self, value: tuple | list | glm.vec3 | np.ndarray):
        if isinstance(value, glm.vec3): self._forward = glm.vec3(value)
        elif isinstance(value, tuple) or isinstance(value, list) or isinstance(value, np.ndarray):
            if len(value) != 3: raise ValueError(f'Node: Invalid number of values for forward. Expected 3, got {len(value)}')
            self._forward = glm.vec3(value)
        else: raise TypeError(f'Node: Invalid forward value type {type(value)}')
        
    # TODO add setter for Mesh
    
    # TODO add setter for Material
    
    @velocity.setter
    def velocity(self, value: tuple | list | glm.vec3 | np.ndarray):
        if isinstance(value, glm.vec3): self._velocity = glm.vec3(value)
        elif isinstance(value, tuple) or isinstance(value, list) or isinstance(value, np.ndarray):
            if len(value) != 3: raise ValueError(f'Node: Invalid number of values for velocity. Expected 3, got {len(value)}')
            self._velocity = glm.vec3(value)
        else: raise TypeError(f'Node: Invalid velocity value type {type(value)}')
        
    @rotational_velocity.setter
    def rotational_velocity(self, value: tuple | list | glm.vec3 | glm.quat | glm.vec4 | np.ndarray):
        if isinstance(value, glm.quat) or isinstance(value, glm.vec4) or isinstance(value, glm.vec3): self._rotational_velocity = glm.quat(value)
        elif isinstance(value, tuple) or isinstance(value, list) or isinstance(value, np.ndarray):
            if len(value) == 3: self._rotational_velocity = glm.quat(glm.vec3(*value))
            elif len(value) == 4: self._rotational_velocity = glm.quat(*value)
            else: raise ValueError(f'Node: Invalid number of values for rotational velocity. Expected 3 or 4, got {len(value)}')
        else: raise TypeError(f'Node: Invalid rotational velocity value type {type(value)}')
        
    @mass.setter
    def mass(self, value: int | float):
        if not self.physics_body: raise RuntimeError('Node: Cannot set the mass of a node that has no physics body')
        if isinstance(value, int) or isinstance(value, float): self.physics_body.mass = value
        else: raise TypeError(f'Node: Invalid mass value type {type(value)}')
        
    @static_friction.setter
    def static_friction(self, value: int | float):
        if not self.collider: raise RuntimeError('Node: Cannot set the static friction of a node that has no physics body')
        if isinstance(value, int) or isinstance(value, float): self.collider.static_friction = value
        else: raise TypeError(f'Node: Invalid static friction value type {type(value)}')
    
    @kinetic_friction.setter
    def kinetic_friction(self, value: int | float):
        if not self.collider: raise RuntimeError('Node: Cannot set the kinetic friction of a node that has no physics body')
        if isinstance(value, int) or isinstance(value, float): self.collider.kinetic_friction = value
        else: raise TypeError(f'Node: Invalid kinetic friction value type {type(value)}')
        
    @elasticity.setter
    def elasticity(self, value: int | float):
        if not self.collider: raise RuntimeError('Node: Cannot set the elasticity of a node that has no physics body')
        if isinstance(value, int) or isinstance(value, float): self.collider.elasticity = value
        else: raise TypeError(f'Node: Invalid elasticity value type {type(value)}')
        
    @collision_group.setter
    def collision_group(self, value: str):
        if not self.collider: raise RuntimeError('Node: Cannot set the collision gruop of a node that has no physics body')
        if isinstance(value, str): self.collider.collision_group = value
        else: raise TypeError(f'Node: Invalid collision group value type {type(value)}')
        
    @name.setter
    def name(self, value: str):
        if isinstance(value, str): self._name = value
        else: raise TypeError(f'Node: Invalid name value type {type(value)}')
        
    @tags.setter
    def tags(self, value: list[str]):
        if isinstance(value, list) or isinstance(value, tuple):
            for tag in value:
                if not isinstance(tag, str): raise TypeError(f'Node: Invalid tag value in tags list of type {type(tag)}')
            self._tags = value
        else: raise TypeError(f'Node: Invalid tags value type {type(value)}')
        
    @x.setter
    def x(self, value: int | float):
        if isinstance(value, int) or isinstance(value, float): self._position.x = value
        else: raise TypeError(f'Node: Invalid positional x value type {type(value)}')
        
    @y.setter
    def y(self, value: int | float):
        if isinstance(value, int) or isinstance(value, float): self._position.y = value
        else: raise TypeError(f'Node: Invalid positional y value type {type(value)}')
        
    @z.setter
    def z(self, value: int | float):
        if isinstance(value, int) or isinstance(value, float): self._position.z = value
        else: raise TypeError(f'Node: Invalid positional z value type {type(value)}')