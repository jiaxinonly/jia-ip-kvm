import yaml


class Config:
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
        secret_key = config['secret']['key']
        username = config['secret']['username']
        password = config['secret']['password']
        video_index = config['device']['video']['index']
        video_fps = config['device']['video']['frame']['fps']
        video_height = config['device']['video']['frame']['height']
        video_width = config['device']['video']['frame']['width']
        hid_port = config['device']['hid']['port']
        baudrate = config['device']['hid']['baudrate']
        mac = config['device']['mac']
