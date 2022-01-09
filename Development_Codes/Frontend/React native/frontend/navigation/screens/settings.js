import { StatusBar } from "expo-status-bar";
import React, { useState, useEffect } from "react";
import { StyleSheet, Text, View, Image } from "react-native";
import routeLogin from "../Utilis";

export default function SettingsScreen({ navigation, route }) {
	return (
		<View style={{ flex: 1, alignItems: "center", justifyContent: "center" }}>
			<Image style={{ height: "100%", width: "100%" }} source={require("../../assets/images/photo1.png")}></Image>
		</View>
	);
}
