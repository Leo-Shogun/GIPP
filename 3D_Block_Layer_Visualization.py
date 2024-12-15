# Copyright (c) 2024 Xinrui LIU
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
#
# project address: https://github.com/Leo-Shogun/GIPP
# code name: 3D_Block_Layer_Visualization.py
# author: Xinrui LIU
# author: Xinzhe LIU, School of Architecture, Southeast University, Nanjing, China
# detail information: Use 3D histograms to visualize data in different blocks and layers.


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# Step 1: Load the CSV file and preprocess the data
data = pd.read_csv('test.csv')  # Load the data from a CSV file, you can edit for your file name

# Define default view angles for 3D plots
default_elev = 30  # Default elevation angle for the 3D plot, can be changed
default_azim = -60  # Default azimuthal angle for the 3D plot, can be changed

# Split the first column into block and layer numbers
data[['block_number', 'layer_number']] = data.iloc[:, 0].str.split('_', expand=True)
data['block_number'] = data['block_number'].astype(int)  # Convert block_number to integer
data['layer_number'] = data['layer_number'].astype(int)  # Convert layer_number to integer
data['value'] = data.iloc[:, 1]  # Extract the value column

# Step 2: Prepare the data for plotting
unique_blocks = data['block_number'].unique()  # Get unique block numbers
num_blocks = len(unique_blocks)  # Total number of blocks
side_length = int(np.ceil(np.sqrt(num_blocks)))  # Calculate side length for arranging blocks in a grid

# Step 3: Create bins for values and define a colormap
value_column = 'value'
values = data[value_column]
# Divide values into 100 quantile-based bins
value_bins, bins = pd.qcut(values, q=100, retbins=True, duplicates='drop')

# Create a color map with 100 shades of blue
colors = plt.cm.Blues(np.linspace(0.4, 1, 100))
cmap = ListedColormap(colors)

# Step 4: Plot 3D bar chart of all blocks and layers
fig = plt.figure(figsize=(12, 10))  # Initialize the figure

default_height = 1.0  # Default bar height in the 3D plot
custom_height = default_height  # Adjustable bar height
ax = fig.add_subplot(111, projection='3d')  # Create a 3D subplot

# Iterate through each block and layer to add bars to the 3D plot
for block_num in unique_blocks:
    block_data = data[data['block_number'] == block_num]
    row, col = divmod(block_num - 1, side_length)  # Map block number to grid row and column
    if row < side_length and col < side_length:  # Ensure within grid bounds
        for _, layer in block_data.iterrows():
            layer_number = layer['layer_number']
            value = layer['value']
            # Determine color based on the value bin
            color_idx = np.digitize(value, bins) - 1
            color = cmap(color_idx)
            # Plot the 3D bar with appropriate height and color
            ax.bar3d(col, row, layer_number * custom_height, 1, 1, custom_height,
                     color='whitesmoke' if value == 0 else color,
                     alpha=0.1 if value == 0 else 0.9)

# Set axis labels and title
ax.set_xlabel('Block Column Index')
ax.set_ylabel('Block Row Index')
ax.set_zlabel('Layer Number')
ax.set_title('3D Bar Chart of Each Block and Layer Values')

# Set the view angles
ax.view_init(elev=default_elev, azim=default_azim)

# Add a color bar for the value bins
sm = plt.cm.ScalarMappable(cmap=cmap)
sm.set_array(values)
cbar = plt.colorbar(sm, ax=ax, fraction=0.02, pad=0.1)
cbar.set_label('Value Bins')
cbar.set_ticks([values.min(), values.max()])
cbar.set_ticklabels([f'{values.min():.2f}', f'{values.max():.2f}'])

plt.show()  # Display the plot

# Step 5: Plot top-down view of the 3D bar chart
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')  # Create another 3D subplot

# Repeat the plotting process for a top-down view
for block_num in unique_blocks:
    block_data = data[data['block_number'] == block_num]
    row, col = divmod(block_num - 1, side_length)
    if row < side_length and col < side_length:
        for _, layer in block_data.iterrows():
            layer_number = layer['layer_number']
            value = layer['value']
            color_idx = np.digitize(value, bins) - 1
            color = cmap(color_idx)
            ax.bar3d(col, row, layer_number * custom_height, 1, 1, custom_height,
                     color='whitesmoke' if value == 0 else color,
                     alpha=0.1 if value == 0 else 0.9)

# Set axis labels and title
ax.set_xlabel('Block Column Index')
ax.set_ylabel('Block Row Index')
ax.set_title('Top-Down View of 3D Bar Chart of Each Block and Layer Values')

# Set top-down view angles and remove z-axis ticks
ax.view_init(elev=90, azim=-90)
ax.zaxis.line.set_linewidth(0.)
ax.set_zticks([])

# Add a color bar for the value bins
sm = plt.cm.ScalarMappable(cmap=cmap)
sm.set_array(values)
cbar = plt.colorbar(sm, ax=ax, fraction=0.02, pad=0.1)
cbar.set_label('Value Bins')
cbar.set_ticks([values.min(), values.max()])
cbar.set_ticklabels([f'{values.min():.2f}', f'{values.max():.2f}'])

plt.show()  # Display the top-down view
