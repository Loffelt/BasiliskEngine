#version 330 core

layout (location = 0) in vec2  in_position;
layout (location = 1) in vec4  in_color;
layout (location = 2) in int   in_uses_image;

out vec4     color;
out vec2     imageIndex;
out vec2     uv;
flat out int usesImage;

void main() {
    usesImage = in_uses_image;
    if (bool(in_uses_image)) {
        imageIndex = in_color.xy;
        uv = in_color.zw;
    }
    else{
        color = in_color;
    }
    gl_Position = vec4(in_position.x, -in_position.y, 0.0, 1.0);
}