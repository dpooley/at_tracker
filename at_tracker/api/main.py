import httpx
import traceback

from fastapi import FastAPI
from pydantic import BaseModel

from at_tracker.common.config import VERSION, API_V1_STR, TITLE, DESC
from at_tracker.common.cache import cache_json_get, cache_json_set


class GeoBound(BaseModel):
    zoom: int
    north: float
    south: float
    east: float
    west: float


def _api_geobounds(geobound: GeoBound, feature_collection: dict) -> dict:
    features = []
    for f in feature_collection['features']:
        lat = f['geometry']['coordinates'][1]
        lng = f['geometry']['coordinates'][0]
        if lat < geobound.north and \
           lat > geobound.south and \
           lng < geobound.east and \
           lng > geobound.west:
            features.append(f)
    return {'type': 'FeatureCollection', 'features': features}


app = FastAPI(version=VERSION, title=TITLE, description=DESC)


@app.post(API_V1_STR + '/vehicles')
def read_vehicles(geobound: GeoBound) -> dict:
    return _api_geobounds(geobound, cache_json_get('vehicles'))


@app.get(API_V1_STR + '/routes')
def read_routes():
    data = cache_json_get('routes')
    return {data}


@app.get(API_V1_STR + '/routes/{route_id}')
def read_route_id(route_id: str):
    data = {}
    cache = cache_json_get('routes')
    for item in cache:
        if route_id == item.get('route_id'):
            data = item
            break
    return {data}


@app.get(API_V1_STR + '/agencies')
def read_agency():
    data = cache_json_get('agencies')
    return {data}


@app.get(API_V1_STR + '/agencies/{agency_id}')
def read_agency_id(agency_id: str):
    data = {}
    cache = cache_json_get('agencies')
    for item in cache:
        if agency_id == item.get('agency_id'):
            data = item
            break
    return {data}


@app.get(API_V1_STR + '/stops')
def read_stops():
    data = cache_json_get('stops')
    return {data}


@app.get(API_V1_STR + '/stops/{stop_id}')
def read_stop_id(stop_id: str):
    data = {}
    cache = cache_json_get('stops')
    for item in cache:
        if stop_id == item.get('stop_id'):
            data = item
            break
    return {data}
