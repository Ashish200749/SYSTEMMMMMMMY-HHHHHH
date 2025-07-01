# Color Predictor React Native App (APK-ready)

## Build Steps

```bash
npm install
npx react-native-asset           # copies python & html into android assets
npx react-native run-android     # or open android folder in Android Studio, Build › APK
```

Enter Jalwa result number (0‑9) and the app runs the prediction logic offline
and posts VIP predictions / win messages to Telegram.