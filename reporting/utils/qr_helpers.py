import qrcode
import uuid
from django.conf import settings
from pathlib import Path

def generate_qr_code(content: str, filename_prefix: str = "receipt") -> str:
    """
    Generates a QR code PNG file and returns its absolute path.
    """
    filename = f"{filename_prefix}_{uuid.uuid4().hex}.png"
    output_path = Path(settings.MEDIA_ROOT) / "temp_qr" / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=4,
        border=2,
    )
    qr.add_data(content)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_path)

    return str(output_path)
