from quote_source.client.TimeFrame import TimeFrame
def check_tf_could_be_up(from_tf:TimeFrame, to_tf:TimeFrame)->bool:
    return to_tf.to_seconds()%from_tf.to_seconds()==0

def count_candle_in_up_candle(from_tf:TimeFrame, to_tf:TimeFrame)->bool:
    return to_tf.to_seconds()//from_tf.to_seconds()