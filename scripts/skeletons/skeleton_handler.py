import glm
from scripts.skeletons.joints import *
from scripts.nodes.node import Node

class SkeletonHandler():
    def __init__(self, scene, skeletons:list=None):
        self.scene     = scene
        self.skeletons = skeletons if skeletons else [] # contains root bones
        
    def update(self, delta_time:float):
        """
        Updates all the skeletons on the top level/root list. 
        """
        for bone in self.skeletons: bone.update(delta_time)
        
    def add(self, node, joints=None):
        """
        Creates a skeleton and adds it to the top level list. 
        """
        bone = Bone(self, node, joints)
        self.skeletons.append(bone)
        return bone
        
    def create(self, node, joints=None):
        """
        Creates the skeleton and returns it but does not add it to the top level list. 
        """
        return Bone(self, node, joints)

class Bone():
    def __init__(self, skeleton_handler, node, joints=None) -> None:
        self.skeleton_handler  = skeleton_handler
        self.node              = node
        self.original_inv_quat = glm.inverse(glm.quat(self.node.rotation))
        self.joints            = joints if joints else [] # skeleton, joint
        
    def restrict_bones(self, delta_time:float) -> None:
        """
        Restricts the chlid bones based on their respective joints. Also adds spring forces
        """
        # gets difference in rotations and applies to joints
        rotation = glm.quat(self.node.rotation) * self.original_inv_quat # TODO may be causing ginble lock
        for joint in self.joints: joint.rotate_parent_offset(rotation)
        
        for joint in self.joints:
            rotation = glm.quat(joint.child_bone.node.rotation) * joint.child_bone.original_inv_quat # TODO may be causing ginble lock
            joint.rotate_child_offset(rotation)
            
            
        # apply restrictions
        for joint in self.joints: joint.restrict(self.node, joint.child_bone.node, delta_time)
            
    def update(self, delta_time:float):
        """
        Restricts bones and restricts children from joints. 
        """
        self.restrict_bones(delta_time)
        for joint in self.joints: joint.child_bone.update(delta_time)