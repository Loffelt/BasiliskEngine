import glm
import numpy as np
from ..render.image import Image
from ..generic.input_validation import *

class Material():
    material_handler: ...
    """Back reference to the parent material handler"""
    name: str = None
    """Name of the material"""  
    index: 0
    """Index of the material in the material uniform"""
    
    # Base Material Attributes
    color: glm.vec3 = glm.vec3(255.0, 255.0, 255.0)
    """Color multiplier of the material"""   
    texture: Image = None
    """Key/name of the texture image in the image handler. If the image given does not exist, it must be loaded"""
    normal: Image = None
    """Key/name of the normal image in the image handler. If the image given does not exist, it must be loaded"""
    
    # PBR Material Attributes
    roughness: float
    """The roughness of the material, controlls both the specular and diffuse response"""
    subsurface: float
    """Amount of subsurface scattering the material exhibits. Value in range [0, 1]. Lerps between diffuse and subsurface lobes"""
    sheen: float
    """Amount of sheen the material exhibits. Additive lobe"""
    sheen_tint: glm.vec3 = glm.vec3(255.0, 255.0, 255.0)
    """Tinted color of the sheen lobe. Set to white by default"""
    anisotropic: float
    """The amount of anisotropic behaviour the materials specular lobe exhibits"""
    specular: float
    """The strength of the specular lobe of the material"""
    metallicness: float
    """The metallicness of the material, which dictates how much light the surfaces diffuses"""
    specular_tint: glm.vec3 = glm.vec3(255.0, 255.0, 255.0)
    """Tinted color of the specular lobe. Set to white by default"""
    clearcoat: float
    """Amount of clearcoat the material exhibits. Additive lobe"""
    clearcoat_gloss: float
    """The glossiness of the clearcoat layer. 0 For a satin appearance, 1 for a gloss appearance"""

    def __init__(self, name: str=None, color: tuple=(255.0, 255.0, 255.0), texture: Image=None, normal: Image=None, 
                 roughness: float=0.0, subsurface: float=0.0, sheen: float=0.0, sheen_tint: glm.vec3=glm.vec3(255.0, 255.0, 255.0),
                 anisotropic: float=0.0, specular: float=1.0, metallicness: float=0.0, specular_tint: glm.vec3=glm.vec3(255.0, 255.0, 255.0),
                 clearcoat: float=0.0, clearcoat_gloss: float=0.0) -> None:
        """
        Basilisk Material object. Contains the data and images references used by the material.
        Args:
            name: str
                Identifier to be used by user
            color: tuple
                Base color of the material. Applies to textures as well
            texture: Basilisk Image
                The albedo map (color texture) of the material
            normal: Basilisk Image
                The normal map of the material.
        """

        # Set handler only when used by a scene
        self.material_handler = None
        
        self.index = 0
        
        self.name            = name if name else ''
        self.color           = color
        self.texture         = texture
        self.normal          = normal
        self.roughness       = roughness
        self.subsurface      = subsurface
        self.sheen           = sheen
        self.sheen_tint      = sheen_tint
        self.anisotropic     = anisotropic
        self.specular        = specular
        self.metallicness    = metallicness
        self.specular_tint   = specular_tint
        self.clearcoat       = clearcoat
        self.clearcoat_gloss = clearcoat_gloss

    def get_data(self) -> list:
        """
        Returns a list containing all the gpu data in the material.
        Used by the material handler
        """

        # Add color and PBR data
        data = [self.color.x         / 255.0, self.color.y         / 255.0, self.color.z         / 255.0, self.roughness,   self.subsurface, self.sheen,
                self.sheen_tint.x    / 255.0, self.sheen_tint.y    / 255.0, self.sheen_tint.z    / 255.0, self.anisotropic, self.specular,   self.metallicness,
                self.specular_tint.x / 255.0, self.specular_tint.y / 255.0, self.specular_tint.z / 255.0, self.clearcoat,   self.clearcoat_gloss]
        
        # Add texture data
        if self.texture: data.extend([1, self.texture.index.x, self.texture.index.y])
        else: data.extend([0, 0, 0])

        # Add normal data
        if self.normal: data.extend([1, self.normal.index.x, self.normal.index.y])
        else: data.extend([0, 0, 0])

        return data

    def __repr__(self) -> str:
        return f'<Basilisk Material | {self.name}, ({self.color.x}, {self.color.y}, {self.color.z}), {self.texture}>'


    @property
    def color(self):           return self._color
    @property
    def texture(self):         return self._texture
    @property
    def normal(self):          return self._normal
    @property
    def roughness(self):       return self._roughness
    @property
    def subsurface(self):      return self._subsurface
    @property
    def sheen(self):           return self._sheen
    @property
    def sheen_tint(self):      return self._sheen_tint
    @property
    def anisotropic(self):     return self._anisotropic
    @property
    def specular(self):        return self._specular
    @property
    def metallicness(self):    return self._metallicness
    @property
    def specular_tint(self):   return self._specular_tint
    @property
    def clearcoat(self):       return self._clearcoat
    @property
    def clearcoat_gloss(self): return self._clearcoat_gloss


    @color.setter
    def color(self, value: tuple | list | glm.vec3 | np.ndarray):
        self._color = validate_glm_vec3("Material", "color", value)
        if self.material_handler: self.material_handler.write()
        
    @texture.setter
    def texture(self, value: Image | None):
        self._texture = validate_image("Material", "texture", value)
        if self.material_handler: self.material_handler.write()
        
    @normal.setter
    def normal(self, value: Image | None):
        self._normal = validate_image("Material", "normal map", value)
        if self.material_handler: self.material_handler.write()

    @roughness.setter
    def roughness(self, value: float | int | glm.float32):
        self._roughness = validate_float("Material", "roughness", value)
        if self.material_handler: self.material_handler.write()

    @subsurface.setter
    def subsurface(self, value: float | int | glm.float32):
        self._subsurface = validate_float("Material", "subsurface", value)
        if self.material_handler: self.material_handler.write()

    @sheen.setter
    def sheen(self, value: float | int | glm.float32):
        self._sheen = validate_float("Material", "sheen", value)
        if self.material_handler: self.material_handler.write()

    @sheen_tint.setter
    def sheen_tint(self, value: tuple | list | glm.vec3 | np.ndarray):
        self._sheen_tint = validate_glm_vec3("Material", "sheen tint", value)
        if self.material_handler: self.material_handler.write()

    @anisotropic.setter
    def anisotropic(self, value: float | int | glm.float32):
        self._anisotropic = validate_float("Material", "anisotropic", value)
        if self.material_handler: self.material_handler.write()

    @specular.setter
    def specular(self, value: float | int | glm.float32):
        self._specular = validate_float("Material", "specular", value)
        if self.material_handler: self.material_handler.write()

    @metallicness.setter
    def metallicness(self, value: float | int | glm.float32):
        self._metallicness = validate_float("Material", "metallicness", value)
        if self.material_handler: self.material_handler.write()

    @specular_tint.setter
    def specular_tint(self, value: tuple | list | glm.vec3 | np.ndarray):
        self._specular_tint = validate_glm_vec3("Material", "specular tint", value)
        if self.material_handler: self.material_handler.write()
    
    @clearcoat.setter
    def clearcoat(self, value: float | int | glm.float32):
        self._clearcoat = validate_float("Material", "clearcoat", value)
        if self.material_handler: self.material_handler.write()

    @clearcoat_gloss.setter
    def clearcoat_gloss(self, value: float | int | glm.float32):
        self._clearcoat_gloss = validate_float("Material", "clearcoat gloss", value)
        if self.material_handler: self.material_handler.write()