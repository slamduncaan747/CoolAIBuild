import requests
import pygame
import tempfile
import os

def generate_and_stream_audio(text):
    api_key = 'ebc13dfa297853586372a1acf0b80c1b'  # Replace 'YOUR_API_KEY' with your actual ElevenLabs API key
    voice_id = 'pNInz6obpgDQGcFmaJgB'  # Replace 'YOUR_VOICE_ID' with the ID of the desired voice
    url = f'https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream'

    headers = {
        'Accept': 'audio/mpeg',
        'Content-Type': 'application/json',
        'xi-api-key': api_key
    }

    data = {
        'text': text,
        'model_id': 'eleven_monolingual_v1',
        'voice_settings': {
            'stability': 0.4,
            'similarity_boost': 0.77
        }
    }

    response = requests.post(url, json=data, headers=headers, stream=True)

    if response.status_code == 200:
        # Save the audio as a temporary file
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_audio:
            for chunk in response.iter_content(chunk_size=1):
                temp_audio.write(chunk)

        # Create a Pygame mixer to handle audio playback
        pygame.mixer.init()
        pygame.mixer.music.load(temp_audio.name)
        pygame.mixer.music.play()

        # Wait for the audio to finish playing
        while pygame.mixer.music.get_busy():
            pass

        # Close the Pygame mixer and delete the temporary file
        pygame.mixer.quit()
        os.remove(temp_audio.name)

    else:
        print(f'Error: {response.status_code}')

# Example usage:
message = "Hi! This is a sample message. I am now gonna ramble on and on to test the speed of the sound development. i dont care about this text, i just want to see how quickly large amounts of text can be processed."
generate_and_stream_audio(message)
