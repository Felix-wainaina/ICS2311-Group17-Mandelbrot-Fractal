# ICS 2311 Computer Graphics II

## Group 17 – Mandelbrot Set Implementation

---

### 📘 Project Overview

This project demonstrates the implementation of the **Mandelbrot Set**, a well-known fractal in computer graphics. The goal is to visualize complex mathematical behavior using both **real-time rendering (C++ OpenGL)** and **image generation (Python)**.

The Mandelbrot Set is generated using an iterative function:

[
z_{n+1} = z_n^2 + c
]

Each point in the complex plane is tested to determine whether it remains bounded or escapes to infinity. The number of iterations before escape determines the color of the pixel.

---

### 👥 Group Members

* **Felix Nduati** – SCT211-0313/2023
* **Philip Muendo** – SCT211-0013/2023

---

## 📂 Project Structure

```
ICS2311-Group17-Mandelbrot-Fractal/
│
├── mandelbrot_OpenGl.cpp          # C++ OpenGL implementation
├── mandelbrot.exe          # Compiled executable (Windows)
├── mandelbrot_python.py    # Python implementation
├── mandelbrot_output.png   # Output image (Python)
├── mandelbrot_output.jpg   # Alternative output image
└── README.md               # Project documentation
```

---

## 🖥️ 1. C++ OpenGL Version (`mandelbrot_OpenGl.cpp`)

### 🔹 Description

This implementation renders the Mandelbrot Set in **real-time** using OpenGL and GLUT. It allows visualization of the fractal directly on screen.

### 🔹 Features

* Resolution: **800 × 600**
* Real-time rendering
* Escape-time algorithm
* Smooth blue gradient coloring

---

### ⚙️ Compilation (Windows – MinGW)

```bash
g++ mandelbrot_OpenGl.cpp -o mandelbrot.exe -lfreeglut -lglu32 -lopengl32
```

---

### ▶️ Run

```bash
./mandelbrot.exe
```

---

### 📌 Output

* Displays an interactive window showing the Mandelbrot fractal

---

## 🐍 2. Python Version (`mandelbrot_python.py`)

### 🔹 Description

This version generates a **static image** of the Mandelbrot Set using Python. It uses numerical computation and plotting libraries.

---

### 🔹 Requirements

Install dependencies:

```bash
pip install numpy matplotlib
```

---

### ▶️ Run

```bash
python mandelbrot_python.py
```

---

### 📌 Output Files

The script generates:

* `mandelbrot_output.png`
* `mandelbrot_output.jpg`

📍 Saved in:

```
ICS2311-Group17-Mandelbrot-Fractal/
```

---

## 🎨 Output Characteristics

Both implementations produce:

* **Black regions** → Points inside the Mandelbrot set (bounded)
* **Blue gradient** → Points that escape
* **Bright edges** → Regions with slow escape (high detail boundary)

---

## 🧠 Key Concepts Demonstrated

* Complex number computations
* Iterative algorithms
* Escape-time fractal generation
* Color mapping based on iteration count
* Real-time vs static rendering approaches

---

## 🚀 Conclusion

This project highlights how mathematical concepts such as complex iteration can be visualized using computer graphics techniques. The comparison between C++ OpenGL and Python implementations demonstrates different approaches to rendering fractals.

---

## 📎 Notes

* Ensure OpenGL libraries are properly installed before compiling the C++ version.
* Python version is easier to run but does not provide real-time interaction.
* Higher iteration values improve detail but increase computation time.

---

## 🎥 Bonus (Optional Enhancement)

For advanced visualization, the Mandelbrot set can be extended into:

* 3D surfaces
* Zoom animations
* GPU-based rendering (Shaders)

---
