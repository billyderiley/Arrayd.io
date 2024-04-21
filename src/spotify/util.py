import logging

def setup_logging():
    """Set up the application's logging configuration."""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def format_artist_names(artists):
    """Format the list of artist objects into a string of artist names."""
    return ', '.join(artist['name'] for artist in artists)

def convert_ms_to_min_seconds(milliseconds):
    """Convert milliseconds to a formatted string of minutes and seconds."""
    seconds = int((milliseconds / 1000) % 60)
    minutes = int((milliseconds / (1000 * 60)) % 60)
    return f"{minutes}m {seconds}s"