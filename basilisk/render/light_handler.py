import moderngl as mgl
import glm
from ..render.light import DirectionalLight


class LightHandler():
    engine: ...
    """Back reference to the parent engine"""
    scene: ...
    """Back reference to the parent scene"""
    ctx: mgl.Context
    """Back reference to the parent context"""
    directional_light: DirectionalLight
    """The directional light of the scene"""
    point_lights: list
    """List of all the point lights in the scene"""

    def __init__(self, scene) -> None:
        """
        Handles all the lights in a Basilisk scene.
        """

        # Back references
        self.scene  = scene
        self.engine = scene.engine
        self.ctx    = scene.engine.ctx

        # Intialize light variables
        self.directional_light = None
        self.directional_light = DirectionalLight(self)
        self.point_lights      = []

        # Initalize uniforms
        self.write()

    def write(self, program: mgl.Program=None, directional=True, point=False) -> None:
        """
        Writes all the lights in a scene to the given shader program
        """

        if not program: program = self.scene.shader_handler.programs['batch']

        if directional and self.directional_light:
            program['dirLight.direction'].write(self.directional_light.direction)
            program['dirLight.intensity'].write(glm.float32(self.directional_light.intensity))
            program['dirLight.color'    ].write(self.directional_light.color / 255.0)
            program['dirLight.ambient'  ].write(glm.float32(self.directional_light.ambient))
        
        if point:
            ...