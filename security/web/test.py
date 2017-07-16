import re
import zlib
import cv2

from scapy.all import *
from scapy.layers.inet import TCP

pictures_directory = "/Users/river/project/security/dessert/security/web/pictures"
faces_directory = "/Users/river/project/security/dessert/security/web/faces"
pcap_file = "arper.pcap"

def face_detect(path, file_name):
    img = cv2.imread(path)
    cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
    rects = cascade.detectMultiScale(img, 1.3, 4, cv2.cv.CV_HAAR_SCALE_IMAGE, (20,20))

    if len(rects) == 0:
        return False

    rects[:, 2:] += rects[:, :2]

    # highlight the faces in the image
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), (127, 255, 0), 2)

    cv2.imwrite("%s/%s-%s" % (faces_directory, pcap_file, file_name), img)

    return True


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
        print("start: "+str(start))
        print("end: "+str(end))
        print(headers_raw)

        # break out the headers
        header = dict(re.findall(r"(?P<name>.*?): (?P<value>.*?)\r\n", headers_raw))
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


def http_assembler(pcap_file):
    carved_images = 0
    faces_detected = 0

    a = rdpcap(pcap_file)

    sessions = a.sessions()

    for session in sessions:
        http_payload = ""
        for packet in sessions[session]:
            try:
                if packet[TCP].dport == 80 or packet[TCP].sport == 80:
                    # reassemble the stream
                    http_payload += str(packet[TCP].payload)

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

                print(file_name)
                fd = open("%s/%s" % (pictures_directory, file_name), "wb")

                fd.write(image)
                fd.close()

                carved_images += 1

                # now attempt face detection
                try:
                    result = face_detect("%s/%s" % (pictures_directory, file_name), file_name)

                    if result is True:
                        faces_detected += 1
                except:
                    pass
    return carved_images, faces_detected

if __name__ == "__main__":
    carved_images, faces_detected = http_assembler(pcap_file)

    print "Extracted: %d images" % carved_images
    print "Detected: %d faces" % faces_detected