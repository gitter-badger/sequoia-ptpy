'''Master module that instantiates the correct extension and transport.'''
# Extensions
from canon import PTPDevice as canon
from microsoft import PTPDevice as mtp
from parrot import PTPDevice as parrot
from ptp import PTPDevice as ptp

from usb_transport import USBTransport as usb


class PTPyError(Exception):
    pass

# As extensions are implemented, they should be added here, so they are
# automatically used. The names here need to match those in ptp.py
# VendorExtensionID.
known_extensions = {
    'EastmanKodak': None,
    'SeikoEpson': None,
    'Agilent': None,
    'Polaroid': None,
    'AgfaGevaert': None,
    'Microsoft': mtp,
    'Equinox': None,
    'Viewquest': None,
    'STMicroelectronics': None,
    'Nikon': None,
    'Canon': canon,
    'FotoNation': None,
    'PENTAX': None,
    'Fuji': None,
    'Sony': None,
    'Samsung': None,
    'Parrot': parrot,
}


def ptpy_factory(transport, extension=None):
    # The order needs to be Transport inherits Extension inherits Base. This is
    # so that the extension can extend the base and the transport can
    # instantiate the correct endianness.
    inheritance = ((transport, extension, ptp, object)
                   if extension is not None
                   else (transport, ptp, object))
    return type('PTPy', inheritance, {})


# TODO: Add other transports?
transport = usb
# Attempt to instantiate simple device and get its information. Then terminate
# it.

PTPy = ptpy_factory(transport)
device = PTPy()
if device is not None:
    # TODO: Do this at each instantiation of PTPy instead of just once. This
    # workd OK for a single device but is not ideal.
    device_info = device.get_device_info()
    device._shutdown()
    PTPy = ptpy_factory(
        transport,
        known_extensions[device_info.VendorExtensionID]
    )

# TODO: Add a raw option to get a pure PTP device, and default to a smart
# device that manages properties automatically.
