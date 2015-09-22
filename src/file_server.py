import os
import json
import http.server
import base64


HTTP_LISTEN_PORT = 80
HOSTING_PATH = "/var/www/hosting"

def _get_mounted_volumes():
    restart_args = json.loads(base64.b64decode(os.environ["RESTART_CONTAINER_PARAMETERS"]).decode('utf-8'))
    volumes = []

    for volume in restart_args['volumes']:
        if volume == '/var/run/docker.sock':
            continue

        volumes.append(restart_args['volumes'][volume])

    return volumes


def _generate_links_for_volumes(volumes):
    links = {}
    for volume in volumes:
        name = os.path.split(volume.rstrip('/'))[-1]
        links[name] = volume

    for link in links:
        os.symlink(links[link], link)


if __name__ == "__main__":
    os.makedirs(HOSTING_PATH, exist_ok=True)
    os.chdir(HOSTING_PATH)

    volumes = _get_mounted_volumes()
    if len(volumes) == 0:
        with open(os.path.join(HOSTING_PATH, 'NO SHARES PROVIDED.txt'), 'w') as f:
            f.write("Please specify what files you want to share with -v option to `armada run` command.")
    if len(volumes) == 1 and os.path.isdir(volumes[0]):
        os.chdir(volumes[0])
    else:
        _generate_links_for_volumes(volumes)

    http.server.test(HandlerClass=http.server.SimpleHTTPRequestHandler,port=HTTP_LISTEN_PORT,bind="")
