import os
import subprocess
import sys

# 必要なパッケージを確認し、インストールする
required_packages = ["chardet"]
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

import chardet # ここで改めてインポート
import codecs

def convert_to_utf8(file_path):
    # ファイルをバイナリモードで読み込み、文字コードを検出
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        encoding = chardet.detect(raw_data)['encoding']

    # 文字コードが既にUTF-8 BOMの場合はスキップ
    if encoding != 'utf-8':
        # ファイルの内容をデコードし、UTF-8 でエンコード
        try:
            decoded_data = raw_data.decode(encoding)
            encoded_data = codecs.BOM_UTF8 + decoded_data.encode('utf-8')
            
            # 変換したデータを同じファイルに書き込む
            with open(file_path, 'wb') as f:
                f.write(encoded_data)
        except UnicodeDecodeError:
            print(f"Unicode decode error in file {file_path}, skipping...")
        except UnicodeEncodeError:
            print(f"Unicode encode error in file {file_path}, skipping...")
        except TypeError:
            print(f"Type error in file {file_path}, skipping...")
        except Exception as e:
            print(f"Error converting file {file_path}: {e}")

def main():
    # スクリプトがあるディレクトリを取得
    root_dir = os.path.dirname(os.path.abspath(__file__))

    # 再帰的にフォルダ内のファイルをリストアップ
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            # ファイルのフルパスを取得
            file_path = os.path.join(root, file)
            # UTF-8に変換
            convert_to_utf8(file_path)

if __name__ == '__main__':
    main()
