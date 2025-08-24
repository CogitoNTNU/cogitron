import cogitron

def main():
    follower_port=cogitron.arms.get_arm_ports()[0]
    print(follower_port)

if __name__ == '__main__':
    main()