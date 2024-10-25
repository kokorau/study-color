import json
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


# データの読み込み
def load_data(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return np.array(data)  # NumPy配列に変換


# VAEモデルの構築
def build_vae(input_shape):
    # エンコーダー
    inputs = keras.Input(shape=input_shape)
    x = layers.Flatten()(inputs)
    x = layers.Dense(64, activation='relu')(x)
    z_mean = layers.Dense(32)(x)
    z_log_var = layers.Dense(32)(x)

    # 再パラメータ化トリック
    def sampling(args):
        z_mean, z_log_var = args
        epsilon = tf.random.normal(tf.shape(z_mean))
        return z_mean + tf.exp(0.5 * z_log_var) * epsilon

    z = layers.Lambda(sampling)([z_mean, z_log_var])

    # デコーダー
    decoder_input = layers.Input(shape=(32,))
    x = layers.Dense(64, activation='relu')(decoder_input)
    x = layers.Dense(np.prod(input_shape), activation='sigmoid')(x)
    outputs = layers.Reshape(input_shape)(x)

    encoder = keras.Model(inputs, [z_mean, z_log_var, z], name='encoder')
    decoder = keras.Model(decoder_input, outputs, name='decoder')

    # VAEモデル
    outputs = decoder(encoder(inputs)[2])
    vae = keras.Model(inputs, outputs, name='vae')

    # 損失関数の定義
    reconstruction_loss = keras.losses.binary_crossentropy(inputs, outputs) * np.prod(input_shape)
    kl_loss = -0.5 * tf.reduce_mean(z_log_var - tf.square(z_mean) - tf.exp(z_log_var) + 1)
    vae_loss = tf.reduce_mean(reconstruction_loss + kl_loss)

    vae.add_loss(vae_loss)
    return vae, encoder, decoder


# モデルの訓練
def train_vae(data, epochs=50, batch_size=128):
    input_shape = data.shape[1:]  # (高さ, 幅, チャンネル数)
    vae, encoder, decoder = build_vae(input_shape)

    vae.compile(optimizer='adam')
    vae.fit(data, data, epochs=epochs, batch_size=batch_size)

    return encoder, decoder


# メイン処理
if __name__ == "__main__":
    data_path = '../data/processed/train_oklchPalette.json'  # 訓練データのファイルパス
    data = load_data(data_path)

    # VAEモデルを訓練
    encoder, decoder = train_vae(data)

    # モデルの保存
    encoder.save('models/vae_encoder.h5')
    decoder.save('models/vae_decoder.h5')
