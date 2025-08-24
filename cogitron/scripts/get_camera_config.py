import cogitron

def main():
    camera_config = cogitron.camera.get_camera_config()
    print("{ front: {type: opencv, index_or_path: " + camera_config.index_or_path \
          + ", width: " + camera_config.width + ", height: " + camera_config.height + ", fps: " + camera_config.fps + "}}")

if __name__ == '__main__':
    main()