# manual_predictor.py – offline logic + Telegram call via requests
import requests, time, json, os

BOT_TOKEN = "8037812910:AAEuGljU5I99-FphxEz6ekefnAcxWanqUGk"
CHANNEL   = "@preditorssytemm"
API_URL   = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

losses = 0
mode   = "simple"
level  = 1
total_wins = 0
total_amount = 0
amount_map = {1:100,2:200,3:400,4:800,5:1600}
last_pred = None

BIG   = (2,7,8,9)
SMALL = (0,3,5)

def get_category(n:int):
    return "BIG" if n in BIG else "SMALL" if n in SMALL else "SKIP"

def opposite(pred:str): return "SMALL" if pred=="BIG" else "BIG"

def tg_send(msg:str):
    try:
        requests.post(API_URL, data={"chat_id":CHANNEL, "text":msg})
    except Exception as e:
        print("Telegram error:", e)

def process(num:int):
    global losses, mode, level, last_pred, total_wins, total_amount
    cat = get_category(num)
    if cat=="SKIP": return "SKIP"

    # evaluate previous prediction
    if last_pred:
        win = (cat == last_pred)
        if win:
            amt = amount_map.get(level,100)
            tg_send(f"✅ WIN\nAmount ₹{amt}")
            total_wins += 1
            total_amount += amt
            losses, mode, level = 0, "simple", 1
            last_pred = None
            return "WIN"
        else:
            losses += 1
            mode = "opposite" if mode=="simple" else "simple"
            level = min(level+1,5)

    # fire after pair of losses
    if losses>=2:
        pred = opposite(cat) if mode=="opposite" else cat
        tg_send(f"🔥 VIP PREDICTION 🔥\nPrediction: {pred}\nLevel: {level}")
        last_pred = pred
        losses = 0
        return pred
    else:
        last_pred = cat
        return "WAIT"