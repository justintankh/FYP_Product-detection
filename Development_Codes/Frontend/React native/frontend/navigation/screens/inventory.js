import { StatusBar } from "expo-status-bar";
import React, { useState, useEffect } from "react";
import { StyleSheet, Text, View, Image } from "react-native";
import { NavigationContainer, useIsFocused } from "@react-navigation/native";
import routeLogin from "../Utilis";

export default function InventoryScreen({ navigation, route }) {
	// const isFocused = useIsFocused();
	// if (isFocused) {
	// 	console.log(`${route.name} is focused`);
	//}

	return (
		<View>
			<Image style={{ height: "100%", width: "100%" }} source={require("../../assets/images/photo1.png")}></Image>
		</View>
	);
}
