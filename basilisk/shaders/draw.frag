#version 330 core

layout (location = 0) out vec4 fragColor;

in vec4     color;
in vec2     imageIndex;
in vec2     uv;
flat in int usesImage;

struct textArray {
    sampler2DArray array;
};
uniform textArray textureArrays[5];

void main() {
    if (bool(usesImage)) {
        fragColor = texture(textureArrays[int(round(imageIndex.x))].array, vec3(uv, round(imageIndex.y)));
        // fragColor = vec4(1, 0, 0, 1);
    }
    else {
        fragColor = color;
    }
}