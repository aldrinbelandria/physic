import requests

def download_sample_image(width=32, height=32):
    url = f"https://images.unsplash.com/photo-1506744038136-46273834b3fb?w={width}&h={height}&fit=crop"
    response = requests.get(url)
    file_name = f"img_{width}x{height}.png"
    if response.status_code == 200:
        with open(file_name, "wb") as f:
            f.write(response.content)
        print(f"Imagen descargada como {file_name}")
    else:
        print("Error al descargar la imagen:", response.status_code)

if __name__ == "__main__":
    download_sample_image(64, 64)
