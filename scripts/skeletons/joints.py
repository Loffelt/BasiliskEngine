import glm
from scripts.nodes.node import Node
from scripts.skeletons.animation import Animation

# child free to move within radius, child must point at offset
class BallJoint(): 
    def __init__(self, child_bone, parent_offset:glm.vec3, child_offset:glm.vec3, spring_constant:float=1e5, fixed=False): # parent and child not saved for splitting
        # child bone
        self.child_bone = child_bone
        
        # rigging
        self.fixed = fixed
        self.animations : list[Animation] = [] # animation queue
        
        # offsets from node position
        self.parent_offset          = glm.vec3(parent_offset)
        self.original_parent_offset = glm.vec3(parent_offset)
        self.child_offset           = glm.vec3(child_offset)
        self.original_child_offset  = glm.vec3(child_offset)
        
        self.original_child_rotation = glm.inverse(glm.quat(self.child_bone.node.rotation)) # TODO remove if unused
        
        # spring 
        self.spring_constant = spring_constant
        
    def animate(self, child:Node, delta_time:float) -> glm.vec3:
        """
        Applies the force required for an animation on a child
        """
        # gets animation data
        if len(self.animations) == 0: return # no animation queued
        if not self.animations[0].is_running: self.animations[0].is_running = True
        position, rotation, time_remaining = self.animations[0].get_key_frame()
        self.animations[0].update(delta_time)
        if not self.animations[0].is_running: self.animations.pop(0)
        
        if not child.physics_body or time_remaining < 1e-2: return
        # get constant forces from physics engine
        if position:
            velocity = (position - child.position) / time_remaining
            child.physics_body.velocity = velocity
        
        if rotation:
            if glm.dot(rotation, child.physics_body.rotation) < 0: rotation *= -1
            diff_quat = glm.inverse(rotation) * child.physics_body.rotation #glm.slerp(child.physics_body.rotation, rotation, time_remaining)
            angle, axis = glm.angle(diff_quat) / time_remaining, glm.axis(diff_quat)
            
            child.physics_body.rotational_velocity = angle
            child.physics_body.axis_of_rotation = axis
        
    def restrict(self, parent:Node, child:Node, delta_time:float) -> glm.vec3:
        """
        Restricts the child to the parent
        """
        
        # calculate offset information
        origin       = parent.position + self.parent_offset
        child_point  = child.position + self.child_offset
        displacement = child_point - origin
        
        # quick restrict if fixed
        if self.fixed:
            child.position = origin - self.child_offset
            # print(self.parent_offset, parent.position)
            return glm.vec3(0, 0, 0)
        
        magnitude = glm.length(displacement)
        if magnitude < 1e-7: return # no movement needed
        
        direction = glm.normalize(displacement)
        
        def spring_force(cpos:glm.vec3, cvel:glm.vec3, ppos:glm.vec3, pvel:glm.vec3):
            
            displacement = cpos + self.child_offset - ppos - self.parent_offset
            
            mass = child.physics_body.mass # * parent.physics_body.mass / (child.physics_body.mass + parent.physics_body.mass) if parent.physics_body else child.physics_body.mass
            
            # dampening force
            relative_velocity = cvel - pvel
            relative_velocity = glm.dot(direction, relative_velocity)
            c = 2 * glm.sqrt(self.spring_constant * mass)
            
            return (-c * cvel - self.spring_constant * displacement) / mass
        
        # if the node has a physics body do thi
        if child.physics_body and delta_time < 0.022:
            
            cpos, cvel, ppos, pvel = child.position, child.physics_body.velocity, parent.position, parent.physics_body.velocity if parent.physics_body else glm.vec3(0.0)
            
            k1_pos = cvel
            k1_vel = spring_force(cpos, cvel, ppos, pvel)
            k2_pos = cvel + 0.5 * delta_time * k1_vel
            k2_vel = spring_force(cpos + 0.5 * delta_time * k1_pos, cvel + 0.5 * delta_time * k1_vel, ppos, pvel)
            k3_pos = cvel + 0.5 * delta_time * k2_vel
            k3_vel = spring_force(cpos + 0.5 * delta_time * k2_pos, cvel + 0.5 * delta_time * k2_vel, ppos, pvel)
            k4_pos = cvel + 0.5 * delta_time * k3_vel
            k4_vel = spring_force(cpos + 0.5 * delta_time * k3_pos, cvel + 0.5 * delta_time * k3_vel, ppos, pvel)
            
            deno = 6#12 if parent.physics_body and not self.fixed else 6
            child.position += delta_time * (k1_pos + 2 * k2_pos + 2 * k3_pos + k4_pos) / deno
            child.physics_body.velocity += delta_time * (k1_vel + 2 * k2_vel + 2 * k3_vel + k4_vel) / deno
            # if parent.physics_body and not self.fixed:
            #     parent.position -= delta_time * (k1_pos + 2 * k2_pos + 2 * k3_pos + k4_pos) / deno
            #     parent.physics_body.velocity -= delta_time * (k1_vel + 2 * k2_vel + 2 * k3_vel + k4_vel) / deno
                
            return glm.vec3(0.0) # TODO get spring force
            
        # snap to position if it does not
        else: 
            child.position -= displacement
            if child.physics_body: child.physics_body.velocity[1] = parent.physics_body.velocity[1] if parent.physics_body else 0
            
            return glm.vec3(0.0)
    
    def rotate_parent_offset(self, rotation:glm.quat):
        """
        Rotate the original parent offset point by the given rotation
        """
        rotated_quat = glm.inverse(rotation) * glm.quat(0, *self.original_parent_offset) * rotation
        self.parent_offset = glm.vec3(rotated_quat.x, rotated_quat.y, rotated_quat.z)
        
    def rotate_child_offset(self, rotation:glm.quat):
        """
        Rotate the original child offset point by the given rotation
        """
        rotated_quat = glm.inverse(rotation) * glm.quat(0, *self.original_child_offset) * rotation
        self.child_offset = glm.vec3(rotated_quat.x, rotated_quat.y, rotated_quat.z)
        
