#!/usr/bin/env python3
import requests
import os

# Using the existing bot token from the app
BOT_TOKEN = "8037812910:AAEuGljU5I99-FphxEz6ekefnAcxWanqUGk"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_apk_to_telegram(chat_id, file_path):
    """Send APK file to specified Telegram chat"""
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    file_size = os.path.getsize(file_path) / 1024 / 1024  # MB
    print(f"📱 Preparing to send APK ({file_size:.1f}MB) to Telegram...")
    
    try:
        # Send document (APK file)
        with open(file_path, 'rb') as apk_file:
            files = {'document': apk_file}
            data = {
                'chat_id': chat_id,
                'caption': '🎯 Color Predictor APK\n\n✅ Ready to install on Android\n📱 Size: 3.3MB\n🔧 Compatible with Android 5.0+\n\n📋 Installation:\n1. Download this APK\n2. Enable "Unknown Sources" in Android settings\n3. Tap APK to install\n4. Launch "Color Predictor" app'
            }
            
            response = requests.post(f"{API_URL}/sendDocument", data=data, files=files)
            
        if response.status_code == 200:
            result = response.json()
            if result.get('ok'):
                print("✅ APK sent successfully to Telegram!")
                return True
            else:
                print(f"❌ Telegram API error: {result.get('description')}")
                return False
        else:
            print(f"❌ HTTP error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error sending APK: {str(e)}")
        return False

def get_bot_info():
    """Get information about the bot"""
    try:
        response = requests.get(f"{API_URL}/getMe")
        if response.status_code == 200:
            result = response.json()
            if result.get('ok'):
                bot_info = result.get('result')
                print(f"🤖 Bot Info:")
                print(f"   Name: {bot_info.get('first_name')}")
                print(f"   Username: @{bot_info.get('username')}")
                print(f"   ID: {bot_info.get('id')}")
                return True
        return False
    except Exception as e:
        print(f"❌ Error getting bot info: {str(e)}")
        return False

if __name__ == "__main__":
    print("🤖 Telegram APK Sender")
    print("=" * 40)
    
    # Check bot status
    if not get_bot_info():
        print("❌ Could not connect to Telegram bot")
        exit(1)
    
    # APK file path
    apk_path = "/workspace/ColorPredictorApp.apk"
    
    print(f"\n📁 APK Location: {apk_path}")
    
    # Get chat ID from user
    print("\n📱 To send the APK, I need your Telegram chat ID or username.")
    print("Options:")
    print("1. Your Telegram username (e.g., @yourusername)")
    print("2. Your chat ID (numeric)")
    print("3. Send to the existing channel (@preditorssytemm)")
    
    choice = input("\nEnter option (1/2/3) or your chat ID/username: ").strip()
    
    if choice == "3":
        chat_id = "@preditorssytemm"
    elif choice.startswith("@"):
        chat_id = choice
    elif choice.isdigit():
        chat_id = choice
    elif choice in ["1", "2"]:
        chat_input = input(f"Enter your {'username' if choice == '1' else 'chat ID'}: ").strip()
        chat_id = chat_input
    else:
        chat_id = choice
    
    print(f"\n📤 Sending APK to: {chat_id}")
    
    # Send the APK
    success = send_apk_to_telegram(chat_id, apk_path)
    
    if success:
        print("\n✅ APK sent successfully!")
        print("📱 Check your Telegram for the file")
    else:
        print("\n❌ Failed to send APK")
        print("💡 Make sure:")
        print("   - Your chat ID/username is correct")
        print("   - You've started a conversation with the bot")
        print("   - The bot has permission to send files")