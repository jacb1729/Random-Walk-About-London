# Random Walk About London
Why not automate going for a walk about London using OpenStreetMap data? The views are statistically stunning!

Go to the `notebook.ipynb` now!

## Requirements
- `osmnx` (optional) - for small-scale network graphs
- `pyrosm` - for large-scale OSM data parsing
- `geopandas` - geospatial data handling
- `numpy` - numerical computations
- `matplotlib` - visualization
- Footwear (culturally advised)

## Progress

Work that's currently done:
- Getting graphical data for London (efficiently)
- Getting the geodesic distance between two points (efficiently)
- Choosing a start node based on given latitude-longitude
- Exploration tool - inline gmap links

Files: 
- `README.md` (project overview)
- `distances.py` (geodesic distance utilities)
- `data_and_validation_due_diligence.ipynb` (data validation)
- `notebook.ipynb` (main demo space)


Coming up
- Checking the given lengths against geodesic lengths
- Explore directionality of Edges GeoDF
- If all is directed, implement a random walk algorithm which walks a given distance

Extension ideas
- Get building data for applications
- Random walks...to cafes? How likely are you to walk a desired length and ensure that you end up in a cafe?
