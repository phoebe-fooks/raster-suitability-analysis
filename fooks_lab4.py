#!/usr/bin/env python
# coding: utf-8

# In[56]:


import rasterio
import numpy as np
from rasterio.plot import show
#add to code

#The site cannot contain urban areas.
urban_rs = rasterio.open('urban_areas.tif')
urban = urban_rs.read(1)
urban = np.where(urban > 0, 0, 1)
urban_ar = np.zeros_like(urban)
for row in range(1, urban.shape[0] -1):
    for col in range(1, urban.shape[1] -1):
        window = urban[row - 1:row + 10,
                       col - 1:col + 8]
        urban_ar[row, col] = window.mean()
urban_array = np.where(urban_ar != 1 , 0, 1)

#Less than 2% of land can be covered by water bodies.
water_rs = rasterio.open('water_bodies.tif')
water = water_rs.read(1)
water = np.where(water < 0, 0, water)
water_ar = np.zeros_like(water)
for row in range(1, water.shape[0] -1):
    for col in range(1, water.shape[1] -1):
        window = water[row - 1:row + 10,
                       col - 1:col + 8]
        water_ar[row, col] = window.mean()
water_array = np.where(water_ar < 0.02, 1, 0)

#Less than 5% of the site can be within protected areas.
protected_rs = rasterio.open('protected_areas.tif')
protected = protected_rs.read(1)
protected = np.where(protected < 0, 0, protected)
protected_ar = np.zeros_like(protected)
for row in range(1, protected.shape[0] -1):
    for col in range(1, protected.shape[1] -1):
        window = protected[row - 1:row + 10,
                           col - 1:col + 8]
        protected_ar[row, col] = window.mean()
protected_array = np.where(protected_ar < 0.05, 1, 0)

#Less than 5% of the site can be within protected areas.
protected_rs = rasterio.open('protected_areas.tif')
protected = protected_rs.read(1)
protected = np.where(protected < 0, 0, protected)
protected_ar = np.zeros_like(protected)
for row in range(1, protected.shape[0] -1):
    for col in range(1, protected.shape[1] -1):
        window = protected[row - 1:row + 10,
                           col - 1:col + 8]
        protected_ar[row, col] = window.mean()
protected_array = np.where(protected_ar < 0.05, 1, 0)

#An average slope of less than 15 degrees is necessary for the development plans.
slope_rs = rasterio.open('slope.tif')
slope = slope_rs.read(1)
slope = np.where(slope < 0, 0, slope)
slope_ar = np.zeros_like(slope, np.float32)
for row in range(5, slope.shape[1] - 5):
    for col in range(4, slope.shape[1] - 4):
        window = slope[row - 5:row + 5 + 1,
                       col - 4:col + 4 + 1]
        slope_ar[row, col] = window.mean()   
slope_array = np.where(slope_ar < 15, 1, 0)

#The average wind speed must be greater than 8.5m/s.
wind_rs = rasterio.open('ws80m.tif')
wind = wind_rs.read(1)
wind = np.where(wind< 0, 0, wind)
wind_ar = np.zeros_like(wind)
for row in range(1, wind.shape[0] -1):
    for col in range(1, wind.shape[1] -1):
        window = wind[row - 1:row + 10,
                      col - 1:col + 8]
        wind_ar[row, col] = window.mean()
wind_array = np.where(wind_ar > 8.5, 1, 0)

#write raster
with rasterio.open(r'slope.tif') as dataset:
    with rasterio.open(f'suitable_sites.tif', 'w',
                       driver = 'GTiff',
                       height = suitable_array.shape[0],
                       width = suitable_array.shape[1],
                       count = 1,
                       dtype = np.int32,
                       crs = dataset.crs, 
                       transform = dataset.transform,
                       nodata = -9999) as tif_dataset:
        tif_dataset.write(suitable_array, 1)
show(suitable_array)

#print final statement
sum_array = urban_array + water_array + protected_array + slope_array + wind_array
suitable_array = np.where(sum_array == 5, 1, 0)
print(suitable_array.sum())

