import numpy as np
import moderngl as mgl
from .shader import Shader
from .framebuffer import Framebuffer

from .post_process import PostProcess

class Frame:
    shader: Shader=None
    vbo: mgl.Buffer=None
    vao: mgl.VertexArray=None
    framebuffer: mgl.Framebuffer=None

    def __init__(self, scene, resolution=1, filter=(mgl.LINEAR, mgl.LINEAR)) -> None:
        """
        Basilisk render destination. 
        Can be used to render to the screen or for headless rendering
        """

        self.scene  = scene
        self.engine = scene.engine
        self.ctx    = scene.ctx

        # Load framebuffer
        self.resolution = resolution
        self.filter = filter
        size = tuple(map(lambda x: int(x * self.resolution), self.engine.win_size))
        self.framebuffer = Framebuffer(self.engine, size=size, filter=self.filter)
        self.ping_pong_buffer = Framebuffer(self.engine, size=size, filter=self.filter)

        # Load Shaders
        self.shader = Shader(self.engine, self.engine.root + '/shaders/frame.vert', self.engine.root + '/shaders/frame.frag')
        self.scene.shader_handler.add(self.shader)

        # Load VAO
        self.vbo = self.ctx.buffer(np.array([[-1, -1, 0, 0, 0], [1, -1, 0, 1, 0], [1, 1, 0, 1, 1], [-1, 1, 0, 0, 1], [-1, -1, 0, 0, 0], [1, 1, 0, 1, 1]], dtype='f4'))
        self.vao = self.ctx.vertex_array(self.shader.program, [(self.vbo, '3f 2f', 'in_position', 'in_uv')], skip_errors=True)

        # TEMP TESTING
        self.post_processes = []


    def render(self) -> None:
        """
        Renders the current frame to the screen
        """

        for process in self.post_processes:
            self.ping_pong_buffer = process.apply(self.framebuffer, self.ping_pong_buffer)
            
            temp = self.framebuffer
            self.framebuffer = self.ping_pong_buffer
            self.ping_pong_buffer = temp
        
        self.ctx.screen.use()
        self.shader.program['screenTexture'] = 0
        self.framebuffer.texture.use(location=0)
        self.vao.render()


    def use(self) -> None:
        """
        Uses the frame as a render target
        """
        
        self.framebuffer.use()
        self.clear()

    def add_post_process(self, post_process: PostProcess) -> PostProcess:
        """
        Add a post process to the frames post process stack
        """

        self.post_processes.append(post_process)
        return post_process

    def save(self, destination: str=None) -> None:
        """
        Saves the frame as an image to the given file destination
        """

        self.framebuffer.save(destination)
    
    def clear(self):
        self.framebuffer.clear()

    def resize(self, size: tuple[int]=None) -> None:
        """
        Resize the frame to the given size. None for window size
        """

        size = tuple(map(lambda x: int(x * self.resolution), self.engine.win_size))
        self.framebuffer.resize(size)
        self.ping_pong_buffer.resize(size)

    def __del__(self) -> None:
        """
        Releases memory used by the frame
        """
        
        if self.vbo: self.vbo.release()
        if self.vao: self.vao.release()