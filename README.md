# Travel Route Optimization with FastAPI

This project provides a FastAPI application that generates optimal travel itineraries for users based on the number of days and a list of tourist attractions they wish to visit. The application clusters tourist attractions using KMeans clustering and organizes the itinerary by grouping nearby attractions into the same day. The places are optimized by sorting attractions based on their rating and opening time to ensuring a smooth travel experience.

## Features

- **Cluster Attractions:** Clusters tourist attractions into the number of days the user plans to stay.
- **Calculate Distances:** Uses the Haversine formula to calculate the distance between the user's location and attractions.
- **Sort by Rating and Time:** Selects the top-rated places and sorts them by opening times.
- **Dockerized Application:** The application is packaged in a Docker container for easy deployment.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/username/repository.git
   cd repository
2. Build the Docker image:
   ```bash
   docker build -t travel-route-optimizer .
3. Run the Docker container:
   ```bash
   docker run -p 8000:8000 travel-route-optimizer
4. The application will be available at http://localhost:8000.

## Requirements

- Python 3.11+
- Docker
- Required Python libraries:
  - fastapi
  - math
  - scikit-learn
  - pandas
