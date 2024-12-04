import random
import math
from sympy import isprime, mod_inverse

def main():
    display_list()
    
    # ビット長を入力
    bit_length = int(input("鍵のビット長を入力してください: "))
    
    # 鍵生成
    public_key, private_key = generate_keys(bit_length)

    # ユーザーからメッセージを標準入力で受け取る
    message = input("暗号化したいメッセージを入力してください: ")

    # メッセージを数値に変換
    number = message_to_number(message)
    if number >= public_key[1]:  # n より大きな数値は暗号化できない
        print("メッセージが長すぎます。")
        return

    # 数値を暗号化
    encrypted_number = encrypt_number(number, public_key)

    # 暗号化された数値を文字列に変換
    encrypted_message = number_to_message(encrypted_number)
    print("\n暗号文:")
    print(encrypted_message)

    # 暗号化された数値を復号化
    decrypted_number = decrypt_number(encrypted_number, private_key)

    # 復号化された数値をメッセージに変換
    decrypted_message = number_to_message(decrypted_number)
    print("\n復号化されたメッセージ:")
    print(decrypted_message)


def display_list():
    # 使用可能な文字のリストを表示
    print("\n==================================================================== 使用可能な文字 ==================================================================")
    print(' '.join(character))
    print("======================================================================================================================================================\n")

# 素数を生成
def generate_prime_candidate(length):
    p = random.getrandbits(length)
    if p % 2 == 0:
        p += 1
    return p

def generate_prime_number(length):
    p = generate_prime_candidate(length)
    while not isprime(p):
        p = generate_prime_candidate(length)
    return p

# 最小公倍数を計算
def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)

# 鍵を生成
def generate_keys(bit_length):
    p = generate_prime_number(bit_length)
    q = generate_prime_number(bit_length)
    n = p * q
    L = lcm(p-1, q-1)  # 最小公倍数を計算

    e = 65537
    d = mod_inverse(e, L)
    
    return ((e, n), (d, n))

# 文字と数値のマッピング
character = list('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!?#$%&"\'\\+*/. ')
char_to_value = {char: idx for idx, char in enumerate(character)} #文字から数字の割り当て
value_to_char = {idx: char for char, idx in char_to_value.items()} #数字から文字の割り当て

# メッセージを数値に変換
def message_to_number(message):
    base = len(character)
    number = 0
    
    # 文字列を逆順に処理（最下位桁から順に計算）
    for idx, char in enumerate(reversed(message)):
        # 文字を数値に変換
        char_value = char_to_value[char]
        
        # 基数のべき乗を計算
        power = base ** idx
        
        # 数値を加算
        number += char_value * power
    return number

# 数値をメッセージに変換
def number_to_message(number):
    base = len(character)  # 使用する基数を設定（アルファベットの長さ）
    if number == 0:
        return value_to_char[0]  # 数値が0の場合、対応する文字を返す
    
    message = []  # メッセージを空のリストとして設定

    while number > 0:
        number, remainder = divmod(number, base)  # 基数で割り算し、商と余りを取得
        message.insert(0, value_to_char[remainder])  # 余りを文字に変換し、メッセージの先頭に追加
    return ''.join(message)  # リストを文字列に結合して返す

# 暗号化関数
def encrypt_number(number, public_key):
    e, n = public_key
    return pow(number, e, n)

# 復号化関数
def decrypt_number(number, private_key):
    d, n = private_key
    return pow(number, d, n)

if __name__ == "__main__":
    main()
