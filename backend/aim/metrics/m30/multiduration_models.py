# Standard library modules
from typing import Any, List, Tuple

# Third-party modules
import keras.backend as K
from keras.layers import (
    LSTM,
    Conv2D,
    Dense,
    GlobalAveragePooling2D,
    Input,
    Lambda,
    Layer,
    MaxPooling2D,
    Multiply,
    TimeDistributed,
    UpSampling2D,
)
from keras.models import Model

# First-party modules
from aim.metrics.m30.xception_custom import Xception_wrapper


def decoder_block_timedist(
    x: Layer, dil_rate: Tuple = (2, 2), dec_filt: int = 1024
) -> Layer:
    # Dilated convolutions
    x = TimeDistributed(
        Conv2D(
            dec_filt,
            3,
            padding="same",
            activation="relu",
            dilation_rate=dil_rate,
        )
    )(x)
    x = TimeDistributed(
        Conv2D(
            dec_filt,
            3,
            padding="same",
            activation="relu",
            dilation_rate=dil_rate,
        )
    )(x)
    x = TimeDistributed(UpSampling2D((2, 2), interpolation="bilinear"))(x)

    x = TimeDistributed(
        Conv2D(
            dec_filt // 2,
            3,
            padding="same",
            activation="relu",
            dilation_rate=dil_rate,
        )
    )(x)
    x = TimeDistributed(
        Conv2D(
            dec_filt // 2,
            3,
            padding="same",
            activation="relu",
            dilation_rate=dil_rate,
        )
    )(x)
    x = TimeDistributed(UpSampling2D((2, 2), interpolation="bilinear"))(x)

    x = TimeDistributed(
        Conv2D(
            dec_filt // 4,
            3,
            padding="same",
            activation="relu",
            dilation_rate=dil_rate,
        )
    )(x)
    x = TimeDistributed(
        Conv2D(
            dec_filt // 4,
            3,
            padding="same",
            activation="relu",
            dilation_rate=dil_rate,
        )
    )(x)
    x = TimeDistributed(UpSampling2D((4, 4), interpolation="bilinear"))(x)

    # Final conv to get to a heatmap
    x = TimeDistributed(
        Conv2D(1, kernel_size=1, padding="same", activation="relu")
    )(x)

    return x


def xception_se_lstm(
    input_shape: Tuple = (240, 320, 3),
    conv_filters: int = 256,
    lstm_filters: int = 512,
    verbose: bool = True,
    n_outs: int = 1,
    ups: int = 8,
    freeze_enc: bool = False,
    return_sequences: bool = True,
    **kwargs,
) -> Model:
    inp: Input = Input(shape=input_shape)

    ### ENCODER ###
    xception: Model = Xception_wrapper(
        include_top=False, weights="imagenet", input_tensor=inp, pooling=None
    )

    if freeze_enc:
        for layer in xception.layers:
            layer.trainable = False

    ### LSTM over SE representation ###
    x: Layer = se_lstm_block_timedist(
        xception.output,
        nb_timestep=3,
        lstm_filters=lstm_filters,
        return_sequences=return_sequences,
    )

    ### DECODER ###
    outs_dec: Layer = decoder_block_timedist(
        x, dil_rate=(2, 2), dec_filt=conv_filters
    )

    outs_final: List[Layer] = [outs_dec] * n_outs
    m: Model = Model(inp, outs_final)
    if verbose:
        m.summary()
    return m


def se_lstm_block_timedist(
    inp: Model,
    nb_timestep: int,
    units: int = 512,
    lstm_filters: int = 512,
    return_sequences: bool = True,
) -> Layer:

    inp_rep: Layer = Lambda(
        lambda y: K.repeat_elements(
            K.expand_dims(y, axis=1), nb_timestep, axis=1
        ),
        lambda s: (s[0], nb_timestep) + s[1:],
    )(inp)
    x: Layer = TimeDistributed(GlobalAveragePooling2D())(inp_rep)
    x = TimeDistributed(Dense(units, activation="relu"))(x)

    # Normally se block would feed into another fully connected. Instead, we feed it to an LSTM.
    x = LSTM(
        lstm_filters,
        return_sequences=return_sequences,
        unroll=True,
        activation="relu",
    )(x)
    x = TimeDistributed(Dense(inp.shape[-1].value, activation="sigmoid"))(x)

    x = Lambda(
        lambda y: K.expand_dims(K.expand_dims(y, axis=2), axis=2),
        lambda s: (s[0], s[1], 1, 1, s[2]),
    )(x)

    # x is (bs, t, 1, 1, 2048)
    # inp_rep is (bs, t, r, c, 2048)
    out: Layer = Multiply()([x, inp_rep])
    # out is (bs, t, r, c, 2048)

    return out


def xception_se_lstm_nodecoder(
    input_shape=(240, 320, 3),
    nb_timestep=3,
    conv_filters=512,
    lstm_filters=512,
    verbose=True,
    n_outs=1,
    ups=8,
    freeze_enc=False,
    return_sequences=True,
) -> Model:
    inp: Input = Input(shape=input_shape)

    ### ENCODER ###
    xception: Model = Xception_wrapper(
        include_top=False, weights="imagenet", input_tensor=inp, pooling=None
    )
    if freeze_enc:
        for layer in xception.layers:
            layer.trainable = False

    ### LSTM over SE representation ###
    x: Layer = se_lstm_block_timedist(
        xception.output,
        nb_timestep,
        lstm_filters=lstm_filters,
        return_sequences=return_sequences,
    )

    ### DECODER ###
    dil_rate: Tuple = (2, 2)
    x = TimeDistributed(
        Conv2D(
            conv_filters,
            3,
            padding="same",
            activation="relu",
            dilation_rate=dil_rate,
        )
    )(x)
    x = TimeDistributed(
        Conv2D(
            conv_filters,
            3,
            padding="same",
            activation="relu",
            dilation_rate=dil_rate,
        )
    )(x)
    # outs_dec = TimeDistributed(UpSampling2D((2,2), interpolation='bilinear'))(x)
    outs_dec: Layer = TimeDistributed(MaxPooling2D((4, 4)))(x)

    # x = TimeDistributed(Dropout(0.3))(x)
    # x = TimeDistributed(Conv2D(filters=conv_filters, kernel_size=3, padding='same', activation='relu'))(x)
    # x = TimeDistributed(Dropout(0.3))(x)
    # x = TimeDistributed(Conv2D(1, kernel_size=1, padding='same', activation='relu'))(x)
    # outs_dec = TimeDistributed(UpSampling2D(size=(ups,ups), interpolation='bilinear'))(x)
    # outs_final = [outs_dec]*n_outs

    m: Model = Model(inp, outs_dec)
    if verbose:
        m.summary()
    return m
