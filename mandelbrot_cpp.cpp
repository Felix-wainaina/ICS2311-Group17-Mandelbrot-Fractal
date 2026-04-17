/*
============================================================
ICS 2311 – COMPUTER GRAPHICS II
GROUP 17

Felix Nduati SCT211-0313/2023
Philip Muendo SCT211-0013/2023

PART B: MANDELBROT SET RENDERING USING OPENGL

DESCRIPTION:
This program renders the Mandelbrot Set using the escape-time algorithm.
Each screen pixel is mapped to the complex plane and iteratively tested
using the Mandelbrot equation: z = z^2 + c.

The output visually distinguishes:
- Points inside the set (black)
- Points outside (blue gradient)
- Boundary points (bright white glow)
============================================================
*/

#include <GL/glut.h>   // Library for window creation and drawing
#include <cmath>       // Provides mathematical functions like sqrt()

// Window dimensions (resolution of output)
const int WIDTH = 800;
const int HEIGHT = 600;

// Maximum number of iterations for Mandelbrot computation
// Higher = more detail but slower rendering
const int MAX_ITER = 200;

/*
============================================================
FUNCTION: drawMandelbrot()

CORE FUNCTION OF THE PROGRAM

This function:
1. Iterates through every pixel on the screen
2. Converts pixel coordinates into complex numbers
3. Applies Mandelbrot iteration formula
4. Assigns color based on escape behavior
============================================================
*/
void drawMandelbrot() {

    // Clear previous frame (color buffer)
    glClear(GL_COLOR_BUFFER_BIT);

    // Loop through every pixel horizontally
    for (int x = 0; x < WIDTH; x++) {

        // Loop through every pixel vertically
        for (int y = 0; y < HEIGHT; y++) {

            /*
            ============================================================
            STEP 1: MAP PIXEL → COMPLEX PLANE

            We convert screen coordinates into a complex number:
                c = real + imag*i

            WHY?
            The Mandelbrot Set exists in the complex plane, not screen space.

            RANGE:
            This mapping roughly corresponds to:
                real ∈ [-2, 2]
                imag ∈ [-2, 2]
            ============================================================
            */
            double real = (x - WIDTH / 2.0) * 4.0 / WIDTH;
            double imag = (y - HEIGHT / 2.0) * 4.0 / WIDTH;

            // Define complex number c
            double c_real = real;
            double c_imag = imag;

            /*
            ============================================================
            STEP 2: INITIALIZE z = 0

            Mandelbrot iteration always starts with:
                z0 = 0
            ============================================================
            */
            double z_real = 0;
            double z_imag = 0;

            // Counter to track how many iterations occur
            int iteration = 0;

            /*
            ============================================================
            STEP 3: MANDELBROT ITERATION

            Formula:
                z = z^2 + c

            Expanded:
                (a + bi)^2 = (a^2 - b^2) + 2ab i

            So:
                real = a^2 - b^2 + c_real
                imag = 2ab + c_imag

            LOOP STOPS WHEN:
            - |z| > 2 → point escapes (outside set)
            - iteration reaches MAX_ITER → inside set
            ============================================================
            */
            while (z_real * z_real + z_imag * z_imag <= 4 && iteration < MAX_ITER) {

                double temp = z_real * z_real - z_imag * z_imag + c_real;

                z_imag = 2 * z_real * z_imag + c_imag;

                z_real = temp;

                iteration++;
            }

            /*
            ============================================================
            STEP 4: COLORING (VISUALIZATION)

            THREE REGIONS:

            1. INSIDE SET:
               - Did NOT escape → colored BLACK

            2. OUTSIDE SET:
               - Escaped early → blue gradient

            3. BOUNDARY:
               - Escaped slowly → bright white glow

            WHY IMPORTANT?
            The boundary contains the most complex fractal detail
            ============================================================
            */
            if (iteration == MAX_ITER) {

                // Point is INSIDE Mandelbrot → black
                glColor3f(0.0, 0.0, 0.0);

            } else {

                /*
                Normalize iteration value:
                t ∈ [0,1]
                0 → fast escape
                1 → slow escape (near boundary)
                */
                float t = (float)iteration / MAX_ITER;

                // Smooth curve for natural gradient (reduces banding)
                float smooth = sqrt(t);

                /*
                BASE COLOR (BLUE GRADIENT)

                Creates deep blue background transitioning to lighter tones
                */
                float base_red   = smooth * 0.7f;
                float base_green = smooth * 0.8f + 0.114f;
                float base_blue  = smooth * 0.5f + 0.565f;

                /*
                BOUNDARY DETECTION

                Last 15% of iterations represent points near boundary
                */
                float BOUNDARY_THRESHOLD = 0.85f;
                float boundary_blend = 0.0f;

                if (t >= BOUNDARY_THRESHOLD) {

                    /*
                    Convert t into a 0–1 range within boundary zone
                    */
                    boundary_blend = (t - BOUNDARY_THRESHOLD) / (1.0f - BOUNDARY_THRESHOLD);

                    /*
                    Apply smooth cubic interpolation:
                    Produces soft glowing transition
                    */
                    boundary_blend = boundary_blend * boundary_blend * (3.0f - 2.0f * boundary_blend);
                }

                /*
                FINAL COLOR = BLUE + WHITE BLEND

                - Outside boundary → pure blue
                - Near boundary → blends toward white
                */
                float red   = base_red   + (1.0f - base_red)   * boundary_blend;
                float green = base_green + (1.0f - base_green) * boundary_blend;
                float blue  = base_blue  + (1.0f - base_blue)  * boundary_blend;

                glColor3f(red, green, blue);
            }

            /*
            ============================================================
            STEP 5: DRAW PIXEL

            Each pixel is plotted individually using GL_POINTS
            ============================================================
            */
            glBegin(GL_POINTS);
                glVertex2i(x, y);
            glEnd();
        }
    }

    // Force execution of all drawing commands
    glFlush();
}

/*
============================================================
FUNCTION: init()

Sets up OpenGL environment:
- Background color
- 2D coordinate system
============================================================
*/
void init() {

    // Set background color (dark blue)
    glClearColor(0.0f, 0.114f, 0.565f, 1.0f);

    // Define 2D coordinate system matching screen size
    gluOrtho2D(0, WIDTH, 0, HEIGHT);
}

/*
============================================================
MAIN FUNCTION

Program execution starts here
============================================================
*/
int main(int argc, char** argv) {

    glutInit(&argc, argv);

    // Single buffer + RGB color mode
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB);

    glutInitWindowSize(WIDTH, HEIGHT);

    glutCreateWindow("Mandelbrot Set - Group 17");

    init();

    // Register rendering function
    glutDisplayFunc(drawMandelbrot);

    // Start infinite event loop
    glutMainLoop();

    return 0;
}