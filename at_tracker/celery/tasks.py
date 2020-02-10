import httpx
import traceback

from geojson import Feature, FeatureCollection, Point

from at_tracker.common.config import AT_API_URL, AT_API_KEY
from at_tracker.common.cache import cache_json_get, cache_json_set

from at_tracker.celery.app import celery_app

HEADERS = {'Ocp-Apim-Subscription-Key': AT_API_KEY}


def _at_api_request(url, method='GET', headers=HEADERS, **kwargs):
    response = httpx.request(method,
                             AT_API_URL + url,
                             headers=HEADERS,
                             **kwargs)
    response.raise_for_status()
    return response.json().get('response')


def _get_route_id(route_id):
    for route in cache_json_get('routes'):
        if route['route_id'] == route_id:
            return route

def _get_agency_id(agency_id):
    for agency in cache_json_get('agencies'):
        if agency['agency_id'] == agency_id:
            return agency


def _vehicle_to_feature(vehicle):
    if vehicle.get('vehicle').get('trip'):
        route = _get_route_id(vehicle.get('vehicle').get('trip').get('route_id'))
        agency = _get_agency_id(route['agency_id'])
        properties = {
            'bearing': vehicle.get('vehicle').get('position').get('bearing'),
            'speed': vehicle.get('vehicle').get('position').get('speed', 0) * 3.6,
            'odometer': vehicle.get('vehicle').get('position').get('odometer'),
            'timestamp': vehicle.get('vehicle').get('timestamp'),
            'vehicle_id': vehicle.get('vehicle').get('vehicle').get('id'),
            'vehicle_label': vehicle.get('vehicle').get('vehicle').get('label'),
            'vehicle_license': vehicle.get('vehicle').get('vehicle').get('license_plate'),
            'occupancy_status': vehicle.get('vehicle').get('occupancy_status'),
            'trip_id': vehicle.get('vehicle').get('trip').get('trip_id'),
            'trip_start_time': vehicle.get('vehicle').get('trip').get('start_time'),
            'trip_start_date': vehicle.get('vehicle').get('trip').get('start_date'),
            'route_id': vehicle.get('vehicle').get('trip').get('route_id'),
            'direction_id': vehicle.get('vehicle').get('trip').get('direction_id'),
            **route,
            **agency
        }
    else:
        return None

    return Feature(
        geometry=Point(
            coordinates=(
                vehicle.get('vehicle').get('position').get('longitude'),
                vehicle.get('vehicle').get('position').get('latitude')
            )
        ),
        properties=properties
    )


@celery_app.task
def fetch_routes():
    response = _at_api_request('/gtfs/routes')
    cache_json_set('routes', response)


@celery_app.task
def fetch_stops():
    response = _at_api_request('/gtfs/stops')
    cache_json_set('stops', response)


@celery_app.task
def fetch_agencies():
    response = _at_api_request('/gtfs/agency')
    cache_json_set('agencies', response)


@celery_app.task
def fetch_vehicles():
    response = _at_api_request('/public/realtime/vehiclelocations')
    fc = []
    for vehicle in response.get('entity'):
        try:
            f = _vehicle_to_feature(vehicle)
            if f:
                fc.append(f)
        except:
            pass

    cache_json_set('vehicles', FeatureCollection(fc))
