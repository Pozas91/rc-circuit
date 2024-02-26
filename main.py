from RPi import GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

mode = GPIO.getmode()

print(mode)


def main():
    print("Hello, World!")


if __name__ == "__main__":
    main()
