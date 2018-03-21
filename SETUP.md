Control demo of evolv DNA Series by Python
===
# セットアップ

Raspberry Piの準備
---
- 開発では、Raspberry Pi 3 modelB を使用しております。
- OSは、Rasbian ( 2017-11-29-raspbian-stretch-lite )を使用しております。
- 適当なSDカードへインストール後、アップデートし、ネットワーク接続が有効な状態までセットアップを完了してください。
- 本デモでは、LED制御の為、rootで動作させております。
- ディレクトリは、「/data」、及び「/ramdisk」を使用します。別ディレクトリへ設置する場合、スクリプト内の変数を変更して下さい。
- 「/ramdisk」は、リモコン制御用ファイル設置に使用します。tmpfsにて、RAMDISKを設置することをお勧めします。容量は1MBあれば充分です。

ハードウェアの準備
---
- ハードウェアPWM制御有効化
```
Adafruit RGB MATRIX HAT上の「GPIO4」と「GPIO18」を接続
```
- 赤外線受光部の接続
```
Adafruit RGB MATRIX HAT上の「GPIO25」に、赤外線受光部のOUTPUTを接続
＊電源が汚れている為、赤外線受光部の動作が不安定な場合があります。
＊赤外線受光部のデータシートを参照し、フィルタ回路を追加することをお勧めします。
```

DNA接続設定
---
- cuをセットアップ
```
apt-get install cu
```
- シリアルコンソールの削除
```
/boot/config.txt : 「console=serial0,115200」を削除
リブート
```
- rootのシリアル接続許可
```
/etc/group : rootを「dialout」に追加
```
- DNAを接続、dmesgを確認
```
[  104.823036] usb 1-1.4: new full-speed USB device number 4 using dwc_otg
[  104.966377] usb 1-1.4: New USB device found, idVendor=268b, idProduct=0408
[  104.966399] usb 1-1.4: New USB device strings: Mfr=2, Product=3, SerialNumber=1
[  104.966409] usb 1-1.4: Product: Evolv DNA 75
[  104.966418] usb 1-1.4: Manufacturer: Dimension Engineering
[  104.966428] usb 1-1.4: SerialNumber: JXYTVJAYTNVG
[  104.998336] hid-generic 0003:268B:0408.0001: hiddev0,hidraw0: USB HID v1.10 Device [Dimension Engineering Evolv DNA 75] on usb-20980000.usb-1.4/input0
[  105.113838] cdc_acm 1-1.4:1.1: ttyACM0: USB ACM device
[  105.133105] usbcore: registered new interface driver cdc_acm
[  105.133119] cdc_acm: USB Abstract Control Model driver for USB modems and ISDN adapters
```
cdc_acmドライバ応答、「ttyACM0」が、DNAのデバイス名です。
/devディレクトリに該当のデバイスがあるか、確認して下さい。
- cuによるDNA接続確認
```
cu -l /dev/ttyACM0 -s 115200
「Connected.」確認
B=GET[enter]を打って、バッテリー電圧っぽいのが帰ってくることを確認
~.で抜ける
```

MATRIX LEDライブラリの準備
---
ソースは、https://github.com/hzeller/rpi-rgb-led-matrix　にあります。
詳細は、上記サイトをご参照下さい。
```
apt-get install git

mkdir /data
mkdir /data/source
cd /data/source
git clone https://github.com/hzeller/rpi-rgb-led-matrix.git
cd cd rpi-rgb-led-matrix/
make

apt-get install python2.7-dev python-pillow -y

cd /data/source/rpi-rgb-matrix/bindings/python
make
make install

/boot/config.txt 更新
dtparam=audio=off
```

赤外線リモコンの準備
---
以下のURLの記事を参考にしました。

http://www.neko.ne.jp/~freewing/raspberry_pi/raspberry_pi_stretch_lirc_ir_remote_control_2017/
```
apt-get install lirc

/etc/lirc/lirc_options.conf を編集
driver          = default
device          = /dev/lirc0

/boot/config.txt を編集
#RemoteController
dtoverlay=lirc-rpi
dtparam=gpio_in_pin=25

mv /etc/lirc/lircd.conf.d/devinput.lircd.conf /etc/lirc/lircd.conf.d/devinput.lircd.conf,disable

/lirc/appleremote.lircd.conf を、 /etc/lirc/lircd.conf.d/ にコピー
/lirc/lircrc を、 /etc/lirc/ にコピー
/systemd/rcexec.service を、 /etc/systemd/system/ にコピー

systemdに登録
systemctl enable lircd
systemctl enable irexec

正常動作の場合、リモコンのボタンを押すと、「/ramdisk」に、「rcdata」が出来ます。
```

スクリプトの準備
---
```
apt-get install python-pip
pip install numpy
＊超時間かかる
pip install pyserial

/*.py と、 /rckick を、 /data/dnainfo にコピー
/systemd/dnainfo.service を、 /etc/systemd/system/ にコピー
```

コンソール上での、スクリプト動作確認
---
```
DNAを接続した状態で、以下コマンドを実行
cd /data/dnainfo
python ./dnainfodemo.py

パフ時、以下のような情報が流れれば、DNA接続部は動作しています。
6.81W  285.86F  1.285V  4.965A  0.252ohm  BAT: 3.87V  MEAS WATT: 6.380025W
6.47W  285.01F  1.246V  4.916A  0.252ohm  BAT: 3.88V  MEAS WATT: 6.125336W
6.84W  283.87F  1.349V  5.255A  0.252ohm  BAT: 3.87V  MEAS WATT: 7.088995W
7.37W  283.88F  1.359V  5.207A  0.252ohm  BAT: 3.86V  MEAS WATT: 7.076313W
7.67W  285.25F  1.335V  5.037A  0.253ohm  BAT: 3.86V  MEAS WATT: 6.724395W

[CTRL+C]で抜けられます。
```

サービス登録
```
systemctl start dnainfo
＊LEDに表示が出れば成功です。

Raspberry Pi 起動時に自動起動するには、以下コマンドを投入して下さい。
systemctl enable dnainfo

動作停止は、以下コマンドです。
systemctl stop dnainfo
systemctl disable dnainfo
```
