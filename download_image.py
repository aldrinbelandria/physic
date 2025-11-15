import requests

def download_sample_image(width=32, height=32, filename="img.png"):
    url = f"https://images.unsplash.com/photo-1506744038136-46273834b3fb?w={width}&h={height}&fit=crop"
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"Imagen descargada como {filename}")
    else:
        print("Error al descargar la imagen:", response.status_code)

if __name__ == "__main__":
    download_sample_image(2, 2)
