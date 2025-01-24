from .batch import Batch


class Chunk():
    chunk_handler: ...
    """Back refrence to the parent chunk handler"""
    position: tuple
    """The position of the chunk. Used as a key in the chunk handler"""
    batch: Batch
    """Batched mesh of the chunk"""
    nodes: set
    """Set conaining references to all nodes in the chunk"""
    static: bool
    """Type of node that the chunk recognizes"""

    def __init__(self, chunk_handler, position: tuple, static: bool, shader=None) -> None:
        """
        Basilisk chunk object. 
        Contains references to all nodes in the chunk.
        Handles batching for its own nodes
        """

        # Back references
        self.chunk_handler = chunk_handler

        # Chunk Attrbiutes
        self.position = position
        self.static = static
        self.shader = shader

        # Create empty batch
        self.batch = Batch(self)

        # Create empty set for chunk's nodes
        self.nodes = set()

    def render(self) -> None:
        """
        Renders the chunk mesh
        """

        if self.batch.vao: self.batch.vao.render()

    def update(self) -> bool:
        """
        Batches all the node meshes in the chunk        
        """

        # Check if there are no nodes in the chunk
        if not self.nodes: return False
        # Batch the chunk nodes, return success bit
        return self.batch.batch()

    def node_update_callback(self, node):
        if not self.batch.vbo: return
        
        data = node.get_data()
        self.batch.vbo.write(data, node.data_index * 25 * 4)

    def add(self, node):
        """
        Adds an existing node to the chunk. Updates the node's chunk reference
        """

        self.nodes.add(node)
        node.chunk = self

        return node

    def remove(self, node):
        """
        Removes a node from the chunk
        """

        self.nodes.remove(node)
        self.batch.vbo.clear()

        return node

    def get_program(self):
        """
        Gets the program of the chunks nodes' shader
        """

        shader = self.shader

        if shader: return shader.program
        return self.chunk_handler.engine.shader.program

    def __repr__(self) -> str:
        return f'<Basilisk Chunk | {self.position}, {len(self.nodes)} nodes, {'static' if self.static else 'dynamic'}>'

    def __del__(self) -> None:
        """
        Deletes the batch if this chunk is deleted
        """
        
        del self.batch