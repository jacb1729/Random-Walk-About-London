import numpy as np
from multipledispatch import dispatch

START = (51.564, 0.00227) # (latitude, longitude)

@dispatch(np.ndarray, np.ndarray)
def numpy_haversine_distance(arr_1: np.ndarray, arr_2: np.ndarray) -> np.ndarray:
    """Gets the rowise haversine distance between 2 arrays, where axis 0 indexes the coordinates, axis 1 has length 2
    Maps a pair of 2D arrays to a 1D array, (N x 2, N x 2) -> N"""
    assert arr_1.shape == arr_2.shape, "Input arrays must have the same shape."
    rarr_1 = np.radians(arr_1)
    rarr_2 = np.radians(arr_2)
    dlat = rarr_1[:, 0] - rarr_2[:, 0]
    dlon = rarr_1[:, 1] - rarr_2[:, 1]
    return numpy_haversine_function(dlat) + np.cos(rarr_1[:, 0]) * np.cos(rarr_2[:, 0]) * numpy_haversine_function(dlon)

@dispatch(np.ndarray, (tuple, list))
def numpy_haversine_distance(arr_1: np.ndarray, point: tuple) -> np.ndarray:
    """Gets the rowwise haversine distance between a 2D array and a single point.
    Maps a 2D array and a 2-tuple point to a 1D array, (N x 2, 2) -> N"""
    arr_2 = np.broadcast_to(np.asarray(point, dtype=arr_1.dtype), (len(arr_1), 2))
    return numpy_haversine_distance(arr_1, arr_2)


def numpy_geodesic_distance(arr_1: np.ndarray, arr_2: np.ndarray) -> np.ndarray:
    """Gets the rowwise great-circle distance in meters between 2 arrays using the haversine formula.
    Maps a pair of 2D arrays to a 1D array, (N x 2, N x 2) -> N"""
    R = 6_371_000  # Earth's radius in meters
    haversine_vals = numpy_haversine_distance(arr_1, arr_2)
    return 2 * R * np.arcsin(np.sqrt(haversine_vals))

def numpy_haversine_function(arr: np.ndarray):
    '''Pointwise Haversine function'''
    arr = np.sin(arr / 2) ** 2
    return arr

def get_nearest_node_row_id(nodes_df, point: tuple = START) -> int:
    '''Get the row number in nodes_df of nearest node to a given point (lat, lon) using numpy for speed'''
    arr = nodes_df[['lat', 'lon']].values
    distances = numpy_haversine_distance(arr, point)
    return np.argmin(distances)

    
def get_nearest_node_uid(nodes_df, point: tuple = START, return_row_id=False) -> int:
    '''Get the uid nearest node to a given point (lat, lon) using numpy for speed.
    '''
    row_id = get_nearest_node_row_id(nodes_df, point=point)
    if nodes_df.index.name == 'id':
        uid = nodes_df.iloc[row_id].name
    elif 'id' in nodes_df.columns:
        uid = nodes_df.iloc[row_id].id
    else:
        raise Exception("Need an id column or id as index")
    return uid, row_id if return_row_id else uid



