import os
import urllib.request

def download_fonts():
    # Create fonts directory if it doesn't exist
    if not os.path.exists('fonts'):
        os.makedirs('fonts')
    
    # Font URLs from Google Fonts
    fonts = {
        'DejaVuSansCondensed.ttf': 'https://fonts.gstatic.com/s/roboto/v30/KFOlCnqEu92Fr1MmWUlfBBc4AMP6lQ.woff2',
        'DejaVuSansCondensed-Bold.ttf': 'https://fonts.gstatic.com/s/roboto/v30/KFOlCnqEu92Fr1MmWUlfBBc4AMP6lQ.woff2'
    }
    
    # Download fonts
    for font_name, url in fonts.items():
        font_path = os.path.join('fonts', font_name)
        if not os.path.exists(font_path):
            print(f"Downloading {font_name}...")
            try:
                urllib.request.urlretrieve(url, font_path)
                print(f"Downloaded {font_name}")
            except Exception as e:
                print(f"Error downloading {font_name}: {str(e)}")
                print("Please download the fonts manually from:")
                print("1. Go to https://fonts.google.com/")
                print("2. Search for 'Roboto'")
                print("3. Download the Regular and Bold variants")
                print("4. Place them in the 'fonts' directory as:")
                print("   - DejaVuSansCondensed.ttf")
                print("   - DejaVuSansCondensed-Bold.ttf")

if __name__ == "__main__":
    download_fonts() 