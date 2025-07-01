import React, { useState, useRef } from "react";
import { SafeAreaView, View, Text, TextInput, Button, StyleSheet, Alert } from "react-native";
import { WebView } from "react-native-webview";

export default function App() {
  const [num, setNum] = useState("");
  const web = useRef(null);

  const submit = () => {
    if (num.match(/^[0-9]$/)) {
      if (web.current) {
        web.current.injectJavaScript(`window.processNumber(${num});true;`);
      }
      setNum("");
    } else {
      Alert.alert("Input must be 0‑9");
    }
  };

  return (
    <SafeAreaView style={{ flex: 1, backgroundColor: "#000" }}>
      <WebView
        ref={web}
        originWhitelist={["*"]}
        source={{ uri: "file:///android_asset/custom/bridge.html" }}
        style={{ flex: 1 }}
      />
      <View style={styles.row}>
        <Text style={styles.txt}>Number:</Text>
        <TextInput
          style={styles.inp}
          value={num}
          onChangeText={setNum}
          keyboardType="numeric"
          maxLength={1}
        />
        <Button title="Send" onPress={submit} />
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  row: { flexDirection: "row", padding: 10, alignItems: "center" },
  txt: { color: "#fff", marginRight: 6 },
  inp: { backgroundColor: "#eee", width: 60, textAlign: "center", marginRight: 8 }
});