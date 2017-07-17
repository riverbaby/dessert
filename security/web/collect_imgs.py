import re
import zlib

from scapy.all import *
from scapy.layers.inet import TCP

pictures_directory = "./pic"
pcap_file = "arper.pcap"
debug = False

def get_http_headers(http_payload):
    headers = []
    while True:
        # split the headers off if it is HTTP traffic
        start = http_payload.find("HTTP/1.1")
        if start is -1:
            return headers
        end = http_payload.find("\r\n\r\n")
        if end is -1:
            return headers
        headers_raw = http_payload[start:end+2]
        if debug:
            print("start: "+str(start))
            print("end: "+str(end))
            print(headers_raw)

        # break out the headers
        header = dict(re.findall(r"(?P<name>.*?): (?P<value>.*?)\r\n", headers_raw))
        if debug:
            print(header)
        if "Content-Length" in header.keys():
            len = int(header["Content-Length"])
            payload = http_payload[end+4:end+4+len]
        else:
            len = 0
            payload = ""

        headers.append({"header": header, "payload": payload})
        http_payload = http_payload[end+4+len:]

    return headers


def extract_image(header, payload):
    image = None
    image_type = None

    try:
        if "image" in header["Content-Type"]:
            # grab the image type and image body
            image_type = header["Content-Type"].split("/")[1]

            image = payload

            # if we detect compression decompress the image
            try:
                if "Content-Encoding" in header.keys():
                    print("encoding")
                    if header["Content-Encoding"] == "gzip":
                        image = zlib.decompress(image, 16+zlib.MAX_WBITS)
                    elif header["Content-Encoding"] == "deflate":
                        image = zlib.decompress(image)

            except:
                pass
    except:
        return None, None

    return image, image_type

def derepeat_packet(packetlist):
    sortlist = sorted(packetlist, key=lambda packet: packet.id)
    return sortlist

def http_assembler(pcap_file):
    carved_images = 0
    faces_detected = 0

    a = rdpcap(pcap_file)

    sessions = a.sessions()

    for session in sessions:
        http_payload = ""
        packetlist = derepeat_packet(sessions[session])
        ids = []
        for packet in packetlist:
            try:
                if (packet[TCP].sport == 80) and not (packet.id in ids):
                    # reassemble the stream
                    http_payload += str(packet[TCP].payload)
                    ids.append(packet.id)
            except:
                pass

        headers = get_http_headers(http_payload)

        if headers is []:
            continue

        for http in headers:
            image, image_type = extract_image(http["header"], http["payload"])

            if image is not None and image_type is not None:
                # store the image
                file_name = "%s-pic_carver_%d.%s" % \
                    (pcap_file, carved_images, image_type)

                fd = open("%s/%s" % (pictures_directory, file_name), "wb")

                fd.write(image)
                fd.close()

                carved_images += 1

    return carved_images, faces_detected

if __name__ == "__main__":
    carved_images, faces_detected = http_assembler(pcap_file)

    print("Extracted: %d images" % carved_images)
    print("Detected: %d faces" % faces_detected)
