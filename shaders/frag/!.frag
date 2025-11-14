
            #version 330


            in vec3 v_pos;
            out vec4 fragColor;

            void main() {
                vec3 color = 0.5 + 0.5 * normalize(v_pos);
                fragColor = vec4(color, 1.0);
            }
