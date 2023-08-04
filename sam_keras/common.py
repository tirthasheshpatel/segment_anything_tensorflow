# Author: Tirth Patel (tirthasheshpatel@gmail.com)

# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.

# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

from keras_cv.backend import keras


@keras.utils.register_keras_serializable(package="keras_cv")
class MLPBlock(keras.layers.Layer):
    def __init__(self, embedding_dim, mlp_dim, activation="gelu", **kwargs):
        """A MLP block with architecture
        `embedding_dim -> mlp_dim -> embedding_dim`.

        Args:
            embedding_dim (int): The number of units in the input and the
                output layer.
            mlp_dim (int): The number of units in the hidden layer.
            activation (str, optional): The activation of the output.
                Defaults to "gelu".
        """
        super().__init__(**kwargs)
        self.dense_layer1 = keras.layers.Dense(mlp_dim)
        self.dense_layer2 = keras.layers.Dense(embedding_dim)
        self.activation_layer = keras.layers.Activation(activation)

        self.embedding_dim = embedding_dim
        self.mlp_dim = mlp_dim
        self.activation = activation

        self.built = False

        self.dense_layer1.build([self.embedding_dim])
        self.dense_layer2.build([self.mlp_dim])

        self.built = True

    def call(self, x):
        return self.dense_layer2(self.activation_layer(self.dense_layer1(x)))

    def get_config(self):
        config = super().get_config()
        config.update(
            {
                "embedding_dim": self.embedding_dim,
                "mlp_dim": self.mlp_dim,
                "activation": self.activation,
            }
        )