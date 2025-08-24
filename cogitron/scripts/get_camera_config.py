import cogitron

def main():
    camera_config = cogitron.camera.get_camera_config()
    print('"{ front: {type: opencv, index_or_path: ' + str(camera_config.index_or_path) \
          + ', width: ' + str(camera_config.width) + ', height: ' + str(camera_config.height) + ', fps: ' + str(camera_config.fps) + '}}"')

if __name__ == '__main__':
    main()