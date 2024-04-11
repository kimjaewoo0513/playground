import math
import os
os.environ['tf_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
import pyupbit
import numpy as np
from config import baseInterval
from make_log import make_log

def scaleDown(df, name, i):
    return round(df[name].iloc[i]/math.pow(10,len(str(int(df[name].iloc[0])))),5)

def makeX(df, i):
    tempX = []
    tempX.append(scaleDown(df, 'open', i))
    tempX.append(scaleDown(df, 'high', i))
    tempX.append(scaleDown(df, 'low', i))
    tempX.append(scaleDown(df, 'volume', i))
    tempX.append(scaleDown(df, 'value', i))
    tempX.append(scaleDown(df, 'close', i))
    tempX.append(math.floor(df.index[i].hour/3))
    return np.array(tempX)  # np.squeeze를 사용하지 않고 바로 넘파이 배열을 반환

def makeY(df, i):
    gap = df['close'].iloc[i+1] - df['close'].iloc[i]
    tempY = 1 if gap > 0 else 0
    return tempY

def predict_buy(pTicker):
    try:
        x = []
        y = []
        df = pyupbit.get_ohlcv(ticker=pTicker, interval=baseInterval, count=365, period=1)
        if len(df) > 20:
            for i in range(len(df)):
                if i < len(df)-2:
                    x.append(makeX(df, i))
                    y.append(makeY(df, i))

            inputs = tf.keras.Input(shape=(7,))
            h1 = tf.keras.layers.Dense(64, activation='relu')(inputs)
            h2 = tf.keras.layers.Dense(128, activation='tanh')(h1)
            h3 = tf.keras.layers.Dense(256, activation='relu')(h2)
            h4 = tf.keras.layers.Dense(128, activation='relu')(h3)
            h5 = tf.keras.layers.Dense(64, activation='relu')(h4)
            outputs = tf.keras.layers.Dense(1, activation='sigmoid')(h5)
            model = tf.keras.Model(inputs=inputs, outputs=outputs)
            model.compile(optimizer="adam", loss="binary_crossentropy", metrics=['accuracy'])
            
            x = np.array(x)
            y = np.array(y)  # y 데이터도 넘파이 배열로 변환
            
            fitInfo = model.fit(x, y, epochs=2000, batch_size=32)  # 배치 크기를 지정하여 학습
            
            # 모델 예측 시 입력 데이터의 차원을 맞춰줌
            result = model.predict(np.expand_dims(makeX(df, -2), axis=0))
            
            return {'accuracy': round(fitInfo.history['accuracy'][-1],2),
                    'predict': round(result[0][0],2)}
        else:
            return None
    except Exception as ex:
        type = '에러'
        log = 'buy_conditions error! : ' + pTicker + ' : ' + str(ex)
        make_log(type, log, detail=True)
        return '에러'
    

print(predict_buy('KRW-WAVES'))
