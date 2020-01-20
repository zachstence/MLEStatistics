import requests
import json
import sys
import argparse

def read_token(token_file):
    with open(token_file, 'r') as f:
        token = f.readline()
    return token

def get_stats(token, replay, visibility, output):
    upload_url = f'https://ballchasing.com/api/v2/upload?visibility={visibility}'
    r = requests.post(
        upload_url,
        headers={'Authorization': token},
        files={'file': open(replay, 'rb')}
    )

    response = json.loads(r.text)
    error = response['error'] if 'error' in response else None
    replay_id = response['id']
    url = response['location']

    if error == None:
        print('Replay successfully uploaded')
    elif error == 'duplicate replay':
        print('Replay already uploaded to BallChasing.com')
    else:
        print(f'Error uploading replay: {error}')

    print(f'Replay ID: {replay_id}')
    print(f'Replay URL: {url}')

    download_url = f'https://ballchasing.com/api/replays/{replay_id}'

    r = requests.get(
        download_url,
        headers={'Authorization': token}
    )
    stats = r.text

    with open(output, 'w+') as f:
        # f.write(stats)
        f.write(json.dumps(json.loads(stats), indent=2))
    
    print(f'BallChasing stats written to {output}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Automatically upload Rocket League replays to BallChasing.com and download their stats!')
    parser.add_argument('token', help='a BallChasing.com API token')
    parser.add_argument('replay', help='the filepath of the replay to upload')
    parser.add_argument('-v', '--visibility', help='the visibility of the uploaded replay on BallChasing.com, acceptable values are \'public\', \'unlisted\', \'private\'')
    parser.add_argument('-o', '--output', help='the filepath of the output json')
    args = parser.parse_args()
    
    if args.visibility == None:
        args.visibility = 'private'
    if args.output == None:
        args.output = 'out.json'

    get_stats(args.token, args.replay, args.visibility, args.output)
