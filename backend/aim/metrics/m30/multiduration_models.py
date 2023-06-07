from keras.layers import Input, Multiply, TimeDistributed, LSTM, Lambda, Conv2D, Dense, GlobalAveragePooling2D, MaxPooling2D, UpSampling2D
import keras.backend as K
from keras.models import Model
from aim.metrics.m30.xception_custom import Xception_wrapper


def decoder_block_timedist(x, dil_rate=(2,2), print_shapes=False, dec_filt=1024):
    # Dilated convolutions
    x = TimeDistributed(Conv2D(dec_filt, 3, padding='same', activation='relu', dilation_rate=dil_rate))(x)
    x = TimeDistributed(Conv2D(dec_filt, 3, padding='same', activation='relu',  dilation_rate=dil_rate))(x)
    x = TimeDistributed(UpSampling2D((2,2), interpolation='bilinear'))(x)

    x = TimeDistributed(Conv2D(dec_filt//2, 3, padding='same', activation='relu',  dilation_rate=dil_rate))(x)
    x = TimeDistributed(Conv2D(dec_filt//2, 3, padding='same', activation='relu',  dilation_rate=dil_rate))(x)
    x = TimeDistributed(UpSampling2D((2,2), interpolation='bilinear'))(x)

    x = TimeDistributed(Conv2D(dec_filt//4, 3, padding='same', activation='relu',  dilation_rate=dil_rate))(x)
    x = TimeDistributed(Conv2D(dec_filt//4, 3, padding='same', activation='relu',  dilation_rate=dil_rate))(x)
    x = TimeDistributed(UpSampling2D((4,4), interpolation='bilinear'))(x)
    if print_shapes: print('Shape after last ups:',x.shape)

    # Final conv to get to a heatmap
    x = TimeDistributed(Conv2D(1, kernel_size=1, padding='same', activation='relu'))(x)
    if print_shapes: print('Shape after 1x1 conv:',x.shape)

    return x


def xception_se_lstm(input_shape = (240, 320, 3),
                     conv_filters=256,
                     lstm_filters=512,
                     verbose=True,
                     print_shapes=False,
                     n_outs=1,
                     ups=8,
                     freeze_enc=False,
                     return_sequences=True,
                     **kwargs):
    inp = Input(shape = input_shape)

    ### ENCODER ###
    xception = Xception_wrapper(include_top=False, weights='imagenet', input_tensor=inp, pooling=None)
    if print_shapes: print('xception output shapes:',xception.output.shape)
    if freeze_enc:
        for layer in xception.layers:
            layer.trainable = False

    ### LSTM over SE representation ###
    x = se_lstm_block_timedist(xception.output, nb_timestep = 3, lstm_filters=lstm_filters, return_sequences=return_sequences)

    ### DECODER ###
    outs_dec = decoder_block_timedist(x, dil_rate=(2,2), print_shapes=print_shapes, dec_filt=conv_filters)

    outs_final = [outs_dec]*n_outs
    m = Model(inp, outs_final)
    if verbose:
        m.summary()
    return m



def se_lstm_block_timedist(inp, nb_timestep, units=512, print_shapes=True, lstm_filters=512, return_sequences=True):

    inp_rep = Lambda(lambda y: K.repeat_elements(K.expand_dims(y, axis=1), nb_timestep, axis=1),
                     lambda s: (s[0], nb_timestep) + s[1:])(inp)
    x = TimeDistributed(GlobalAveragePooling2D())(inp_rep)
    #print('shape after AvgPool',x.shape)
    x = TimeDistributed(Dense(units, activation='relu'))(x)
    #print('shape after first dense',x.shape)

    # Normally se block would feed into another fully connected. Instead, we feed it to an LSTM.
    x = LSTM(lstm_filters, return_sequences=return_sequences, unroll=True, activation='relu')(x) #, activation='relu'
    #print('shape after lstm',x.shape)

    x = TimeDistributed(Dense(inp.shape[-1].value, activation='sigmoid'))(x)
    #print('shape after second dense:', x.shape)

    x = Lambda(lambda y: K.expand_dims(K.expand_dims(y, axis=2),axis=2),
                lambda s: (s[0], s[1], 1, 1, s[2]))(x)
    #print('shape before mult',x.shape)

    # x is (bs, t, 1, 1, 2048)
    # inp_rep is (bs, t, r, c, 2048)
    out = Multiply()([x,inp_rep])

    #print('shape out',out.shape)
    # out is (bs, t, r, c, 2048)

    return out


def xception_se_lstm_nodecoder(input_shape = (240, 320, 3),
                     nb_timestep=3,
                     conv_filters=512,
                     lstm_filters=512,
                     verbose=True,
                     print_shapes=False,
                     n_outs=1,
                     ups=8,
                     freeze_enc=False,
                     return_sequences=True):
    inp = Input(shape = input_shape)

    ### ENCODER ###
    xception = Xception_wrapper(include_top=False, weights='imagenet', input_tensor=inp, pooling=None)
    if print_shapes: print('xception output shapes:',xception.output.shape)
    if freeze_enc:
        for layer in xception.layers:
            layer.trainable = False

    ### LSTM over SE representation ###
    x = se_lstm_block_timedist(xception.output, nb_timestep, lstm_filters=lstm_filters, return_sequences=return_sequences)

    ### DECODER ###
    dil_rate = (2,2)
    x = TimeDistributed(Conv2D(conv_filters, 3, padding='same', activation='relu', dilation_rate=dil_rate))(x)
    x = TimeDistributed(Conv2D(conv_filters, 3, padding='same', activation='relu',  dilation_rate=dil_rate))(x)
    #outs_dec = TimeDistributed(UpSampling2D((2,2), interpolation='bilinear'))(x)
    outs_dec = TimeDistributed(MaxPooling2D((4,4)))(x)

    #print('outs_final shape:', outs_dec.shape)

    #x = TimeDistributed(Dropout(0.3))(x)
    #x = TimeDistributed(Conv2D(filters=conv_filters, kernel_size=3, padding='same', activation='relu'))(x)
    #x = TimeDistributed(Dropout(0.3))(x)
    #x = TimeDistributed(Conv2D(1, kernel_size=1, padding='same', activation='relu'))(x)
    #outs_dec = TimeDistributed(UpSampling2D(size=(ups,ups), interpolation='bilinear'))(x)
    #outs_final = [outs_dec]*n_outs

    m = Model(inp, outs_dec)
    if verbose:
        m.summary()
    return m
