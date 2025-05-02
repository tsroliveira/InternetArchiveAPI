# Internet Archive Video API Facade

This project provides a RESTful API facade for accessing video content from the Internet Archive. It's built using Python and FastAPI, following clean architecture principles.

## Features

- Explore various video collections
- Get detailed information about specific collections
- List videos (items) within collections
- Get detailed information about specific videos, including thumbnails and playback URLs
- Clean architecture design
- Documented API endpoints with OpenAPI
- Unit tests for core functionality
- Environment variable configuration

## Project Structure

The project follows a clean architecture design with the following structure:

```
python/
├── app/
│   ├── api/            # API layer (FastAPI routes)
│   ├── core/           # Business logic layer
│   ├── models/         # Data models
│   ├── utils/          # Utility functions and helpers
│   └── main.py         # Application entry point
├── tests/              # Unit tests
├── requirements.txt    # Project dependencies
├── run.py              # Script to run the application
├── .env                # Environment variables (you need to create this)
└── README.md           # Project documentation
```

## Requirements

- Python 3.8 or higher
- pip for package management

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/tsroliveira/InternetArchiveAPI.git
   cd InternetArchiveAPI/python
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   
   On Windows:
   ```bash
   venv\Scripts\activate
   ```
   
   On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

4. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Create a `.env` file in the python directory with the following content:
   ```
   # Internet Archive API Configuration
   ARCHIVE_API_BASE_URL=https://archive.org/advancedsearch.php
   ```

## Running the Application

To run the application locally:

```bash
python run.py
```

The API server will start at `http://localhost:8000`.

You can access the API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Explore Video Collections

```
GET /api/v1/explore
```

Returns a list of video collections (categories) for exploration.

Query parameters:
- `page`: Page number (default: 1)
- `rows`: Number of results per page (default: 10, max: 100)
- `sort`: Sort criteria (default: "stars desc")

### Get Collection Details

```
GET /api/v1/collections/{collection_id}
```

Returns detailed information about a specific collection, including some of its videos.

Query parameters:
- `film_rows`: Number of videos to include (default: 10, max: 100)
- `page`: Page number for films pagination (default: 1)

### Get Collection Items (Videos)

```
GET /api/v1/collections/{collection_id}/items
```

Returns videos (items) within a specific collection.

Query parameters:
- `page`: Page number (default: 1)
- `rows`: Number of results per page (default: 10, max: 100)
- `sort`: Sort criteria (default: "stars desc")

### Get Video Details

```
GET /api/v1/videos/{video_id}
```

Returns detailed information about a specific video, including:
- Basic metadata (title, description, creator, date, subjects)
- Thumbnail URL
- Playback URLs for different formats
- The Playback URL was implemented along with this endpoint. The decision was to maintain the format already provided by the Internet Archive API. I understood that it would not be ideal for the client of this application to make an additional request, since the information is already returned by the current endpoint.


## Design Decisions

### Explore Endpoint Structure

The `/api/v1/explore` endpoint returns a list of collections without including all videos in each collection. This approach:
- Reduces response payload size
- Improves response time
- Aligns with the client app's "explore screen" which shows thematic rows

### Video Playback URLs

Playback URLs are included directly in the `/api/v1/videos/{video_id}` endpoint response rather than having a separate endpoint. This decision was made to:
- Simplify the client application logic (fewer API calls needed)
- Provide a more comprehensive video details response
- Follow common patterns in video API design

## Environment Variables

The application uses the following environment variables:

| Variable | Description | Default Value |
|----------|-------------|---------------|
| ARCHIVE_API_BASE_URL | The base URL for the Internet Archive API | https://archive.org/advancedsearch.php |

## Testing

Run the tests with:

```bash
python -m unittest discover tests
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Internet Archive](https://archive.org/) for providing the data and API
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework 


# Frontend

This is the frontend application, an web interface for Internet Archive.

## Prerequisites

- Node.js (version 14 or higher)
- npm (usually comes with Node.js)

## Installation

1. Clone the repository
2. Navigate to the web folder:
```bash
cd web
```

3. Install dependencies:
```bash
npm install
```

## Running the project

1. Make sure the Python API is running
2. Start the development server:
```bash
npm start
```

3. Open [http://localhost:3000](http://localhost:3000) in your browser

## Project Structure

- `src/components`: Reusable React components
- `src/pages`: Application pages
- `src/services`: API services and utilities
- `src/styles`: Global styles and themes

## Features

- Collection gallery view with pagination
- Video view by collection
- Video playback in modal
- Navigation between collections and videos 


# Front End Images

## Initial Page
![Texto alternativo](https://github.com/tsroliveira/InternetArchiveAPI/blob/master/InternetArchiveAPI/web/public/img/1_Initial_Explore_Page.png)

## Initial Page Pagination Footer
![Texto alternativo](https://github.com/tsroliveira/InternetArchiveAPI/blob/master/InternetArchiveAPI/web/public/img/2_Initial_Explore_Page_Pagination.png)

## Collection Video Navgate
![Texto alternativo](https://github.com/tsroliveira/InternetArchiveAPI/blob/master/InternetArchiveAPI/web/public/img/3_Collection_Video_Navgate.png)

## Video Detailed PopUp
![Texto alternativo](https://github.com/tsroliveira/InternetArchiveAPI/blob/master/InternetArchiveAPI/web/public/img/4_Video_Detailed_Popup.png)



