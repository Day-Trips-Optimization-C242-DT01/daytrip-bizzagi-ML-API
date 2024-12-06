from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from math import radians, sin, cos, sqrt, atan2

app = FastAPI()

class LokasiUser(BaseModel):
    latitude: float
    longitude: float

class Place(BaseModel):
    place_id: str
    latitude: float
    longitude: float
    rating: float
    open_time: str
    close_time: str

class RouteRequest(BaseModel):
    num_days: int
    lokasi_user: LokasiUser
    places: List[Place]

# Function to calculate Haversine distance
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth's radius in kilometers
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# Function to calculate routes within clusters
def calculate_routes(places_data, num_days, lokasi_user):
    # Extract features for clustering
    features = places_data[['latitude', 'longitude']]
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)

    # Perform clustering
    kmeans = KMeans(n_clusters=num_days, init='k-means++', n_init=1000, max_iter=10000, random_state=42)
    places_data['cluster'] = kmeans.fit_predict(features_scaled)

    results = []  # Store results for all clusters
    for cluster in range(num_days):
        cluster_result = {"cluster": cluster + 1, "total_distance": 0, "places": []}
        cluster_points = places_data[places_data['cluster'] == cluster]

        # Select top 5 places with the highest rating in the cluster
        if len(cluster_points) > 5:
            cluster_points = cluster_points.nlargest(5, 'rating')

        # Sort places by opening time
        cluster_points = cluster_points.sort_values(by='open_time').reset_index(drop=True)

        total_distance = 0
        distance_list = []

        # Get the first place
        first_point = cluster_points.iloc[0]

        # Calculate distance from the user's location to the first place
        origin = {"latitude": lokasi_user.latitude, "longitude": lokasi_user.longitude}
        destination = {"latitude": first_point['latitude'], "longitude": first_point['longitude']}
        distance_from_user = haversine(origin['latitude'], origin['longitude'], destination['latitude'], destination['longitude'])
        total_distance += distance_from_user

        # Add first place details
        cluster_result["places"].append({
            "place_id": first_point['place_id'],
            "open_time": first_point['open_time'],
            "close_time": first_point['close_time'],
            "rating": first_point['rating'],
            "distance_from_previous": distance_from_user,
        })

        # Iterate through the remaining places
        previous_point = first_point
        for _, row in cluster_points.iloc[1:].iterrows():
            origin = {"latitude": previous_point['latitude'], "longitude": previous_point['longitude']}
            destination = {"latitude": row['latitude'], "longitude": row['longitude']}
            distance = haversine(origin['latitude'], origin['longitude'], destination['latitude'], destination['longitude'])
            distance_list.append({"from": previous_point['place_id'], "to": row['place_id'], "distance": distance})
            total_distance += distance

            # Add place details
            cluster_result["places"].append({
                "place_id": row['place_id'],
                "open_time": row['open_time'],
                "close_time": row['close_time'],
                "rating": row['rating'],
                "distance_from_previous": distance,
            })

            # Update previous point
            previous_point = row

        # Add total distance and route distances to the result
        cluster_result["total_distance"] = total_distance
        cluster_result["distances"] = distance_list
        results.append(cluster_result)

    return results

# FastAPI endpoint for route calculation
@app.post("/calculate_routes")
def calculate_routes_endpoint(request: RouteRequest):
    # Convert places to a DataFrame
    places_data = pd.DataFrame([place.dict() for place in request.places])

    # Check if enough places are provided for clustering
    if len(places_data) < request.num_days:
        raise HTTPException(
            status_code=400,
            detail="Number of clusters (num_days) exceeds the number of places provided.",
        )

    # Calculate routes
    routes = calculate_routes(places_data, request.num_days, request.lokasi_user)
    return {"routes": routes}
