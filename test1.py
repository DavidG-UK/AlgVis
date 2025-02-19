import tkinter as tk
import random

# Initialize UI
root = tk.Tk()
root.geometry("500x500")

canvas = tk.Canvas(root, width=500, height=500, bg="white")
canvas.pack()

# Generate Random Data
arr = [random.randint(50, 400) for _ in range(10)]
bar_width = 500 // len(arr)
bar_spacing = 5  # Spacing between bars
bars = []  # Store bar objects

# Create bars as rectangles
for i, val in enumerate(arr):
    bar = canvas.create_rectangle(i * bar_width, 500 - val, (i + 1) * bar_width - bar_spacing, 500, fill="blue")
    bars.append(bar)

def animate_swap(i, j, step=0, max_steps=10):
    """Moves bars smoothly before swapping."""
    x1, y1, x2, y2 = canvas.coords(bars[i])
    x1_j, y1_j, x2_j, y2_j = canvas.coords(bars[j])

    # Calculate step size
    dx = (x1_j - x1) / max_steps  # Horizontal movement

    # Move gradually
    if step < max_steps:
        canvas.move(bars[i], dx, 0)  # Move i right
        canvas.move(bars[j], -dx, 0)  # Move j left
        root.after(50, lambda: animate_swap(i, j, step + 1, max_steps))  # Continue movement
    else:
        # Finalize swap
        bars[i], bars[j] = bars[j], bars[i]  # Swap references
        arr[i], arr[j] = arr[j], arr[i]  # Swap values
        bubble_sort_step(len(arr), 0, 0)  # Continue sorting

def bubble_sort_step(n, i, j):
    """Step-by-step bubble sort animation with movement."""
    if i < n - 1:
        if j < n - i - 1:
            if arr[j] > arr[j + 1]:  # Swap condition
                animate_swap(j, j + 1)  # Move and swap bars
            else:
                root.after(100, lambda: bubble_sort_step(n, i, j + 1))
        else:
            root.after(100, lambda: bubble_sort_step(n, i + 1, 0))
    else:
        print("Sorting Complete!")

# Start sorting animation
root.after(1000, lambda: bubble_sort_step(len(arr), 0, 0))

root.mainloop()
