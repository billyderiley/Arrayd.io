#from src.spotify.main import main as spotify_main
import src.spotify.main as spotify_main
from src.audio_analysis.main import run_audio_analysis
#from src.audio_analysis.

def main():
    # Run Spotify operations
    #spotify_data = run_spotify_operations()
    spotify_main.main()

    # Run audio analysis
    #analysis_results = run_audio_analysis(spotify_data)

    # Any other operations that tie together results from both

if __name__ == "__main__":
    main()