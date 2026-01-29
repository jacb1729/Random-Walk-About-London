import webbrowser
from functools import singledispatch
from shapely.geometry import Point


# # # # # # # # # # # # #
## Handling overloaded function 'open_google_maps'
def _google_maps_url(lat: float, lon: float) -> str:
    return f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"


def _google_maps_embed_url(lat: float, lon: float, api_key: str | None = None) -> str:
    if api_key:
        return f"https://www.google.com/maps/embed/v1/place?key={api_key}&q={lat},{lon}"
    # This may be blocked by X-Frame-Options depending on environment
    return f"https://www.google.com/maps?q={lat},{lon}&output=embed"


def _open_inline_map(lat: float, lon: float, *, api_key: str | None = None, inline_mode: str = "iframe") -> None:
    try:
        from IPython.display import IFrame, display
    except Exception as exc:  # pragma: no cover - runtime dependency
        raise RuntimeError("IPython is required for inline display in notebooks.") from exc

    if inline_mode == "iframe":
        display(IFrame(_google_maps_embed_url(lat, lon, api_key=api_key), width=900, height=600))
    else:
        raise ValueError("inline_mode must be 'iframe' or 'folium'.")


def _open_coord(
    lat: float,
    lon: float,
    *,
    open_in: str = "browser",
    api_key: str | None = None,
    inline_mode: str = "iframe",
) -> None:
    if open_in == "browser":
        webbrowser.open(_google_maps_url(lat, lon))
    elif open_in == "inline":
        _open_inline_map(lat, lon, api_key=api_key, inline_mode=inline_mode)
    else:
        raise ValueError("open_in must be 'browser' or 'inline'.")


def _is_coord_tuple(value) -> bool:
    if not isinstance(value, tuple) or len(value) != 2:
        return False
    lat, lon = value
    return isinstance(lat, (int, float)) and isinstance(lon, (int, float))


def _iter_coords(container):
    # Accept iterables of tuples or shapely Points
    for item in container:
        if Point is not None and isinstance(item, Point):
            yield (item.y, item.x)
        elif _is_coord_tuple(item):
            yield item
        else:
            raise TypeError(f"Unsupported coordinate item: {type(item)}")


@singledispatch
def open_google_maps(coords, *, open_in: str = "browser", api_key: str | None = None, inline_mode: str = "iframe"):
    raise TypeError(f"Unsupported type for coords: {type(coords)}")


@open_google_maps.register
def _(coords: tuple, *, open_in: str = "browser", api_key: str | None = None, inline_mode: str = "iframe"):
    # Single coordinate tuple or container of coordinates
    if _is_coord_tuple(coords):
        lat, lon = coords
        _open_coord(lat, lon, open_in=open_in, api_key=api_key, inline_mode=inline_mode)
        return
    # Treat as container of coords
    coords_list = list(_iter_coords(coords))
    if len(coords_list) > 50:
        raise ValueError("Refusing to open more than 50 Google Maps links.")
    for lat, lon in coords_list:
        _open_coord(lat, lon, open_in=open_in, api_key=api_key, inline_mode=inline_mode)


@open_google_maps.register
def _(coords: list, *, open_in: str = "browser", api_key: str | None = None, inline_mode: str = "iframe"):
    coords_list = list(_iter_coords(coords))
    if len(coords_list) > 50:
        raise ValueError("Refusing to open more than 50 Google Maps links.")
    for lat, lon in coords_list:
        _open_coord(lat, lon, open_in=open_in, api_key=api_key, inline_mode=inline_mode)


@open_google_maps.register
def _(coords: set, *, open_in: str = "browser", api_key: str | None = None, inline_mode: str = "iframe"):
    coords_list = list(_iter_coords(coords))
    if len(coords_list) > 50:
        raise ValueError("Refusing to open more than 50 Google Maps links.")
    for lat, lon in coords_list:
        _open_coord(lat, lon, open_in=open_in, api_key=api_key, inline_mode=inline_mode)


@open_google_maps.register
def _(coords: Point, *, open_in: str = "browser", api_key: str | None = None, inline_mode: str = "iframe"):
    _open_coord(coords.y, coords.x, open_in=open_in, api_key=api_key, inline_mode=inline_mode)
# # # # # # # # # # # # #


def open_google_maps_from_geodf(
    gdf,
    *,
    geometry_column: str = "geometry",
    open_in: str = "browser",
    api_key: str | None = None,
    inline_mode: str = "iframe",
):
    """Open Google Maps for each POINT geometry in a GeoDataFrame."""
    if geometry_column not in gdf.columns:
        raise ValueError(f"GeoDataFrame is missing '{geometry_column}' column.")

    points = gdf[geometry_column].tolist()
    if len(points) > 50:
        raise ValueError("Refusing to open more than 50 Google Maps links.")

    for point in points:
        if not isinstance(point, Point):
            raise TypeError(f"Expected Point geometries, got {type(point)}")
        _open_coord(point.y, point.x, open_in=open_in, api_key=api_key, inline_mode=inline_mode)
