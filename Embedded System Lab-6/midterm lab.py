import RPi.GPIO as GPIO
import time

SDI_PORT_1_PIN = 29
RCLK1_PIN = 12
SRCLK_PORT_1_PIN = 31
SRCLK_PORT_2_PIN = 37
RCLK2_PIN = 16
SRCLK_PORT_2_PIN = 35

ALPHABET_CODE = [0x77, 0x7C, 0x58, 0x5E, 0x79, 0x71, 0x6F, 0x74, 0x06, 0x0E, 0x70, 0x38, 0x37, 0x54, 0x5C, 0x73,
             0x67, 0x50, 0x6D, 0x78, 0x1C, 0x62, 0x36, 0x52, 0x72, 0x43]
def TEXT_PRINT():
    print('Program is running...')
    print('Please press Ctrl+C to exit the program...')
def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(SDI_PORT_1_PIN, GPIO.OUT)
    GPIO.setup(RCLK1_PIN, GPIO.OUT)
    GPIO.setup(SRCLK_PORT_1_PIN, GPIO.OUT)
    GPIO.output(SDI_PORT_1_PIN, GPIO.LOW)
    GPIO.output(RCLK1_PIN, GPIO.LOW)
    GPIO.output(SRCLK_PORT_1_PIN, GPIO.LOW)

    GPIO.setup(SRCLK_PORT_2_PIN, GPIO.OUT)
    GPIO.setup(RCLK2_PIN, GPIO.OUT)
    GPIO.setup(SRCLK_PORT_2_PIN, GPIO.OUT)
    GPIO.output(SRCLK_PORT_2_PIN, GPIO.LOW)
    GPIO.output(RCLK2_PIN, GPIO.LOW)
    GPIO.output(SRCLK_PORT_2_PIN, GPIO.LOW)
def hc595_shift(DATA1, sdi, rclk, srclk):
    for bit in range(0, 8):
        GPIO.output(sdi, 0x80 & (DATA1 << bit))
        GPIO.output(srclk, GPIO.HIGH)
        time.sleep(0.003)
        GPIO.output(srclk, GPIO.LOW)
    GPIO.output(rclk, GPIO.HIGH)
    time.sleep(0.03)
    GPIO.output(rclk, GPIO.LOW)





def string(sentence_text):
    pair_of_string = [("", sentence_text[0])]

    for i in range(1, len(sentence_text)):
        pair = (sentence_text[i - 1], sentence_text[i])

        pair_of_string.append(pair)

    pair_of_string.append((sentence_text[-1], ""))
    pair_of_string.append(("", ""))

    return pair_of_string


def display(popup_msg):
    pair_words = string(popup_msg)

    for pair in pair_words:

        text1 = pair[0]
        text2 = pair[1]

        if text1.isalpha():
            index_charec = ord(text1.upper()) - ord('A')

            if 0 <= index_charec < len(ALPHABET_CODE):
                hc595_shift(ALPHABET_CODE[index_charec], SDI_PORT_1_PIN, RCLK1_PIN, SRCLK_PORT_1_PIN)

        else:
            hc595_shift(0x00, SDI_PORT_1_PIN, RCLK1_PIN, SRCLK_PORT_1_PIN)


        if text2.isalpha():
            index_charec = ord(text2.upper()) - ord('A')
            if 0 <= index_charec < len(ALPHABET_CODE):
                hc595_shift(ALPHABET_CODE[index_charec], SRCLK_PORT_2_PIN, RCLK2_PIN, SRCLK_PORT_2_PIN)

        else:
            hc595_shift(0x00, SRCLK_PORT_2_PIN, RCLK2_PIN, SRCLK_PORT_2_PIN)
        time.sleep(0.4)


def loop():
    while True:
        display('hi you did good job')
        time.sleep(0.4)


def destroy():
    GPIO.cleanup()


if __name__ == '__main__':
    TEXT_PRINT()
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
