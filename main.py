from PIL import Image
from numpy import array, uint8
from math import log, floor, ceil


def text_to_binary(text):
    # Функция для преобразования текста в двоичное представление
    result = []
    for c in text:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result + [1] * 20


def binary_to_text(text):
    # Функция для преобразования двоичных данных в текст
    chars = []
    for b in range(len(text) // 8):
        byte = text[b * 8:(b + 1) * 8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)


def numerical_segment(number):
    # Функция для определения числового сегмента
    if 0 <= number <= 7:
        return [0, 7]
    if 8 <= number <= 15:
        return [8, 15]
    if 16 <= number <= 31:
        return [16, 31]
    if 32 <= number <= 63:
        return [32, 63]
    if 64 <= number <= 127:
        return [64, 127]
    if 128 <= number <= 255:
        return [128, 255]


def encode(pixels, message):
    # Функция для кодирования сообщения в пиксели изображения красного цветового канала
    width, height = img.size
    message = text_to_binary(message)
    iter_in_message = 0
    for i in range(0, len(pixels), 2):
        Pi = pixels[i][0]
        Pk = pixels[i + 1][0]
        value_difference = Pk - Pi
        can_be_built_in = int(log(
            numerical_segment(abs(value_difference))[1] - numerical_segment(abs(value_difference))[0] + 1, 2))
        fragment_of_the_message = []
        for k in range(can_be_built_in):
            if iter_in_message < len(message):
                fragment_of_the_message.append(message[iter_in_message])
                iter_in_message += 1
        fragment_of_the_message = int(''.join(map(str, fragment_of_the_message)), 2)

        if value_difference >= 0:
            value_difference_new = numerical_segment(abs(value_difference))[0] + fragment_of_the_message
        else:
            value_difference_new = -(numerical_segment(abs(value_difference))[0] + fragment_of_the_message)

        if value_difference % 2 == 1:
            P_new_i = Pi - ceil((value_difference_new - value_difference) / 2)
            P_new_k = Pk + floor((value_difference_new - value_difference) / 2)
        else:
            P_new_i = Pi - floor((value_difference_new - value_difference) / 2)
            P_new_k = Pk + ceil((value_difference_new - value_difference) / 2)

        pixels[i] = (P_new_i, pixels[i][1], pixels[i][2])
        pixels[i + 1] = (P_new_k, pixels[i + 1][1], pixels[i + 1][2])

        if iter_in_message >= len(message):
            break

    pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]
    new_image = Image.fromarray(array(pixels, dtype=uint8))
    new_image.save('out.png')


def decode(image):
    # Функция для декодирования скрытого сообщения из изображения
    message = []
    width, height = img.size

    # Извлечение данных из красного канала
    for i in range(0, len(pixels), 2):
        Pi = pixels[i][0]
        Pk = pixels[i + 1][0]
        value_difference = abs(Pk - Pi)
        can_be_built_in = int(log(
            numerical_segment(abs(value_difference))[1] - numerical_segment(abs(value_difference))[0] + 1, 2))

        fragment_of_the_message = value_difference - numerical_segment(abs(value_difference))[0]
        fragment_of_the_message = list(bin(fragment_of_the_message)[2:])
        fragment_of_the_message = [int(bit) for bit in fragment_of_the_message]
        for j in range(can_be_built_in - len(fragment_of_the_message)):
            message.append(0)
        for j in fragment_of_the_message:
            message.append(j)

        if len(message) > 15 and 0 not in message[-15:]:
            break
    print(binary_to_text(message)[:-2])


if __name__ == '__main__':
    with Image.open("Lenna.png") as img:
        pixels = list(img.getdata())
        encode(pixels, "hello!! It's a secret text.")
    with Image.open("out.png") as new_img:
        pixels = list(new_img.getdata())
        decode(pixels)