# child is locked in place but can rotate on given axis
class RotatorJoint(BallJoint):
    def __init__(self, child_bone, parent_offset:glm.vec3, child_offset:glm.vec3, spring_constant:float=1e5, fixed=False):
        super().__init__(child_bone, parent_offset, child_offset, spring_constant, fixed)
        
    def restrict(self, parent, child, delta_time:float): # TODO watch, mat casuse gimble lock
        """
        Restrict face axis to parent offset then ball joint restrict
        """
        # apply spring forces 
        super().restrict(parent, child, delta_time)  
        
        # calculate axis angle
        normal_parent, normal_child = glm.normalize(self.parent_offset), glm.normalize(self.child_offset)
        axis  = glm.cross(normal_parent, normal_child)
        
        if glm.length(axis) < 1e-6: return
        theta = glm.acos(glm.clamp(glm.dot(normal_child, normal_parent), -1, 1))
        
        # compute effective torque
        torque  = self.spring_constant * theta * axis
        torque -= normal_child * glm.dot(torque, normal_child)
        
        # apply torque
        child.apply_torque(torque, delta_time)
        
# child free to move within radius but can only rotate on given axis TODO test and debug
class HingeJoint(BallJoint):
    def __init__(self, child_bone, parent_offset:glm.vec3, child_offset:glm.vec3, spring_constant:float=1e5, axis:glm.vec3=None, fixed=False):
        super().__init__(child_bone, parent_offset, child_offset, spring_constant, fixed)
        self.axis = glm.normalize(axis) if glm.length(axis) > 1e-7 else glm.vec3(0, 1, 0)
        self.original_axis = glm.vec3(axis)
        
    def rotate_parent_offset(self, rotation: glm.quat):
        """
        Rotate the parent offset and axis. 
        """
        super().rotate_parent_offset(rotation)
        
        rotated_quat = glm.inverse(rotation) * glm.quat(0, *self.original_axis) * rotation
        self.axis    = glm.vec3(rotated_quat.x, rotated_quat.y, rotated_quat.z)
        
        if glm.length(self.axis) < 1e-7: self.axis = glm.vec3(0, 1, 0)
        else: self.axis = glm.normalize(self.axis)
        
    def restrict(self, parent, child, delta_time:float):
        """
        Restrict joint by ball spring, then align with parent axis. 
        """
        super().restrict(parent, child, delta_time)
        
        # get target quaternion
        child_proj  = self.child_offset - glm.dot(self.child_offset, self.axis) * self.axis
        parent_proj = self.parent_offset - glm.dot(self.parent_offset, self.axis) * self.axis
        
        axis  = glm.cross(child_proj, parent_proj)
        angle = glm.acos(abs(glm.dot(child_proj, parent_proj)))
        
        target = glm.angleAxis(angle, axis)

        # get projected chlid omega
        error_quat  = glm.inverse(target) * glm.quat(0, *self.child_offset)
        axis, angle = glm.axis(error_quat), glm.angle(error_quat)
        
        # get torque
        torque  = self.spring_constant * angle * axis
        torque -= glm.dot(torque, self.axis) * self.axis
        
        child.apply_torque(torque, delta_time)

# child cannot move or be rotated. ex pistons
class PistonJoint(BallJoint):
    def __init__(self, child_bone, parent_offset:glm.vec3, child_offset:glm.vec3, spring_constant:float=1e5, fixed=False):
        super().__init__(child_bone, parent_offset, child_offset, spring_constant, fixed)