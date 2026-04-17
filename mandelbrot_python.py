"""
============================================================
ICS 2311 – COMPUTER GRAPHICS II
GROUP 17

Felix Nduati SCT211-0313/2023
Philip Muendo SCT211-0013/2023

PART B: MANDELBROT SET (PYTHON IMPLEMENTATION)

DESCRIPTION:
This program generates and visualizes the Mandelbrot Set using Python.

Unlike the C++ OpenGL version which draws pixel-by-pixel on screen,
this implementation:
- Uses NumPy for numerical computation
- Uses Matplotlib for rendering the image

Key idea:
Each pixel is mapped to a complex number and tested using the
Mandelbrot iterative formula:
        z = z² + c

The result is stored in a 2D array and later converted into a colored image.

ADVANTAGES OF PYTHON VERSION:
- Easier to experiment with colors and parameters
- Faster to prototype and visualize
- Cleaner mathematical representation using NumPy
============================================================
"""

import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# CONFIGURATION PARAMETERS
# ============================================================

# Image resolution (higher values = sharper image but slower computation)
WIDTH = 800
HEIGHT = 600  

# Maximum number of iterations for Mandelbrot calculation
# This controls detail level:
# - Low value → faster but less detail
# - High value → slower but more accurate boundary
MAX_ITER = 200


def mandelbrot(c, max_iter):
    """
    ============================================================
    CORE MANDELBROT FUNCTION (FOR A SINGLE POINT)

    This function determines whether a complex number 'c'
    belongs to the Mandelbrot Set.

    PARAMETERS:
    - c: Complex number (e.g., a + bi)
    - max_iter: Maximum iterations allowed

    PROCESS:
    1. Start with z = 0
    2. Repeatedly apply: z = z² + c
    3. Check if z "escapes" (becomes too large)

    RETURN VALUE:
    - Number of iterations before escape
    - OR max_iter if the point never escapes (inside set)

    INTERPRETATION:
    - Small return value → escapes quickly → outside set
    - Large return value → escapes slowly → near boundary
    - max_iter → inside Mandelbrot set
    ============================================================
    """

    z = 0  # Initial value (z₀ = 0)

    for n in range(max_iter):

        # Escape condition:
        # If magnitude of z > 2, it will go to infinity
        if abs(z) > 2:
            return n  # Return how fast it escaped

        # Apply Mandelbrot formula
        z = z*z + c

    # If loop finishes → point did NOT escape → inside set
    return max_iter


def generate_mandelbrot():
    """
    ============================================================
    GENERATE FULL MANDELBROT SET

    This function creates a 2D grid (image) where:
    - Each cell represents one pixel
    - Each value stores iteration count (escape speed)

    OUTPUT:
    A 2D NumPy array of size [HEIGHT x WIDTH]

    IMPORTANT CONCEPT:
    We map screen pixels → complex plane coordinates
    ============================================================
    """

    # Initialize empty array to store iteration counts
    # Each position corresponds to a pixel
    result = np.zeros((HEIGHT, WIDTH))

    # Define region of complex plane to visualize
    # These ranges determine what part of Mandelbrot we see
    x_min, x_max = -2.5, 1.5
    y_min, y_max = -1.5, 1.5

    print("Generating Mandelbrot set... Please wait.")

    # Loop through every pixel (row = y-axis, col = x-axis)
    for row in range(HEIGHT):
        for col in range(WIDTH):

            """
            MAP PIXEL → COMPLEX NUMBER

            Convert pixel coordinates into complex number:
                c = real + imag*i

            This transforms screen space into mathematical space
            """

            real = x_min + (col / WIDTH) * (x_max - x_min)
            imag = y_min + (row / HEIGHT) * (y_max - y_min)

            c = complex(real, imag)

            # Compute Mandelbrot iteration count for this point
            result[row, col] = mandelbrot(c, MAX_ITER)

        # Show progress (useful for long computations)
        if row % 100 == 0:
            print(f"Progress: {row}/{HEIGHT} rows completed")

    return result


def create_image(data):
    """
    ============================================================
    COLOR MAPPING FUNCTION

    Converts raw iteration data into an RGB image.

    INPUT:
    - data: 2D array of iteration counts

    OUTPUT:
    - 3D RGB image array [HEIGHT x WIDTH x 3]

    COLOR LOGIC:
    - Inside set → BLACK
    - Outside → BLUE gradient
    - Boundary → WHITE glow (last 15% of iterations)
    ============================================================
    """

    # Create empty RGB image (3 channels: Red, Green, Blue)
    image = np.zeros((HEIGHT, WIDTH, 3))

    for row in range(HEIGHT):
        for col in range(WIDTH):

            iteration = data[row, col]

            # Case 1: Point is INSIDE Mandelbrot set
            if iteration == MAX_ITER:
                image[row, col] = [0, 0, 0]  # Black

            else:
                """
                NORMALIZE ITERATION VALUE

                t ranges from 0 → 1
                - 0 = fast escape
                - 1 = slow escape (near boundary)
                """
                t = iteration / MAX_ITER

                # Apply smoothing to avoid harsh color banding
                smooth = np.sqrt(t)

                """
                BASE BLUE GRADIENT

                Creates smooth transition from dark blue to lighter tones
                """
                r = smooth * 0.7
                g = smooth * 0.8 + 0.114
                b = smooth * 0.5 + 0.565

                """
                BOUNDARY ENHANCEMENT

                Points near boundary (t > 0.85) are blended toward white
                This creates the bright glowing edge seen in Mandelbrot images
                """
                if t > 0.85:
                    blend = (t - 0.85) / 0.15  # Normalize to 0–1 range

                    # Smooth transition (cubic interpolation)
                    blend = blend * blend * (3 - 2 * blend)

                    # Blend base color toward white (1,1,1)
                    r = r + (1 - r) * blend
                    g = g + (1 - g) * blend
                    b = b + (1 - b) * blend

                image[row, col] = [r, g, b]

    return image


def main():
    """
    ============================================================
    MAIN PROGRAM EXECUTION

    Steps:
    1. Generate Mandelbrot data
    2. Convert data to colored image
    3. Display using Matplotlib
    4. Save image to file
    ============================================================
    """

    # Step 1: Generate Mandelbrot iteration data
    mandelbrot_data = generate_mandelbrot()

    # Step 2: Convert to RGB image
    colored_image = create_image(mandelbrot_data)

    # Step 3: Display image
    plt.figure(figsize=(10, 7.5))  # Maintain aspect ratio
    plt.imshow(colored_image, extent=[-2.5, 1.5, -1.5, 1.5])

    # Add labels for clarity
    plt.title("Mandelbrot Set - Group 17 (Python Implementation)", fontsize=14)
    plt.xlabel("Real Axis")
    plt.ylabel("Imaginary Axis")

    plt.tight_layout()

    # Step 4: Save high-quality output
    plt.savefig("mandelbrot_output_python.png", dpi=150, bbox_inches='tight')
    print("Image saved as: mandelbrot_output_python.png")

    # Display window
    plt.show()

    print("Done! Close the image window to exit.")


# Entry point of the program
if __name__ == "__main__":
    main()