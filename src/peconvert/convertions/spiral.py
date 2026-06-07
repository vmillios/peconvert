import matplotlib.pyplot as plt
import numpy as np

def convert(data: bytearray):
    data_len = len(data)

    fig, ax = plt.subplots(figsize=(6, 6), dpi=100)
    ax.axis('off')
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    
    # Sample data if it's massive to avoid freezing matplotlib
    step = max(1, data_len // 50000) 
    indices = np.arange(0, data_len, step)
    
    theta = 0.1 * indices
    r = 0.01 * indices
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    colors = [data[i] for i in indices]
    
    ax.scatter(x, y, c=colors, cmap='viridis', s=1, edgecolors='none')
    fig.canvas.draw()
    
    # --- Updated for Matplotlib Compatibility ---
    # Fetch data as an RGBA memoryview, cast to numpy, and drop the alpha channel
    img = np.asarray(fig.canvas.buffer_rgba())
    img = img[..., :3]  # Slice out the Alpha channel to keep it strictly RGB
    
    plt.close(fig)
    return img