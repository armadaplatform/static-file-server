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
    def find_unique_key(dictionary, key, is_file=False):
        if key not in dictionary:
            return key
        
        prefix, suffix = os.path.splitext(key) if is_file else (key, '')
        counter = 1
        
        while (prefix + str(counter) + suffix) in dictionary:
            counter += 1
        
        return "{prefix}_{counter}{suffix}".format(**locals())
        
    links = {}
    for volume in volumes:
        name = os.path.split(volume.rstrip('/'))[-1]
        link_target = find_unique_key(links, name, os.path.isfile(volume))
        links[link_target] = volume
    
    for link in links:
        os.symlink(links[link], link)


if __name__ == "__main__":
    os.makedirs(HOSTING_PATH, exist_ok=True)
    os.chdir(HOSTING_PATH)
    
    volumes = _get_mounted_volumes()
    if len(volumes) == 0:
        raise RuntimeError('No volumes provided')
    if len(volumes) == 1 and os.path.isdir(volumes[0]):
        os.chdir(volumes[0])
    else:
        _generate_links_for_volumes(volumes)
    
    http.server.test(HandlerClass=http.server.SimpleHTTPRequestHandler,port=HTTP_LISTEN_PORT,bind="")
