# Travel Route Optimization with FastAPI

This project provides a FastAPI application that calculates optimized travel routes for users based on their location and a list of tourist attractions. The application clusters tourist attractions using KMeans clustering and generates routes based on geographical proximity and user preferences. The routes are optimized by sorting attractions based on their rating and opening time, ensuring a smooth travel experience.

## Features

- **Cluster Attractions:** Clusters tourist attractions into the number of days the user plans to stay.
- **Calculate Distances:** Uses the Haversine formula to calculate the distance between the user's location and attractions.
- **Sort by Rating and Time:** Selects the top-rated places and sorts them by opening times.
- **Dockerized Application:** The application is packaged in a Docker container for easy deployment.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/yourrepository.git
   cd yourrepository
2. Build the Docker image:
   ```bash
   docker build -t travel-route-optimizer .
4. Run the Docker container:
   ```bash
   docker run -p 8000:8000 travel-route-optimizer
6. The application will be available at http://localhost:8000.
